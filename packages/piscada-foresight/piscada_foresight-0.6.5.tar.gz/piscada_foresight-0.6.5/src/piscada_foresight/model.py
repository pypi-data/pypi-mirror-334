"""Define models for domains, traits, and relationships.

Used in the Piscada Foresight project.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator


class Relationship(BaseModel):
    """Model representing a relationship between entities in a domain.

    Contains information about the hierarchy of relationships (parents/children)
    and inverse relationships.
    """

    name: str
    id: str
    parent_ids: List[str]
    child_ids: List[str]
    inverse_ids: List[str]
    domain_prefix: str

    @field_validator("domain_prefix", mode="before")
    @classmethod
    def extract_domain_prefix(cls, value: Dict[str, str]) -> Optional[str]:
        """Extract the domain prefix from a dict containing a 'prefix' key."""
        return value["prefix"] if value else None

    @field_validator("parent_ids", mode="before")
    @classmethod
    def extract_parent_ids(cls, value: List[Dict[str, str]]) -> List[str]:
        """Extract a list of parent ids from a list of dictionaries."""
        return [e["id"] for e in value] if value else []

    @field_validator("child_ids", mode="before")
    @classmethod
    def extract_child_ids(cls, value: List[Dict[str, str]]) -> List[str]:
        """Extract a list of child ids from a list of dictionaries."""
        return [e["id"] for e in value] if value else []

    @field_validator("inverse_ids", mode="before")
    @classmethod
    def extract_inverse_ids(cls, value: Dict[str, str]) -> List[str]:
        """Extract the inverse id from a dict and return it as a list."""
        return [value["id"]] if value else []


class Trait(BaseModel):
    """Model representing a trait that can be assigned to entities.

    Contains hierarchical information about parent/child relationships and
    equivalent traits.
    """

    name: str
    id: str
    domain_prefix: str
    parent_ids: List[str]
    child_ids: List[str]
    equivalent_ids: List[str]

    @field_validator("domain_prefix", mode="before")
    @classmethod
    def extract_domain_prefix(cls, value: Dict[str, str]) -> str|None:
        """Extract the domain prefix from a dict containing a 'prefix' key."""
        return value["prefix"] if value else None

    @field_validator("parent_ids", mode="before")
    @classmethod
    def extract_parent_ids(cls, value: list[dict[str, str]]) -> list[str]:
        """Extract a list of parent ids from a list of dictionaries."""
        return [e["id"] for e in value] if value else []

    @field_validator("child_ids", mode="before")
    @classmethod
    def extract_child_ids(cls, value: list[dict[str, str]]) -> list[str]:
        """Extract a list of child ids from a list of dictionaries."""
        return [e["id"] for e in value] if value else []

    @field_validator("equivalent_ids", mode="before")
    @classmethod
    def extract_equivalent_ids(cls, value: list[dict[str, str]]) -> list[str]:
        """Extract a list of equivalent trait ids from a list of dictionaries."""
        return [e["id"] for e in value] if value else []


class Domain(BaseModel):
    """Model representing a domain containing traits and relationships.

    A domain defines a namespace of traits and relationships that can be
    used to describe entities.
    """

    name: str
    prefix: str
    description: Optional[str]
    uri: str
    traits: List[Trait]
    relationships: List[Relationship]

    @field_validator("traits", mode="before")
    @classmethod
    def validate_traits(cls, value: object) -> list[Any]:
        """Ensure the traits field is valid, or return an empty list."""
        return  value if isinstance(value, list) else []

    @field_validator("relationships", mode="before")
    @classmethod
    def validate_relationships(cls, value: object) -> list[Any]:
        """Ensure the relationships field is valid, or return an empty list."""
        return  value if isinstance(value, list) else []

    def __init__(self, **data: object) -> None:
        """Initialize a Domain instance.

        Passes all keyword data to the base initializer and creates a trait
        lookup dictionary mapping each trait's id to its object.

        Parameters
        ----------
        **data : object
            Arbitrary keyword arguments.

        """
        super().__init__(**data)
        self._trait_dict = (
            {trait.id: trait for trait in self.traits} if self.traits else {}
        )

    def get_trait_by_id(self, id_str: str) -> Trait:
        """Retrieve a trait by its identifier.

        Parameters
        ----------
        id_str : str
            The unique identifier of the trait.

        Returns
        -------
        Trait
            The Trait object matching the given identifier.

        """
        return self._trait_dict[id_str]
