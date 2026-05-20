"""Tests for RemNote rich text fragment parsing."""

from remnote2obsidian.domain import parse_rich_text_fragments
from remnote2obsidian.models import JsonObject, RichTextFragmentKind, SourceContext


def test_parse_rich_text_fragments_supports_plain_text() -> None:
    """Plain string fragments should become text fragments."""
    result = parse_rich_text_fragments(["Hello ", "world"])

    assert result.is_success
    assert result.data is not None
    assert tuple(fragment.kind for fragment in result.data) == (
        RichTextFragmentKind.TEXT,
        RichTextFragmentKind.TEXT,
    )
    assert tuple(fragment.text for fragment in result.data) == ("Hello ", "world")


def test_parse_rich_text_fragments_supports_references() -> None:
    """Observed RemNote reference objects should preserve target Rem IDs."""
    raw_reference: JsonObject = {"i": "q", "_id": "rem-target"}

    result = parse_rich_text_fragments(["See ", raw_reference])

    assert result.is_success
    assert result.data is not None
    assert result.data[1].kind == RichTextFragmentKind.REFERENCE
    assert result.data[1].target_rem_id == "rem-target"
    assert result.data[1].raw is raw_reference


def test_parse_rich_text_fragments_preserves_unsupported_fragments() -> None:
    """Unsupported fragment objects should be preserved and reported as warnings."""
    unsupported: JsonObject = {"content": {"imageUrl": "https://example.test/image.png"}}
    source = SourceContext(file_path="rem.json:docs[0]", rem_id="rem-1")

    result = parse_rich_text_fragments([unsupported], source=source)

    assert result.is_success
    assert result.data is not None
    assert result.data[0].kind == RichTextFragmentKind.UNSUPPORTED
    assert result.data[0].raw is unsupported
    assert result.warnings[0].code == "rich_text_fragment_unsupported"
    assert result.warnings[0].source == source


def test_parse_rich_text_fragments_accepts_single_string_value() -> None:
    """A single string value should be parsed as one text fragment."""
    result = parse_rich_text_fragments("Standalone text")

    assert result.is_success
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].text == "Standalone text"
