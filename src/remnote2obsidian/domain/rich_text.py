"""Parse RemNote `key` and `value` rich text fragments."""

from __future__ import annotations

from remnote2obsidian.models import (
    Diagnostic,
    JsonObject,
    JsonValue,
    Result,
    RichTextFragment,
    RichTextFragmentKind,
    SourceContext,
)


def parse_rich_text_fragments(
    value: JsonValue,
    *,
    source: SourceContext | None = None,
) -> Result[tuple[RichTextFragment, ...]]:
    """Parse RemNote rich text data in a preservation-first format."""
    fragments: list[RichTextFragment] = []
    diagnostics: list[Diagnostic] = []
    source_context = source or SourceContext()

    for index, fragment_data in enumerate(_fragment_items(value)):
        fragment = _parse_fragment(fragment_data)
        fragments.append(fragment)

        if fragment.kind == RichTextFragmentKind.UNSUPPORTED:
            diagnostics.append(
                Diagnostic.warning(
                    code="rich_text_fragment_unsupported",
                    message=f"Unsupported rich text fragment at index {index} was preserved.",
                    source=source_context,
                )
            )

    return Result(data=tuple(fragments), diagnostics=tuple(diagnostics))


def _fragment_items(value: JsonValue) -> tuple[JsonValue, ...]:
    """Return normalized fragment items without changing each fragment payload."""
    if value is None:
        return ()
    if isinstance(value, list):
        return tuple(value)
    return (value,)


def _parse_fragment(fragment_data: JsonValue) -> RichTextFragment:
    """Parse one RemNote rich text fragment while preserving unsupported data."""
    if isinstance(fragment_data, str):
        return RichTextFragment.text_fragment(fragment_data)

    if isinstance(fragment_data, dict):
        target_rem_id = _reference_target_rem_id(fragment_data)
        if target_rem_id is not None:
            return RichTextFragment.reference_fragment(
                target_rem_id=target_rem_id,
                raw=fragment_data,
            )

    return RichTextFragment.unsupported_fragment(fragment_data)


def _reference_target_rem_id(fragment_data: JsonObject) -> str | None:
    """Return the target RemNote ID for an observed reference fragment shape."""
    target_rem_id = fragment_data.get("_id")
    if fragment_data.get("i") == "q" and isinstance(target_rem_id, str):
        return target_rem_id
    return None
