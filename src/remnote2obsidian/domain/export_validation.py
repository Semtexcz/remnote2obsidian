"""Validate loaded RemNote export envelopes."""

from __future__ import annotations

from remnote2obsidian.models import (
    Diagnostic,
    JsonObject,
    RemNoteExport,
    Result,
    SHARED_ENVELOPE_FILENAMES,
    SourceContext,
)


def validate_export_envelope(export_data: RemNoteExport) -> Result[RemNoteExport]:
    """Validate top-level RemNote export file envelope shapes."""
    diagnostics: list[Diagnostic] = []

    for filename in SHARED_ENVELOPE_FILENAMES:
        if filename not in export_data.files:
            continue

        file_data = export_data.files[filename]
        source = SourceContext(file_path=filename)
        if not isinstance(file_data, dict):
            diagnostics.append(
                Diagnostic.error(
                    code="export_envelope_not_object",
                    message=f"{filename} must contain a top-level JSON object.",
                    source=source,
                )
            )
            continue

        diagnostics.extend(_validate_shared_envelope(filename, file_data, source))

    if "metadata.json" in export_data.files:
        metadata = export_data.files["metadata.json"]
        if not isinstance(metadata, dict):
            diagnostics.append(
                Diagnostic.error(
                    code="metadata_envelope_not_object",
                    message="metadata.json must contain a top-level JSON object.",
                    source=SourceContext(file_path="metadata.json"),
                )
            )

    return Result(data=export_data, diagnostics=tuple(diagnostics))


def _validate_shared_envelope(
    filename: str,
    file_data: JsonObject,
    source: SourceContext,
) -> tuple[Diagnostic, ...]:
    """Validate the shared RemNote export envelope used by most files."""
    diagnostics: list[Diagnostic] = []

    if "docs" not in file_data:
        diagnostics.append(
            Diagnostic.error(
                code="export_envelope_docs_missing",
                message=f"{filename} is missing required top-level `docs`.",
                source=source,
            )
        )
        return tuple(diagnostics)

    if not isinstance(file_data["docs"], list):
        diagnostics.append(
            Diagnostic.error(
                code="export_envelope_docs_not_list",
                message=f"{filename} top-level `docs` must be a list.",
                source=source,
            )
        )

    return tuple(diagnostics)
