"""Manages queries and GraphQL client."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Callable, ClassVar, Self

from gql import Client, gql

from piscada_foresight.http_piscada import ForesightHTTPXTransport
from piscada_foresight.queries_templates.query_handler import QueryHandler

log = logging.getLogger(__name__)


class QueryManager:
    """Manages queries and GraphQL client.

    This class implements a singleton pattern to maintain a single
    set of loaded queries and allow consistent access to an HTTPX-based GraphQL client.
    """

    _instance: ClassVar[QueryManager | None] = None

    def __new__(cls, *args: object, **kwargs: object) -> Self|QueryManager:
        """Create or return the existing singleton instance of QueryManager."""
        _, _ = args, kwargs
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        domain: str,
        client_id: str | None = None,
        client_secret: str | None = None,
        graphql_endpoint: str | None = None,
        json_serialize: Callable[[Any], str] | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize QueryManager to connect to the GraphQL endpoint.

        Args:
            domain (str): The Piscada Foresight domain.
            client_id (str): The OAuth2 client identifier used for authentication.
            client_secret (str): The OAuth2 client secret used for authentication.
            graphql_endpoint (str): The URL of the Piscada Foresight GraphQL endpoint.
            json_serialize (Callable[[Any], str]): Serializes object into JSON string.
            **kwargs (object): Additional keyword argument.

        """
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.graphql_endpoint = graphql_endpoint
        self.json_serialize = json_serialize
        self.kwargs = kwargs
        self.transport = self._create_transport()
        self.client: Client = self._create_client()
        # Instantiate QueryHandler to manage query logic.
        self.query_handler = QueryHandler(base_directory=str(Path(__file__).parent))
        super().__init__()

    def _create_transport(self) -> ForesightHTTPXTransport:
        """Create and return a ForesightHTTPXTransport."""
        json_serialize = self.json_serialize if \
            self.json_serialize is not None else json.dumps
        return ForesightHTTPXTransport(
            self.domain,
            self.client_id,
            self.client_secret,
            self.graphql_endpoint,
            json_serialize,
            **self.kwargs,
        )

    def _create_client(self) -> Client:
        """Create and return a GraphQL client using the current transport."""
        return Client(transport=self.transport, fetch_schema_from_transport=False)

    def update_transport(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        graphql_endpoint: str | None = None,
        json_serialize: Callable[[Any], str] | None = None,
        **kwargs: object,
    ) -> ForesightHTTPXTransport:
        """Update the transport configuration."""
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if graphql_endpoint is not None:
            self.graphql_endpoint = graphql_endpoint
        if json_serialize is not None:
            self.json_serialize = json_serialize
        self.kwargs.update(kwargs)

        self.transport = self._create_transport()
        self.client.transport = self.transport
        return self.transport

    def add_queries_from_directory(self, directory: str) -> None:
        """Delegate adding queries from a new directory to QueryHandler."""
        self.query_handler.add_queries_from_directory(directory)

    def load_query(self,
                   query_name: str,
                   jinja_variables: dict[str, Any] | None,
                   ) -> str:
        """Load and render a query using QueryHandler."""
        return self.query_handler.load_query(query_name, jinja_variables)

    def add_query(self, query_name: str, query_path: str) -> None:
        """Add a new query using QueryHandler."""
        self.query_handler.add_query(query_name, query_path)

    def execute_query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Execute a GraphQL query with given variables.

        Args:
            query (str): The query string to execute.
            variables (dict[str, Any]): Variables for the query.

        Returns:
            A dictionary representing the GraphQL response.

        """
        try:
            response = self.client.execute(gql(query), variable_values=variables)
        except Exception as execution_error:
            msg = (
                f"An error occurred while executing the query: {execution_error}.\n"
                f"Query: {query}\nVariables: {variables}"
            )
            raise RuntimeError(msg) from execution_error
        return response

    def run_query(
        self,
        query_name: str,
        jinja_variables: dict[str, Any] | None = None,
        query_variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Load and execute a query.

        Args:
            query_name (str): The query's name.
            jinja_variables (dict[str, Any] | None): for Jinja template rendering.
            query_variables (dict[str, Any] | None): for the GraphQL query.

        Returns:
            The GraphQL response as a dictionary.

        """
        if jinja_variables is None:
            jinja_variables = {}
        if query_variables is None:
            query_variables = {}

        query_text = self.load_query(query_name, jinja_variables)
        return self.execute_query(query_text, query_variables)
