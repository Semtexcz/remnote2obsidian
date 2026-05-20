"""Preservation-first RemNote rich text fragment models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from remnote2obsidian.models.json import JsonValue


class RichTextFragmentKind(StrEnum):
    """Known rich text fragment categories."""

    TEXT = "text"
    REFERENCE = "reference"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class RichTextFragment:
    """A parsed RemNote rich text fragment with raw data preserved."""

    kind: RichTextFragmentKind
    text: str | None = None
    target_rem_id: str | None = None
    raw: JsonValue = None

    @classmethod
    def text_fragment(cls, text: str) -> RichTextFragment:
        """Create a plain text fragment."""
        return cls(kind=RichTextFragmentKind.TEXT, text=text, raw=text)

    @classmethod
    def reference_fragment(cls, target_rem_id: str, raw: JsonValue) -> RichTextFragment:
        """Create a RemNote reference fragment."""
        return cls(
            kind=RichTextFragmentKind.REFERENCE,
            target_rem_id=target_rem_id,
            raw=raw,
        )

    @classmethod
    def unsupported_fragment(cls, raw: JsonValue) -> RichTextFragment:
        """Create a fragment for unsupported data that must remain inspectable."""
        return cls(kind=RichTextFragmentKind.UNSUPPORTED, raw=raw)
