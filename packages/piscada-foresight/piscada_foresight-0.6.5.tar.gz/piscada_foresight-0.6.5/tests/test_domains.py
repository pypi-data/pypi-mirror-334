"""Test suite for the domains module of piscada foresight.

This module includes tests for domain validation, retrieving domains, traits,
and relationships.
"""

import json
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from piscada_foresight.domains import (
    _validate_domains,
    get_domains,
    get_parent_traits,
    get_trait_by_id,
)
from piscada_foresight.model import Trait

# Load the JSON response used in tests
DOMAINS_RESPONSE = json.load((Path(__file__).parent / "domains_response.json").open())


def test_get_domains_count(mocker: MockerFixture) -> None:
    """Test that the correct number of domains is retrieved from the mock client."""
    mock_client = mocker.Mock()
    mock_client.run_query.return_value = DOMAINS_RESPONSE["data"]
    domains = get_domains(mock_client)

    if len(domains) != 16:  # noqa: PLR2004
        pytest.fail("Expected 16 domains, found a different number.")


def test_get_domains_brick_domain(mocker: MockerFixture) -> None:
    """Test that the Brick domain has the correct name, prefix, and URI."""
    mock_client = mocker.Mock()
    mock_client.run_query.return_value = DOMAINS_RESPONSE["data"]
    domains = get_domains(mock_client)

    brick_domain = domains[2]
    if brick_domain.name != "Brick":
        pytest.fail('Expected the third domain to have name "Brick".')
    if brick_domain.prefix != "brick":
        pytest.fail('Expected prefix to be "brick".')
    if brick_domain.uri != "https://brickschema.org/schema/Brick#":
        pytest.fail('Expected URI to be "https://brickschema.org/schema/Brick#".')


def test_get_domains_brick_traits(mocker: MockerFixture) -> None:
    """Test that specific traits within the Brick domain match expected values."""
    mock_client = mocker.Mock()
    mock_client.run_query.return_value = DOMAINS_RESPONSE["data"]
    domains = get_domains(mock_client)

    brick_domain = domains[2]
    # Check Access_Control_Equipment trait
    ace_trait = brick_domain.traits[2]
    if ace_trait.id != "brick:Access_Control_Equipment":
        pytest.fail('Expected trait ID to be "brick:Access_Control_Equipment".')
    if ace_trait.parent_ids != ["brick:Security_Equipment"]:
        pytest.fail('Expected parent IDs to be ["brick:Security_Equipment"].')
    if ace_trait.child_ids != ["brick:Access_Reader"]:
        pytest.fail('Expected child IDs to be ["brick:Access_Reader"].')

    # Check AHU trait
    ahu_trait = brick_domain.traits[6]
    if ahu_trait.id != "brick:AHU":
        pytest.fail('Expected trait ID to be "brick:AHU".')
    expected_equiv = ["brick:Air_Handler_Unit", "brick:Air_Handling_Unit"]
    if ahu_trait.equivalent_ids != expected_equiv:
        pytest.fail(f"Expected equivalent IDs to be {expected_equiv}.")


def test_get_domains_brick_relationships(mocker: MockerFixture) -> None:
    """Test that relationships within the Brick domain match expected values."""
    mock_client = mocker.Mock()
    mock_client.run_query.return_value = DOMAINS_RESPONSE["data"]
    domains = get_domains(mock_client)

    brick_domain = domains[2]
    feeds_rel = brick_domain.relationships[0]
    if feeds_rel.id != "brick:feeds":
        pytest.fail('Expected relationship ID to be "brick:feeds".')

    expected_parents = [
        "fs_navigation:breadcrumbProcessIncoming",
        "fs_navigation:Expert",
        "fs_navigation:moreDetailsOrOutgoing",
        "fs_navigation:outgoing",
        "fs_navigation:Semantic",
        "fs_schema:Association",
    ]
    if feeds_rel.parent_ids != expected_parents:
        pytest.fail(f"Expected parent IDs to be {expected_parents}.")

    if feeds_rel.child_ids != ["brick:feedsAir"]:
        pytest.fail('Expected child IDs to be ["brick:feedsAir"].')

    if feeds_rel.inverse_ids != ["brick:isFedBy"]:
        pytest.fail('Expected inverse IDs to be ["brick:isFedBy"].')


def test_get_trait_by_id() -> None:
    """Test retrieving a trait by ID from a domain using get_trait_by_id."""
    domains = _validate_domains(DOMAINS_RESPONSE["data"])
    if len(domains) != 16:  # noqa: PLR2004
        pytest.fail("Expected 16 domains, found a different number.")

    if domains[2].name != "Brick":
        pytest.fail('Expected the third domain to have name "Brick".')

    brick_domain = domains[2]
    retrieved_trait = brick_domain.get_trait_by_id("brick:Building")
    if retrieved_trait.name != "Building":
        pytest.fail('Expected the retrieved trait name to be "Building".')


def test_get_parent_traits() -> None:
    """Test retrieving parent traits from a domain using get_parent_traits."""
    domains = _validate_domains(DOMAINS_RESPONSE["data"])
    brick_domain = domains[2]
    trait = brick_domain.get_trait_by_id("brick:Air_Temperature_Sensor")
    parent_traits = get_parent_traits(trait, domains)

    expected_ids = {
        "brick:Air_Temperature_Sensor",
        "brick:Point",
        "brick:Sensor",
        "brick:Temperature_Sensor",
    }
    actual_ids = {t.id for t in parent_traits}
    if actual_ids != expected_ids:
        pytest.fail(f"Expected parent trait IDs {expected_ids}, got {actual_ids}.")


def test_get_trait_by_id_exceptions() -> None:
    """Test error handling for get_trait_by_id with missing traits or empty domains."""
    domains = _validate_domains(DOMAINS_RESPONSE["data"])
    brick_domain = domains[2]

    # Test with non-existent ID
    with pytest.raises(KeyError, match=r".*non:existent:id.*"):
        brick_domain.get_trait_by_id("non:existent:id")

    # Test with empty trait list
    empty_data = {
        "domainDefinitions": [
            {
                "name": "Empty",
                "prefix": "empty",
                "description": "Empty domain",
                "uri": "http://example.org/empty",
                "traits": None,
                "relationships": None,
            },
        ],
    }
    empty_domain = _validate_domains(empty_data)[0]
    with pytest.raises(KeyError, match=r".*any:id.*"):
        empty_domain.get_trait_by_id("any:id")


def test_get_parent_traits_exceptions() -> None:
    """Error handling for get_parent_traits, non-existent/cyclic references."""
    domains = _validate_domains(DOMAINS_RESPONSE["data"])
    brick_domain = domains[2]

    # Test with non-existent parent IDs
    trait_no_parents = brick_domain.get_trait_by_id("brick:Point")
    parent_traits = get_parent_traits(trait_no_parents, domains)
    if len(parent_traits) != 1:
        pytest.fail("Expected 1 parent trait, found a different number.")
    if parent_traits[0].id != "brick:Point":
        pytest.fail('Expected parent trait ID to be "brick:Point".')

    # Test with cyclic parent references
    cyclic_data = {
        "domainDefinitions": [
            {
                "name": "Cyclic",
                "prefix": "cyclic",
                "description": "Cyclic domain",
                "uri": "http://example.org/cyclic",
                "traits": [
                    {
                        "name": "Trait1",
                        "id": "cyclic:trait1",
                        "parent_ids": [{"id": "cyclic:trait2"}],
                        "child_ids": [],
                        "equivalent_ids": [],
                        "domain_prefix": {"prefix": "cyclic"},
                    },
                    {
                        "name": "Trait2",
                        "id": "cyclic:trait2",
                        "parent_ids": [{"id": "cyclic:trait1"}],
                        "child_ids": [],
                        "equivalent_ids": [],
                        "domain_prefix": {"prefix": "cyclic"},
                    },
                ],
                "relationships": None,
            },
        ],
    }
    cyclic_domain = _validate_domains(cyclic_data)[0]
    with pytest.raises(RecursionError):
        get_parent_traits(
            cyclic_domain.get_trait_by_id("cyclic:trait1"),
            [cyclic_domain],
        )

    # Test with None parent_ids
    trait_dict = {
        "name": "NoParents",
        "id": "test:no_parents",
        "parent_ids": None,
        "child_ids": [],
        "equivalent_ids": [],
        "domain_prefix": {"prefix": "test"},
    }
    no_parent_trait = Trait.model_validate(trait_dict)
    parent_traits = get_parent_traits(no_parent_trait, brick_domain)
    if len(parent_traits) != 1:
        pytest.fail(
            "Expected 1 parent trait with None parent_ids, found a different number.",
        )
    if parent_traits[0].id != "test:no_parents":
        pytest.fail('Expected the trait ID to be "test:no_parents".')


def test_get_trait_by_id_with_domains() -> None:
    """Test retrieving a trait by ID from a list of domains using get_trait_by_id."""
    domains = _validate_domains(DOMAINS_RESPONSE["data"])
    trait = get_trait_by_id("brick:Building", domains)
    if trait.name != "Building":
        pytest.fail('Expected the retrieved trait name to be "Building".')

    # Test with non-existent ID across domains
    with pytest.raises(ValueError, match=r".*nonexistent:id.*"):
        get_trait_by_id("nonexistent:id", domains)

    # Test with empty domain list
    with pytest.raises(ValueError, match=r".*any:id.*"):
        get_trait_by_id("any:id", [])

    # Test with None domain list
    with pytest.raises(TypeError, match=r".*None.*"):
        get_trait_by_id("any:id", None)

    # Test with invalid domain data
    invalid_domains = [None, "not a domain", 123]
    with pytest.raises(AttributeError):
        get_trait_by_id("any:id", invalid_domains)
