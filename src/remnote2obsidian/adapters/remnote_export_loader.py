"""Load supported JSON files from a RemNote export directory."""

from __future__ import annotations

from pathlib import Path

from remnote2obsidian.adapters.json_file import JsonFileAdapter
from remnote2obsidian.models import (
    OPTIONAL_EXPORT_FILENAMES,
    REQUIRED_EXPORT_FILENAME,
    Diagnostic,
    JsonValue,
    RemNoteExport,
    Result,
    SourceContext,
)


class RemNoteExportLoader:
    """Read raw supported files from a RemNote export directory."""

    def __init__(self, json_adapter: JsonFileAdapter | None = None) -> None:
        """Initialize the loader with an optional JSON adapter."""
        self._json_adapter = json_adapter or JsonFileAdapter()

    def load(self, export_directory: Path | str) -> Result[RemNoteExport]:
        """Load `rem.json` and present optional files from an export directory."""
        directory = Path(export_directory)
        loaded_files: dict[str, JsonValue] = {}
        diagnostics: list[Diagnostic] = []

        rem_path = directory / REQUIRED_EXPORT_FILENAME
        rem_result = self._json_adapter.read(rem_path)
        diagnostics.extend(rem_result.diagnostics)
        if rem_result.is_success:
            loaded_files[REQUIRED_EXPORT_FILENAME] = rem_result.data

        for filename in OPTIONAL_EXPORT_FILENAMES:
            file_path = directory / filename
            if not file_path.exists():
                continue

            file_result = self._json_adapter.read(file_path)
            diagnostics.extend(file_result.diagnostics)
            if file_result.is_success:
                loaded_files[filename] = file_result.data

        if not rem_path.exists() and not any(
            diagnostic.code == "json_file_missing" and diagnostic.source == SourceContext(str(rem_path))
            for diagnostic in diagnostics
        ):
            diagnostics.append(
                Diagnostic.error(
                    code="required_export_file_missing",
                    message=f"Required RemNote export file is missing: {rem_path}",
                    source=SourceContext(file_path=str(rem_path)),
                )
            )

        return Result(data=RemNoteExport(files=loaded_files), diagnostics=tuple(diagnostics))
