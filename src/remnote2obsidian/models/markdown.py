"""Markdown output models for Obsidian vault generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarkdownDocument:
    """A rendered Markdown document with a vault-relative output path."""

    rem_id: str
    relative_path: str
    content: str


@dataclass(frozen=True, slots=True)
class MarkdownPathMap:
    """Mapping from original RemNote IDs to vault-relative Markdown paths."""

    paths_by_rem_id: dict[str, str]

    def path_for_rem(self, rem_id: str) -> str | None:
        """Return the Markdown path for a RemNote ID when available."""
        return self.paths_by_rem_id.get(rem_id)
