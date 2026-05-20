"""Tests for preservation-first raw RemNote models."""

from remnote2obsidian.models import JsonObject, RawCardMetadata, RawRemDocument


def test_raw_rem_document_preserves_known_and_unknown_fields() -> None:
    """Raw Rem models should expose common fields and retain unknown data."""
    record: JsonObject = {
        "_id": "rem-1",
        "parent": "rem-root",
        "children": ["rem-child"],
        "subBlocks": ["rem-sub-block"],
        "key": ["Question"],
        "value": ["Answer"],
        "type": 2,
        "references": ["rem-ref"],
        "portalsIn": ["portal-1"],
        "searchResults": ["search-1"],
        "customField": {"preserve": True},
    }

    raw_rem = RawRemDocument.from_json(record)

    assert raw_rem.rem_id == "rem-1"
    assert raw_rem.parent == "rem-root"
    assert raw_rem.children == ("rem-child",)
    assert raw_rem.sub_blocks == ("rem-sub-block",)
    assert raw_rem.key == ["Question"]
    assert raw_rem.value == ["Answer"]
    assert raw_rem.rem_type == 2
    assert raw_rem.references == ["rem-ref"]
    assert raw_rem.portals_in == ["portal-1"]
    assert raw_rem.search_results == ["search-1"]
    assert raw_rem.raw is record
    assert raw_rem.unknown_fields == {"customField": {"preserve": True}}


def test_raw_rem_document_tolerates_missing_optional_fields() -> None:
    """Raw Rem models should allow sparse records for diagnostic-first parsing."""
    raw_rem = RawRemDocument.from_json({"_id": "rem-1"})

    assert raw_rem.rem_id == "rem-1"
    assert raw_rem.parent is None
    assert raw_rem.children == ()
    assert raw_rem.key is None
    assert raw_rem.unknown_fields == {}


def test_raw_card_metadata_preserves_rem_id_and_scheduling_fields() -> None:
    """Raw card metadata should retain the `rId` link and scheduling data."""
    record: JsonObject = {
        "_id": "card-1",
        "rId": "rem-1",
        "c": "f",
        "ml": "New",
        "st": 1779235200000,
        "customCardField": "preserve",
    }

    card = RawCardMetadata.from_json(record)

    assert card.card_id == "card-1"
    assert card.rem_id == "rem-1"
    assert card.scheduling_fields == {
        "c": "f",
        "ml": "New",
        "st": 1779235200000,
    }
    assert card.raw is record
    assert card.unknown_fields == {"customCardField": "preserve"}
