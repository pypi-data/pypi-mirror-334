"""Utility functions for file and DataFrame operations used in tests."""
import json
from pathlib import Path
from typing import Union, cast

import pandas as pd


def load_file_content(filename: str) -> Union[dict, str]:
    """Load content from a text, JSON, or GraphQL file.

    The file is expected to be located in the test_config directory.

    Args:
        filename (str): The name of the file to load, including its extension.

    Returns:
        dict | str: Parsed JSON data if the file is a JSON file, or raw string
            content for other files.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is unsupported.

    """
    config_path = Path(__file__).parent / "../test_config" / filename
    if not config_path.exists():
        msg = f"File not found: {config_path.resolve()}"
        raise FileNotFoundError(msg)

    file_extension = config_path.suffix.lower()
    with config_path.open("r", encoding="utf-8") as file:
        if file_extension == ".json":
            return json.load(file)
        if file_extension in {".txt", ".graphql"}:
            return file.read()
        msg = f"Unsupported file type: {file_extension}"
        raise ValueError(msg)


def save_dataframe(dataframe: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to a CSV file with microsecond precision.

    Args:
        dataframe (pd.DataFrame): The DataFrame to save.
        path (str): The file path where the DataFrame will be saved.

    Returns:
        None

    """
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(save_path, index=True, date_format="%Y-%m-%dT%H:%M:%S.%f%z")


def load_dataframe(path: str) -> pd.DataFrame:
    """Load a DataFrame from a CSV file and ensure its index is timezone-aware (UTC).

    Args:
        path (str): The file path from which the CSV file is loaded.

    Returns:
        pd.DataFrame: The loaded DataFrame with a timezone-aware index.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        TypeError: If the loaded index is not a DatetimeIndex.

    """
    save_path = Path(path)
    if not save_path.exists():
        msg = f"File not found: {save_path}"
        raise FileNotFoundError(msg)

    dataframe = pd.read_csv(save_path, index_col=0, parse_dates=True)
    if not isinstance(dataframe.index, pd.DatetimeIndex):
        msg = "Index is not a DatetimeIndex"
        raise TypeError(msg)
    dataframe.index = cast(pd.DatetimeIndex, dataframe.index)
    if dataframe.index.tz is None:
        dataframe.index = dataframe.index.tz_localize("UTC")
    else:
        dataframe.index = dataframe.index.tz_convert("UTC")

    return dataframe


def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    """Compare two DataFrames by flooring their indexes to the nearest second.

    Args:
        df1 (pd.DataFrame): The first DataFrame to compare.
        df2 (pd.DataFrame): The second DataFrame to compare.

    Raises:
        AssertionError: If the DataFrames are not equal.

    """
    if not isinstance(df1.index, pd.DatetimeIndex):
        msg = "df1.index is not a DatetimeIndex"
        raise TypeError(msg)
    df1.index = cast(pd.DatetimeIndex, df1.index)

    if not isinstance(df2.index, pd.DatetimeIndex):
        msg = "df2.index is not a DatetimeIndex"
        raise TypeError(msg)
    df2.index = cast(pd.DatetimeIndex, df2.index)

    df1.index = df1.index.floor("S")
    df2.index = df2.index.floor("S")

    pd.testing.assert_frame_equal(
        df1,
        df2,
        check_dtype=False,
        check_exact=False,
    )
