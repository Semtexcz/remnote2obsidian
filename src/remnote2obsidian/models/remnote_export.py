"""Raw RemNote export data models."""

from __future__ import annotations

from dataclasses import dataclass, field

from remnote2obsidian.models.json import JsonValue


REQUIRED_EXPORT_FILENAME = "rem.json"

OPTIONAL_EXPORT_FILENAMES = (
    "cards.json",
    "metadata.json",
    "user_data.json",
    "knowledge_base_data.json",
    "knowledgebase_local_stored_data.json",
    "local_stored_data.json",
    "spaced_repetition_scheduler.json",
)

SUPPORTED_EXPORT_FILENAMES = (REQUIRED_EXPORT_FILENAME, *OPTIONAL_EXPORT_FILENAMES)

SHARED_ENVELOPE_FILENAMES = tuple(
    filename for filename in SUPPORTED_EXPORT_FILENAMES if filename != "metadata.json"
)


@dataclass(frozen=True, slots=True)
class RemNoteExport:
    """Raw JSON data loaded from supported RemNote export files."""

    files: dict[str, JsonValue] = field(default_factory=dict)

    @property
    def rem(self) -> JsonValue | None:
        """Return raw `rem.json` data when it was loaded."""
        return self.files.get(REQUIRED_EXPORT_FILENAME)

    def has_file(self, filename: str) -> bool:
        """Return whether a supported export file was loaded."""
        return filename in self.files
