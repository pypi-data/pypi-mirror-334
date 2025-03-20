"""Tests for the TimeseriesResponseParser functionality.

This module tests both raw and aggregated responses, covering cases for missing
keys, empty responses, and handling of sublists.
"""

import logging
from datetime import datetime, timezone

import pytest
from pandas import DataFrame

from piscada_foresight.parser_graphql_to_df. \
    time_series.timeseries_response_parser import (
    TimeseriesResponseParser,
)


def test_get_values_aggregated_missing_values(
    mock_query_manager: object,
    aggregated_no_values: object,
    caplog: object,
) -> None:
    """Checks behavior when no aggregator data is available (empty values arrays).

    Ensure a warning is logged and an empty DataFrame is returned.
    """
    mock_query_manager.run_query.return_value = aggregated_no_values

    parser = TimeseriesResponseParser()

    entity_variables = {
        f"entityId_{i}": entity_id
        for i, entity_id in enumerate(["entityId_0", "entityId_1"])
    }

    with caplog.at_level("WARNING"):
        result = parser.parse(
            response=aggregated_no_values,
            entity_variables=entity_variables,
            start="2023-01-01",
            end="2023-01-02",
            query_type="aggregated",
        )
        # Check warning is logged
        assert "No data found for the requested time range" in caplog.text  # noqa: S101
        # Check result is an empty DataFrame
        assert isinstance(result, DataFrame)  # noqa: S101
        assert result.empty  # noqa: S101


@pytest.fixture
def parser() -> TimeseriesResponseParser:
    """Fixture to create a TimeseriesResponseParser instance."""
    return TimeseriesResponseParser()


def test_parse_raw_values_success(
    parser: TimeseriesResponseParser,
    raw_timeseries_response: object,
) -> None:
    """Test parsing a valid 'raw' timeseries response.

    The response includes multiple eventTimes and numeric values.
    """
    entity_variables = {
        "entityId_0": (
            "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-"
            "000000000001"
        ),
        "entityId_1": (
            "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-"
            "000000000002"
        ),
    }

    dataframe = parser.parse(
        response=raw_timeseries_response,
        entity_variables=entity_variables,
        start=datetime(2025, 1, 14, 9, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 14, 11, 0, 0, tzinfo=timezone.utc),
        query_type="raw",
    )

    # We expect two columns, one per entity name
    assert isinstance(dataframe, DataFrame)  # noqa: S101
    assert not dataframe.empty, "DataFrame should not be empty for valid raw data"  # noqa: S101
    assert "360001 Temperature" in dataframe.columns  # noqa: S101
    assert "360001 Temperature Setpoint" in dataframe.columns  # noqa: S101

    # Check some expected values.
    # (The parser forward-fills missing times by default,
    # so you might see more rows than
    # raw data.)
    first_setpoint = dataframe["360001 Temperature Setpoint"].iloc[0]
    expected_first_setpoint = 19.5
    assert first_setpoint == expected_first_setpoint, \
        "Incorrect setpoint value in first row" # noqa: S101


def test_parse_raw_values_missing_keys(
    parser: TimeseriesResponseParser,
    raw_missing_values_tag_response: object,
) -> None:
    """Ensures RuntimeError is raised if keys are missing from response.

    For example, if the 'quantity' or 'values' keys are missing.
    """
    entity_variables = {"entityId_0": "fake_entity_id"}

    with pytest.raises(
        RuntimeError,
        match="Could not retrieve raw values for entity 'fake_entity_id'",
    ):
        parser.parse(
            response=raw_missing_values_tag_response,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="raw",
        )


def test_parse_raw_values_entity_none(
    parser: TimeseriesResponseParser,
) -> None:
    """Test handling when response[variable_name] is None.

    If the response is None, a TypeError will occur when accessing subkeys,
    which should be turned into a RuntimeError by the parser.
    """
    response = {"entityId_0": None}  # This will cause a TypeError
    entity_variables = {"entityId_0": "fake_entity_id"}

    with pytest.raises(RuntimeError, match="Could not find entity 'fake_entity_id'"):
        parser.parse(
            response=response,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="raw",
        )


def test_parse_raw_values_no_entities(
    parser: TimeseriesResponseParser,
    caplog: object,
) -> None:
    """Test behavior when no entities or data are present.

    If the response is empty or if entity_variables is empty, an empty
    DataFrame is expected.
    """
    response = {}
    entity_variables = {}

    with caplog.at_level(logging.WARNING):
        dataframe = parser.parse(
            response=response,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="raw",
        )
    assert dataframe.empty, \
        "Should return an empty DataFrame when no entities or data are present."  # noqa: S101


def test_parse_aggregated_values_success(
    parser: TimeseriesResponseParser,
    aggregated_timeseries_response: object,
) -> None:
    """Test parsing a valid 'aggregated' timeseries response.

    The response includes several aggregationFunctions for each entity.
    """
    entity_variables = {
        "entityId_0": (
            "brick:Supply_Air_Temperature_Sensor:0000-0000-0000-0000-"
            "000000000001"
        ),
        "entityId_1": (
            "brick:Effective_Supply_Air_Temperature_Setpoint:0000-0000-0000-0000-"
            "000000000002"
        ),
    }

    dataframe = parser.parse(
        response=aggregated_timeseries_response,
        entity_variables=entity_variables,
        start=datetime(2025, 1, 14, 9, tzinfo=timezone.utc),
        end=datetime(2025, 1, 14, 11, tzinfo=timezone.utc),
        query_type="aggregated",
    )

    # We expect columns like "360001 Temperature|min", "360001 Temperature|max", etc.
    expected_cols_entity0 = [
        "360001 Temperature|min",
        "360001 Temperature|max",
        "360001 Temperature|avg",
        "360001 Temperature|count",
        "360001 Temperature|last",
    ]
    for col in expected_cols_entity0:
        assert col in dataframe.columns  # noqa: S101

    expected_cols_entity1 = [
        "360002 Temperature Setpoint|min",
        "360002 Temperature Setpoint|max",
        "360002 Temperature Setpoint|avg",
        "360002 Temperature Setpoint|count",
        "360002 Temperature Setpoint|last",
    ]
    for col in expected_cols_entity1:
        assert col in dataframe.columns  # noqa: S101

    # Check some values
    expected_value = 19.5
    assert dataframe.loc["2025-01-14 09:59:59.786000+00:00", \
        "360001 Temperature|min"] == expected_value  # noqa: S101
    expected_value = 19.8
    assert dataframe.loc["2025-01-14 09:59:59.786000+00:00", \
        "360002 Temperature Setpoint|last"] == expected_value  # noqa: S101


def test_parse_aggregated_values_missing_key(
    parser: TimeseriesResponseParser,
    aggregated_tag_missing: object,
) -> None:
    """RuntimeError  raised when keys in response are missing.

    For example, if aggregated values cannot be retrieved.
    """
    entity_variables = {"entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000"}

    with pytest.raises(
        RuntimeError,
        match="Could not retrieve aggregated values for entity 'brick:"
        "Supply_Air_Temperature_Sensor:0000-0000'",
    ):
        parser.parse(
            response=aggregated_tag_missing,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="aggregated",
        )


def test_parse_aggregated_values_all_empty(
    parser: TimeseriesResponseParser,
    aggregated_empty_sublists: object,
    caplog: object,
) -> None:
    """Test behavior when all sublists in 'aggregatedTimeseries' are empty.

    A warning should be logged and an empty DataFrame returned.
    """
    entity_variables = {"entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000"}

    with caplog.at_level(logging.WARNING):
        dataframe = parser.parse(
            response=aggregated_empty_sublists,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="aggregated",
        )

    assert dataframe.empty, \
        "Should return empty DataFrame if no aggregator sublists have data."  # noqa: S101
    assert "No data found for the requested time range" in caplog.text  # noqa: S101


def test_parse_aggregated_values_partial_empty(
    parser: TimeseriesResponseParser,
    aggregated_one_empty_sublist_response: object,
) -> None:
    """Test behavior when some aggregator sublists are empty.

    Only the non-empty columns should be returned.
    """
    entity_variables = {"entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000"}

    dataframe = parser.parse(
        response=aggregated_one_empty_sublist_response,
        entity_variables=entity_variables,
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        query_type="aggregated",
    )
    assert not dataframe.empty, \
        "Should not be empty if at least one aggregator sublist has data"  # noqa: S101
    assert "360001 Temperature|max" in dataframe.columns  # noqa: S101
    assert "360001 Temperature|min" not in dataframe.columns, \
        "Empty aggregator sublist shouldn't appear as a column"  # noqa: S101
    expected_value =  19.7
    assert dataframe.iloc[0, 0] == expected_value, "Unexpected aggregated value"  # noqa: S101


def test_parse_unknown_query_type(
    parser: TimeseriesResponseParser,
) -> None:
    """Test that an unknown query_type raises a ValueError."""
    with pytest.raises(ValueError, match="Unknown query_type: invalid_type"):
        parser.parse(
            response={},
            entity_variables={},
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="invalid_type",
        )
