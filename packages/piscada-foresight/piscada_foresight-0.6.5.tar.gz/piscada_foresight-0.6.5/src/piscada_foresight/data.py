"""Access to Foresight timeseries data."""

import logging
import re
from datetime import datetime, timezone
from json import loads
from uuid import UUID

from pandas import DataFrame, to_datetime

from piscada_foresight.parser_graphql_to_df. \
    time_series.timeseries_response_parser import TimeseriesResponseParser
from piscada_foresight.queries_templates.query_manager import QueryManager

log = logging.getLogger(__name__)


def get_value(
        query_manager: QueryManager,
        entity_ids: UUID | list[UUID],
        moment: datetime | None = None,
        ) -> float|list[float]:
    """Retrieve the latest value of a `foresight:Datapoint` entity."""
    if not moment:
        moment = datetime.now(tz=timezone.utc)
    if isinstance(entity_ids, UUID|str):
        variables = {"entityId": entity_ids, "eventTime": moment.isoformat()}
        response = query_manager.run_query("get_latest_value",
                                           query_variables=variables,
                                           )
        try:
            return float(
                response["entity"]["trait"]["quantity"]["value"]["value"],
            )
        except KeyError as err:
            msg = "Cloud not retrieve value."
            raise RuntimeError(msg) from err
        except ValueError as exc:
            val_str = response["entity"]["trait"]["quantity"]["value"]["value"]
            msg = f"Could not parse value {val_str}"
            raise RuntimeError(msg) from exc

    # For multiple entities
    entity_variables = {
        f"entityId_{i}": str(e) for i, e in enumerate(entity_ids)
    }
    jinja_dict = {
        "variable_names": list(entity_variables.keys()),
    }
    query_variables = {
        **entity_variables, "eventTime": moment.isoformat(),
    }

    response = query_manager.run_query("get_latest_values",
                                       jinja_variables=jinja_dict,
                                       query_variables=query_variables,
                                       )
    results: list[float] = []
    for var_name in jinja_dict["variable_names"]:
        entity = response.get(var_name)
        if entity:
            try:
                value = float(entity["trait"]["quantity"]["value"]["value"])
                results.append(value)
            except KeyError as err:
                msg = f"Could not retrieve value for entity {
                entity.get('id', 'unknown')
                }."
                raise RuntimeError(msg) from err
            except ValueError as exc:
                val_str = entity["trait"]["quantity"]["value"]["value"]
                msg = f"Could not parse value {val_str} for entity {
                entity.get('id', 'unknown')
                }."
                raise RuntimeError(msg) from exc
    return results

def get_raw_timeseries(
    query_manager: QueryManager,
    entity_ids: list[str],
    start: datetime,
    end: datetime | None = None,
) -> DataFrame:
    """Retrieve values of `foresight:Datapoint` entities for a time range."""
    if end is None:
        end = datetime.now(tz=timezone.utc)
    if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
        msg = "The start parameter must be timezone aware."
        raise ValueError(msg)
    if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
        msg = "The end parameter must be timezone aware."
        raise ValueError(msg)
    if start > end:
        msg = "The 'start' datetime cannot be later than the 'end' datetime."
        raise ValueError(
            msg,
        )

    entity_variables = {
        f"entityId_{i}": entity_id for i, entity_id in enumerate(entity_ids)
    }
    jinja_dict = {}
    jinja_dict["variable_names"] = list(entity_variables.keys())
    variables = {
        **entity_variables,
        "startEventTime": start.isoformat(),
        "endEventTime": end.isoformat(),
    }

    response = query_manager.run_query(
        "get_raw_values",
        jinja_variables=jinja_dict,
        query_variables=variables,
    )

    parser = TimeseriesResponseParser()
    return parser.parse(response, entity_variables, start, end, query_type="raw")


def get_aggregated_timeseries(  # noqa: PLR0913
    query_manager: QueryManager,
    entity_ids: list[str],
    start: datetime,
    end: datetime | None = None,
    interval: str = "",
    aggregation_functions: list[str] | None = None,
) -> DataFrame:
    """Retrieve agg values of `foresight:Datapoint` entities for a given time range."""
    if end is None:
        end = datetime.now(tz=timezone.utc)
    if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
        msg = "The start parameter must be timezone aware."
        raise ValueError(msg)
    if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
        msg = "The end parameter must be timezone aware."
        raise ValueError(msg)
    if start > end:
        msg = "The 'start' datetime cannot be later than the 'end' datetime."
        raise ValueError(
            msg,
        )

    if aggregation_functions is None:
        aggregation_functions = []

    # The values are "most likely" cached/saved. (1y is the max interval)
    if interval == "":
        interval = "1y"

    valid_aggregators = {"min", "max", "avg", "count", "last"}
    if not all(func in valid_aggregators for func in aggregation_functions):
        msg = (
            f"Invalid aggregation function provided. "
            f"Only the following are allowed: {valid_aggregators}"
        )
        raise ValueError(
            msg,
        )

    entity_variables = {
        f"entityId_{i}": entity_id for i, entity_id in enumerate(entity_ids)
    }

    query_variables = {
        **entity_variables,
        "startEventTime": start.isoformat(),
        "endEventTime": end.isoformat(),
        "interval": interval,
        "aggregationFunctions": aggregation_functions,
    }

    jinja_dict = {
        "variable_names": list(entity_variables.keys()),
    }
    response = query_manager.run_query(
        "get_aggregated_values",
        jinja_variables=jinja_dict,
        query_variables=query_variables,
    )
    parser = TimeseriesResponseParser()
    return parser.parse(response, entity_variables, start, end, query_type="aggregated")


def get_values(  # noqa: PLR0913
    query_manager: QueryManager,
    entity_ids: list[str],
    start: datetime,
    end: datetime | None = None,
    interval: str = "",
    aggregation_functions: list[str] | None = None,
) -> DataFrame:
    """Dispatches either to raw or aggregated timeseries."""
    if not aggregation_functions:
        return get_raw_timeseries(query_manager, entity_ids, start, end)
    return get_aggregated_timeseries(
        query_manager, entity_ids, start, end, interval, aggregation_functions,
    )


def get_all_values(text: str) -> list[DataFrame]:
    """Extract all pairs of id, name, and values from a GraphQL query."""
    values_regex = re.compile(
        r"'id'\:\s*'([\:\w\s\-_]*?)',\s*'name'\:\s*'([\w\s\-_]*?)',\s*'trait':\s*{'quantity'\:\s*\{'values'\:\s*\[([\{'\w\:\-\s\.\},]*)",
    )
    dfs = []
    for match in values_regex.findall(text):
        eid = match[0].split(":")[-1]
        name = match[1]
        # Convert single quotes to double quotes for JSON parsing
        values_str = f"[{match[2]}]".replace("'", '"')

        parsed_values = loads(values_str)
        data = [
            {"ts": item["eventTime"], f"{name}|{eid}": float(item["value"])}
            for item in parsed_values
        ]
        df_values = DataFrame(data).set_index("ts")
        df_values.index = to_datetime(df_values.index, format="ISO8601")
        dfs.append(df_values)

    return dfs
