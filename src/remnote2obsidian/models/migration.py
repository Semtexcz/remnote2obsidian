"""Migration service request and summary models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MigrationRequest:
    """Inputs for a RemNote to Obsidian migration run."""

    export_directory: Path
    output_directory: Path
    dry_run: bool = False


@dataclass(frozen=True, slots=True)
class MigrationSummary:
    """Deterministic summary of a migration service run."""

    dry_run: bool
    loaded_file_count: int = 0
    rem_count: int = 0
    graph_node_count: int = 0
    markdown_document_count: int = 0
    written_markdown_count: int = 0
    ai_context_written: bool = False

    @property
    def planned_output_count(self) -> int:
        """Return the number of output files that would be or were generated."""
        return self.markdown_document_count + 1
