"""Preservation-first raw RemNote document models.

These models form the typed boundary between loaded JSON export data and later
graph construction. They expose common RemNote fields while keeping the original
record and all unknown fields available for future migration improvements.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from remnote2obsidian.models.json import JsonArray, JsonObject, JsonValue


RAW_REM_KNOWN_FIELDS = frozenset(
    {
        "_id",
        "parent",
        "children",
        "subBlocks",
        "key",
        "value",
        "type",
        "references",
        "portalsIn",
        "searchResults",
    }
)

RAW_CARD_KNOWN_FIELDS = frozenset(
    {
        "_id",
        "rId",
        "c",
        "ml",
        "createdAt",
        "st",
        "e",
        "n",
        "p",
        "u",
        "m",
        "o",
        "y",
        "z",
    }
)

RAW_CARD_SCHEDULING_FIELDS = frozenset(
    {
        "c",
        "ml",
        "createdAt",
        "st",
        "e",
        "n",
        "p",
        "u",
        "m",
        "o",
        "y",
        "z",
    }
)


@dataclass(frozen=True, slots=True)
class RawRemDocument:
    """Raw RemNote `rem.json` document with known and unknown fields preserved."""

    rem_id: str | None
    parent: str | None = None
    children: tuple[str, ...] = ()
    sub_blocks: tuple[str, ...] = ()
    key: JsonArray | None = None
    value: JsonArray | None = None
    rem_type: JsonValue = None
    references: JsonValue = None
    portals_in: JsonValue = None
    search_results: JsonValue = None
    raw: JsonObject = field(default_factory=dict)
    unknown_fields: JsonObject = field(default_factory=dict)

    @classmethod
    def from_json(cls, record: JsonObject) -> RawRemDocument:
        """Create a raw Rem model from a JSON object without normalizing `raw`."""
        return cls(
            rem_id=_optional_string(record.get("_id")),
            parent=_optional_string(record.get("parent")),
            children=_string_tuple(record.get("children")),
            sub_blocks=_string_tuple(record.get("subBlocks")),
            key=_optional_array(record.get("key")),
            value=_optional_array(record.get("value")),
            rem_type=record.get("type"),
            references=record.get("references"),
            portals_in=record.get("portalsIn"),
            search_results=record.get("searchResults"),
            raw=record,
            unknown_fields=_unknown_fields(record, RAW_REM_KNOWN_FIELDS),
        )


@dataclass(frozen=True, slots=True)
class RawCardMetadata:
    """Raw `cards.json` metadata linked to a RemNote document by `rId`."""

    card_id: str | None
    rem_id: str | None
    scheduling_fields: JsonObject = field(default_factory=dict)
    raw: JsonObject = field(default_factory=dict)
    unknown_fields: JsonObject = field(default_factory=dict)

    @classmethod
    def from_json(cls, record: JsonObject) -> RawCardMetadata:
        """Create raw card metadata while preserving scheduling and unknown data."""
        return cls(
            card_id=_optional_string(record.get("_id")),
            rem_id=_optional_string(record.get("rId")),
            scheduling_fields={
                key: value for key, value in record.items() if key in RAW_CARD_SCHEDULING_FIELDS
            },
            raw=record,
            unknown_fields=_unknown_fields(record, RAW_CARD_KNOWN_FIELDS),
        )


def _optional_string(value: JsonValue) -> str | None:
    """Return a string value or `None` for non-string and missing fields."""
    if isinstance(value, str):
        return value
    return None


def _optional_array(value: JsonValue) -> JsonArray | None:
    """Return an array value or `None` for non-array and missing fields."""
    if isinstance(value, list):
        return value
    return None


def _string_tuple(value: JsonValue) -> tuple[str, ...]:
    """Return string members from a RemNote relationship field."""
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def _unknown_fields(record: JsonObject, known_fields: frozenset[str]) -> JsonObject:
    """Return fields not explicitly modeled by the raw data class."""
    return {key: value for key, value in record.items() if key not in known_fields}
