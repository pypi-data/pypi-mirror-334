"""Handles query loading, rendering, and management."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Iterator

from jinja2 import Environment, FileSystemLoader, select_autoescape

log = logging.getLogger(__name__)


def os_walk(path: Path) -> Iterator[tuple[str, list[str], list[str]]]:
    """Mimic os.walk for usage with pathlib.

    Args:
        path (Path): A Path to walk.

    Yields:
        Tuples of (root, dirs, files) equivalent to os.walk.

    """
    for root, dirs, files in os.walk(str(path)):
        yield root, dirs, files

class QueryHandler:
    """Encapsulates query management logic."""

    def __init__(self, base_directory: str) -> None:
        """Initialize QueryHandler.

        Args:
        base_directory (str): The base directory where query templates are stored.

        """
        self.queries_dir = Path(base_directory)
        self.query_dict: Dict[str, str] = {}
        #Last query string being loaded
        self.query_text: str | None = None
        self._load_queries()

    def _collect_queries_from_directory(
        self, directory: Path, *, make_absolute: bool = False, base: Path | None = None,
    ) -> Dict[str, str]:
        """Collect query templates from the specified directory.

        Searches for files ending with .j2 or .graphql inside the directory.
        If make_absolute is True, returns the file paths as absolute, otherwise relative
        to the provided base (or self.queries_dir if base is None).

        Args:
            directory (Path): The directory to search.
            make_absolute (bool): Flag indicating whether to return absolute paths.
            base (Path | None): The base directory to use for relative paths.

        Returns:
            A dictionary mapping the query name (stem) to its file path as a string.

        """
        collected: Dict[str, str] = {}
        for root, _, files in os_walk(directory):
            for file_name in files:
                if file_name.endswith((".j2", ".graphql")):
                    query_name = Path(file_name).stem
                    file_path = (Path(root) / file_name).resolve()
                    if make_absolute:
                        collected[query_name] = str(file_path)
                    else:
                        base_dir = base if base is not None else self.queries_dir
                        relative_path = file_path.relative_to(base_dir)
                        collected[query_name] = str(relative_path)
        return collected

    def _load_queries(self) -> Dict[str, str]:
        """Load query templates in a dictionary from the base queries directory.

        Allow to load the default queries from the queries directory.

        Returns:
            A dictionary mapping query names to their paths.

        """
        self.query_dict = self._collect_queries_from_directory(
            self.queries_dir,
            make_absolute=False,
        )
        return self.query_dict

    def add_queries_from_directory(self, directory: str) -> None:
        """Add all query templates from a new directory.

        Searches for query files in the directory and adds them
        to the query dictionary with their absolute paths.

        Args:
            directory (str): The path to the directory that contains query templates.

        """
        new_dir = Path(directory).resolve()
        if not new_dir.is_dir():
            msg = f"Provided directory {directory} is not a valid directory."
            raise ValueError(msg)
        new_queries = self._collect_queries_from_directory(new_dir, make_absolute=True)
        for query_name, file_path in new_queries.items():
            if query_name in self.query_dict:
                log.warning("Query '%s' \
                already exists and will be overridden.", query_name)
            self.query_dict[query_name] = file_path
        log.info("Queries loaded from directory: %s", new_dir)

    def load_query(self, query_name: str,
                   jinja_variables: dict[str, Any] | None,
                   ) -> str:
        """Load and render a query template by name.

        Args:
            query_name (str): The name (stem) of the query file to load.
            jinja_variables (dict[str, Any] | None): To render into a Jinja template.

        Returns:
            The loaded query text.

        Raises:
            ValueError: If the query file does not exist or is unsupported.

        """
        template_path = self.query_dict.get(query_name)
        if not template_path:
            msg = f"Query '{query_name}' not found in query_dict."
            raise ValueError(msg)

        full_path = Path(template_path) if Path(template_path).is_absolute() \
            else self.queries_dir / template_path

        if template_path.endswith(".j2"):
            jinja_env = Environment(
                loader=FileSystemLoader(str(full_path.parent)),
                autoescape=select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            template = jinja_env.get_template(full_path.name)
            query_text = template.render(**(jinja_variables or {}))
        elif template_path.endswith(".graphql"):
            with full_path.open("r", encoding="utf-8") as file:
                query_text = file.read()
        else:
            msg = f"Unsupported query file type: '{template_path}'."
            raise ValueError(msg)

        self.query_text = query_text
        return query_text

    def add_query(self, query_name: str, query_path: str) -> None:
        """Add a new query to the list of queries.

        Args:
            query_name (str): The name (stem) of the query.
            query_path (str): The relative or absolute path to the query template.

        """
        if query_name in self.query_dict:
            log.warning("Query '%s' already exists and will be overridden.", query_name)
        self.query_dict[query_name] = query_path

    def delete_queries(self, queries_to_delete: list[str]) -> None:
        """Delete specified queries from the query dictionary.

        Args:
            queries_to_delete (List[str]): A list of query names to delete.

        """
        for query_name in queries_to_delete:
            if query_name in self.query_dict:
                del self.query_dict[query_name]
                log.info("Deleted query: %s", query_name)
            else:
                log.warning("Query '%s' not found in query_dict. \
                 No action taken.", query_name)
