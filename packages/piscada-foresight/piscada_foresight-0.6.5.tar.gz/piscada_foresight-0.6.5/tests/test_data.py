"""Tests for the piscada_foresight.data module, verifying get_values function behaviors.

This module includes tests for successful data retrieval, error conditions, and
aggregated data handling.
"""

from datetime import datetime, timezone
from typing import Any, Dict
from unittest.mock import MagicMock

import pandas as pd
import pytest

from piscada_foresight.data import get_value, get_values
from piscada_foresight.queries_templates.query_manager import QueryManager


def test_get_values_success(
        mock_query_manager: MagicMock,
        raw_timeseries_response: Dict[str, Any],
) -> None:
    """Tests that get_values successfully returns a DataFrame with expected data."""
    mock_query_manager.run_query.return_value = raw_timeseries_response
    data_frame = get_values(
        mock_query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
            "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
        ],
        start=datetime.now(tz=timezone.utc),
    )
    expected_value = 8
    if len(data_frame) != expected_value:
        pytest.fail("Expected 8 rows in the DataFrame.")
    if not pd.isna(data_frame["360001 Temperature"].iloc[0]):
        pytest.fail(
            "Expected NaN in the first row of '360001 Temperature' column.",
        )


def test_get_values_missing_values(
        mock_query_manager: MagicMock,
        no_values_response: Dict[str, Any],
) -> None:
    """Tests that get_values raises a RuntimeError when no data is available."""
    mock_query_manager.run_query.return_value = no_values_response
    with pytest.raises(RuntimeError):
        get_values(
            mock_query_manager,
            entity_ids=[
                "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
                "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
            ],
            start=datetime(1993, 2, 12, tzinfo=timezone.utc),
            end=datetime(1993, 2, 13, tzinfo=timezone.utc),
        )


def test_get_values_start_later_than_end(mock_query_manager: MagicMock) -> None:
    """Tests that get_values raises a ValueError when start > end."""
    with pytest.raises(
            ValueError,
            match="The 'start' datetime cannot be later than the 'end' datetime.",
    ):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1, tzinfo=timezone.utc),
            end=datetime(2023, 1, 31, tzinfo=timezone.utc),
        )


def test_get_values_start_or_end_not_timezone_aware(
        mock_query_manager: MagicMock,
) -> None:
    """Tests get_values raises a ValueError if start or end is not tz-aware."""
    # Separate raises for PT012 compliance:
    with pytest.raises(ValueError, match="The start parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1),  # no tzinfo  # noqa: DTZ001
            end=datetime(2023, 1, 31, tzinfo=timezone.utc),
        )

    with pytest.raises(ValueError, match="The start parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1),  # no tzinfo  # noqa: DTZ001
            end=datetime(2023, 1, 31),  # no tzinfo  # noqa: DTZ001
        )

    with pytest.raises(ValueError, match="The end parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1, tzinfo=timezone.utc),
            end=datetime(2023, 1, 31),  # no tzinfo  # noqa: DTZ001
        )


def test_get_values_aggregated_success(
        mock_query_manager: MagicMock,
        aggregated_timeseries_response: Dict[str, Any],
) -> None:
    """Checks that get_values retrieves aggregated data when aggregators are provided.

    Ensures that columns for each aggregator function exist in the result.
    """
    mock_query_manager.run_query.return_value = aggregated_timeseries_response
    data_frame = get_values(
        query_manager=mock_query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
            "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
        ],
        start=datetime(2025, 1, 14, 9, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 14, 11, 0, 0, tzinfo=timezone.utc),
        interval="1h",
        aggregation_functions=["min", "max", "avg", "count", "last"],
    )
    if data_frame.empty:
        pytest.fail("DataFrame should not be empty for valid aggregated data.")

    expected_columns = [
        "360001 Temperature|min",
        "360001 Temperature|max",
        "360001 Temperature|avg",
        "360001 Temperature|count",
        "360001 Temperature|last",
    ]
    for col in expected_columns:
        if col not in data_frame.columns:
            pytest.fail(f"Missing expected column: {col}")


def test_get_values_aggregated_invalid_aggregator(mock_query_manager: MagicMock)\
        -> None:
    """Verifies that ValueError is raised if any aggregator is invalid."""
    with pytest.raises(ValueError, match="Invalid aggregation function provided"):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            interval="1d",
            aggregation_functions=["min", "max", "foo"],  # 'foo' is invalid
        )


def test_get_values_aggregated_multiple_aggregators(
        mock_query_manager: MagicMock,
        aggregated_timeseries_response: Dict[str, Any],
) -> None:
    """Ensures that multiple valid aggregation functions are handled correctly."""
    mock_query_manager.run_query.return_value = aggregated_timeseries_response
    data_frame = get_values(
        query_manager=mock_query_manager,
        entity_ids=["entityId_0", "entityId_1"],
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        interval="1h",
        aggregation_functions=["min", "max", "avg"],
    )
    if data_frame.empty:
        pytest.fail("Aggregated DataFrame should not be empty.")

    for func in ["min", "max", "avg"]:
        col_0 = f"360001 Temperature|{func}"
        col_1 = f"360002 Temperature Setpoint|{func}"
        if col_0 not in data_frame.columns:
            pytest.fail(f"Missing {col_0} aggregator column.")
        if col_1 not in data_frame.columns:
            pytest.fail(f"Missing {col_1} aggregator column.")


def test_get_values_aggregated_interval_none_uses_default(
        mock_query_manager: MagicMock,
        aggregated_timeseries_response: Dict[str, Any],
) -> None:
    """If interval=None is passed, get_values should default to an interval (e.g. '1d').

    Confirms no error is raised and the query can run successfully.
    """
    mock_query_manager.run_query.return_value = aggregated_timeseries_response
    data_frame = get_values(
        query_manager=mock_query_manager,
        entity_ids=["entityId_0"],
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        interval=None,
        aggregation_functions=["min", "max", "avg", "count", "last"],
    )
    if data_frame.empty:
        pytest.fail("DataFrame should not be empty with default interval.")


def test_get_values_aggregated_start_later_than_end_raises_error(
        mock_query_manager: MagicMock,
) -> None:
    """Ensures ValueError is raised when start > end for aggregated queries."""
    with pytest.raises(
            ValueError,
            match="The 'start' datetime cannot be later than the 'end' datetime.",
    ):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 15, tzinfo=timezone.utc),
            end=datetime(2025, 1, 14, tzinfo=timezone.utc),
            aggregation_functions=["min"],
        )


def test_get_values_aggregated_start_or_end_not_timezone_aware_raises_error(
    mock_query_manager: MagicMock,
) -> None:
    """Checks that ValueError is raised if start or end is not tz aware."""
    with pytest.raises(ValueError, match="The start parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 14),  # no tzinfo  # noqa: DTZ001
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            aggregation_functions=["min"],
        )

    with pytest.raises(ValueError, match="The end parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15),  # no tzinfo  # noqa: DTZ001
            aggregation_functions=["min"],
        )

@pytest.mark.skip(reason="Need the right authorization to test the API")
def test_get_values_api() -> None:
    """Tests get_values by calling the real API (skipped unless authorized)."""
    domain = "foresight.piscada.cloud"
    query_manager = QueryManager(domain=domain,
                                 client_id="foresight-lib-py",
                                 client_secret=None,
                                 graphql_endpoint=None,
                                 json_serialize=None)
    result = get_values(
        query_manager=query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:0192576a-f715-72a9-826b-aa4d1c37882b",
        ],
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        aggregation_functions=["min", "max", "avg", "count", "last"],
    )
    if not isinstance(result, pd.DataFrame):
        pytest.fail("The result should be a DataFrame.")
    if len(result) == 0:
        pytest.fail("The DataFrame should not be empty.")

    domain = "foresight.piscada.cloud"
    query_manager = QueryManager(domain=domain,
                                 client_id="foresight-lib-py",
                                 client_secret=None,
                                 graphql_endpoint=None,
                                 json_serialize=None)
    result = get_values(
        query_manager=query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:0192576a-f715-72a9-826b-aa4d1c37882b",
        ],
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
    )
    if not isinstance(result, pd.DataFrame):
        pytest.fail("The result should be a DataFrame.")
    if len(result) == 0:
        pytest.fail("The DataFrame should not be empty.")


@pytest.mark.skip(reason="Need the right authorization to test the API")
def test_get_values_api_wrong_entity_id() -> None:
    """Get_values with wrong entity ID."""
    domain = "foresight.piscada.cloud"
    query_manager = QueryManager(domain=domain,
                                 client_id="foresight-lib-py",
                                 client_secret=None,
                                 graphql_endpoint=None,
                                 json_serialize=None)
    with pytest.raises(RuntimeError):
        get_values(
            query_manager=query_manager,
            entity_ids=["wrong_id"],
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        )


@pytest.mark.skip(reason="Need the right authorization to test the API")
def test_get_latest_values() -> None:
    """Tests get_values by calling the real API (skipped unless authorized)."""
    domain = "foresight.piscada.cloud"
    query_manager = QueryManager(domain=domain,
                                 client_id="foresight-lib-py",
                                 client_secret=None,
                                 graphql_endpoint=None,
                                 json_serialize=None)
    result = get_value(
        query_manager=query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:0192576a-f715-72a9-826b-aa4d1c37882b",
            "brick:Supply_Air_Temperature_Sensor:0192576a-f715-72a9-826b-aa4d1c37882b",
        ],
    )
    if not isinstance(result, list):
        pytest.fail("Result of get_value should be a list.")
    if not result[0]:
        pytest.fail("The result of get_value should not be empty.")

    result = get_value(
        query_manager=query_manager,
        entity_ids="brick:Supply_Air_Temperature_Sensor:0192576a-f715-72a9-826b-aa4d1c37882b",
    )
    if not isinstance(result, float):
        pytest.fail("Result of get_value should be a float.")

