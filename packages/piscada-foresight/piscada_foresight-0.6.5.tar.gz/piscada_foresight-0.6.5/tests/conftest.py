"""Conftest for Piscada Foresight tests, providing shared fixtures."""

from typing import Any, Dict
from unittest.mock import Mock

import pytest

from piscada_foresight.parser_graphql_to_df. \
    time_series.timeseries_response_parser import (
    TimeseriesResponseParser,
)
from tests.utils.test_utils import load_file_content


@pytest.fixture
def parser() -> TimeseriesResponseParser:
    """Return an instance of TimeseriesResponseParser."""
    return TimeseriesResponseParser()


@pytest.fixture
def mock_query_manager() -> Mock:
    """Return a mock implementation of the QueryManager."""
    return Mock()


@pytest.fixture
def aggregated_timeseries_response() -> Dict[str, Any]:
    """Return the aggregated timeseries response from JSON."""
    return load_file_content("responses/aggregated_timeseries.json")


@pytest.fixture
def aggregated_one_empty_sublist_response() -> Dict[str, Any]:
    """Return aggregated data with one empty sublist from JSON."""
    return load_file_content("responses/aggregated_one_empty_sublist.json")


@pytest.fixture
def aggregated_tag_missing() -> Dict[str, Any]:
    """Return aggregated data missing a tag from JSON."""
    return load_file_content("responses/aggregated_tag_missing.json")


@pytest.fixture
def aggregated_empty_sublists() -> Dict[str, Any]:
    """Return aggregated data with empty sublists from JSON."""
    return load_file_content("responses/aggregated_empty_sublists.json")


@pytest.fixture
def aggregated_no_values() -> Dict[str, Any]:
    """Return aggregated data with no values from JSON."""
    return load_file_content("responses/aggregated_no_values.json")


@pytest.fixture
def raw_missing_values_tag_response() -> Dict[str, Any]:
    """Return raw data missing values for some tags from JSON."""
    return load_file_content("responses/raw_missing_values_tag.json")


@pytest.fixture
def raw_timeseries_response() -> Dict[str, Any]:
    """Return raw timeseries response from JSON."""
    return load_file_content("responses/raw_timeseries.json")


@pytest.fixture
def no_values_response(raw_timeseries_response: Dict[str, Any]) -> Dict[str, Any]:
    """Return a raw timeseries response with all values removed."""
    response = raw_timeseries_response
    response["entityId_0"]["trait"]["quantity"]["values"] = []
    response["entityId_1"]["trait"]["quantity"]["values"] = []
    return response
