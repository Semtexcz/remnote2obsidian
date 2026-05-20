"""AI context models for migrated Obsidian vaults."""

from __future__ import annotations

from dataclasses import dataclass, field


AI_CONTEXT_MANIFEST_PATH = ".remnote2obsidian/manifest.json"


@dataclass(frozen=True, slots=True)
class AiManifestEntry:
    """Traceability metadata for one migrated RemNote graph node."""

    remnote_id: str
    markdown_path: str
    parent_id: str | None = None
    child_ids: tuple[str, ...] = ()
    reference_ids: tuple[str, ...] = ()
    attachment_count: int = 0
    card_count: int = 0


@dataclass(frozen=True, slots=True)
class AiManifest:
    """Machine-readable manifest for AI agents navigating generated vaults."""

    version: int = 1
    entries: tuple[AiManifestEntry, ...] = field(default_factory=tuple)

    def to_json_dict(self) -> dict[str, object]:
        """Return a deterministic JSON-serializable manifest dictionary."""
        return {
            "version": self.version,
            "entries": [
                {
                    "remnote_id": entry.remnote_id,
                    "markdown_path": entry.markdown_path,
                    "parent_id": entry.parent_id,
                    "child_ids": list(entry.child_ids),
                    "reference_ids": list(entry.reference_ids),
                    "attachment_count": entry.attachment_count,
                    "card_count": entry.card_count,
                }
                for entry in self.entries
            ],
        }
