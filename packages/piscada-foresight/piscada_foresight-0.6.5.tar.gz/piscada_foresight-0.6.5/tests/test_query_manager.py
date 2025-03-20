"""Test cases for QueryManager functionality."""

import pytest
from graphql import parse, print_ast

from piscada_foresight.queries_templates.query_manager import QueryManager
from tests.utils.test_utils import load_file_content


def test_singleton_behavior() -> None:
    """Ensure that QueryManager is a singleton.

    Create two instances with different domains and verify that they refer
    to the same instance.
    """
    qm1 = QueryManager(domain="domain1",
                       client_id=None,
                       client_secret=None,
                       graphql_endpoint=None,
                       json_serialize=None,
                       )
    qm2 = QueryManager(domain="domain2",
                       client_id=None,
                       client_secret=None,
                       graphql_endpoint=None,
                       json_serialize=None,
                       )
    if qm1 is not qm2:
        pytest.fail(
            "QueryManager should return the same instance regardless of "
            "constructor args.",
        )


def test_load_queries_build_dict() -> None:
    """Test that _load_queries populates the _query_dict.

    The query dictionary should match the expected values and contain
    required keys.
    """
    qm = QueryManager(domain="fake_domain",
                      client_id=None,
                      client_secret=None,
                      graphql_endpoint=None,
                      json_serialize=None,
                      )
    qdict = qm.query_handler.query_dict

    expected_dict = {
        "get_aggregated_values": "graphql_queries/timeseries/"
                                "get_aggregated_values.j2",
        "get_domains": "graphql_queries/domains/get_domains.graphql",
        "get_latest_value": "graphql_queries/timeseries/"
                            "get_latest_value.j2",
        "get_raw_values": "graphql_queries/timeseries/"
                          "get_raw_values.j2",
        "get_latest_values": "graphql_queries/timeseries/"
                          "get_latest_values.j2",
    }
    if qdict != expected_dict:
        pytest.fail("The query dictionary does not match the expected values.")

    for key in expected_dict:
        if key not in qdict:
            pytest.fail(f"Key '{key}' is missing from the query dictionary.")


def test_load_query_not_found() -> None:
    """If a non-existent query is requested, a ValueError should be raised.

    This ensures that queries missing from _query_dict trigger an exception.
    """
    qm = QueryManager(domain="fake_domain",
                      client_id=None,
                      client_secret=None,
                      graphql_endpoint=None,
                      json_serialize=None,
                      )
    with pytest.raises(
        ValueError,
        match=("Query 'does_not_exist' not found in query_dict"),
    ):
        qm.load_query("does_not_exist", {})


def test_load_query_j2() -> None:
    """Test loading a Jinja (.j2) query file.

    Ensure that the final query text is correctly rendered from the Jinja
    environment.
    """
    qm = QueryManager(domain="fake_domain",
                      client_id=None,
                      client_secret=None,
                      graphql_endpoint=None,
                      json_serialize=None,
                      )
    entity_ids = [0, 1]
    entity_variables = {
        f"entityId_{i}": entity_id
        for i, entity_id in enumerate(entity_ids)
    }
    jinja_dict = {"variable_names": list(entity_variables.keys())}
    rendered_text = qm.load_query("get_raw_values", jinja_dict)
    expected_text = load_file_content("assert_results/rendered_jinja_raw.graphql")

    rendered_ast = parse(rendered_text)
    expected_ast = parse(expected_text)

    rendered_normalized = print_ast(rendered_ast)
    expected_normalized = print_ast(expected_ast)

    if rendered_normalized != expected_normalized:
        pytest.fail("The rendered GraphQL query does not match the expected output.")


def test_load_query_graphql() -> None:
    """Loading a .graphql returns its contents directly (no rendering).

    This confirms that GraphQL queries are loaded as raw text.

    """
    qm = QueryManager(domain="fake_domain",
                      client_id=None,
                      client_secret=None,
                      graphql_endpoint=None,
                      json_serialize=None,
                      )
    query_text = qm.load_query("get_domains", {})
    expected_query = load_file_content(
        "../../src/piscada_foresight/queries_templates/"
        "graphql_queries/domains/get_domains.graphql",
    )
    if query_text != expected_query:
        pytest.fail("The loaded GraphQL query does not match the expected content.")
    if qm.query_handler.query_text != query_text:
        pytest.fail("QueryManager.query_text should store the loaded query text.")



def test_load_query_unsupported_extension() -> None:
    """Test ValueError is raised when loading an unsupported file.

    This is simulated by manually inserting an unsupported extension in the
    query dictionary.
    """
    qm = QueryManager(domain="fake_domain",
                      client_id=None,
                      client_secret=None,
                      graphql_endpoint=None,
                      json_serialize=None,
                      )
    qdict = qm.query_handler.query_dict
    qdict["bad_query"] = "folder/bad_query.txt"
    with pytest.raises(
        ValueError,
        match=("Unsupported query file type: 'folder/bad_query.txt'"),
    ):
        qm.load_query("bad_query", [])
