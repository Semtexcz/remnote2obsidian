"""Orchestrate the RemNote to Obsidian migration workflow."""

from __future__ import annotations

from dataclasses import replace

from remnote2obsidian.adapters import AiContextWriter, ObsidianVaultWriter, RemNoteExportLoader
from remnote2obsidian.domain import (
    build_rem_graph,
    generate_ai_manifest,
    generate_markdown_paths,
    parse_raw_card_metadata,
    parse_raw_rem_documents,
    render_markdown_documents,
    validate_export_envelope,
)
from remnote2obsidian.models import (
    Diagnostic,
    JsonObject,
    MigrationRequest,
    MigrationSummary,
    RemNoteExport,
    Result,
)


class MigrationService:
    """Coordinate loading, parsing, rendering, and output writing."""

    def __init__(
        self,
        export_loader: RemNoteExportLoader | None = None,
        vault_writer: ObsidianVaultWriter | None = None,
        ai_context_writer: AiContextWriter | None = None,
    ) -> None:
        """Initialize the service with optional adapter overrides."""
        self._export_loader = export_loader or RemNoteExportLoader()
        self._vault_writer = vault_writer or ObsidianVaultWriter()
        self._ai_context_writer = ai_context_writer or AiContextWriter()

    def migrate(self, request: MigrationRequest) -> Result[MigrationSummary]:
        """Run the migration pipeline and return a summary plus diagnostics."""
        diagnostics: list[Diagnostic] = []
        summary = MigrationSummary(dry_run=request.dry_run)

        load_result = self._export_loader.load(request.export_directory)
        diagnostics.extend(load_result.diagnostics)
        export = load_result.data or RemNoteExport()
        summary = replace(summary, loaded_file_count=len(export.files))
        if _has_errors(diagnostics):
            return Result(data=summary, diagnostics=tuple(diagnostics))

        validation_result = validate_export_envelope(export)
        diagnostics.extend(validation_result.diagnostics)
        if _has_errors(diagnostics):
            return Result(data=summary, diagnostics=tuple(diagnostics))

        rem_data = export.files.get("rem.json")
        if not isinstance(rem_data, dict):
            diagnostics.append(
                Diagnostic.error(
                    code="migration_rem_envelope_missing",
                    message="Loaded export does not contain a valid rem.json object.",
                )
            )
            return Result(data=summary, diagnostics=tuple(diagnostics))

        rem_parse_result = parse_raw_rem_documents(rem_data)
        diagnostics.extend(rem_parse_result.diagnostics)
        raw_rems = rem_parse_result.data or ()
        summary = replace(summary, rem_count=len(raw_rems))
        if _has_errors(diagnostics):
            return Result(data=summary, diagnostics=tuple(diagnostics))

        card_parse_result = parse_raw_card_metadata(_optional_object(export.files.get("cards.json")))
        diagnostics.extend(card_parse_result.diagnostics)
        raw_cards = card_parse_result.data or ()
        if _has_errors(diagnostics):
            return Result(data=summary, diagnostics=tuple(diagnostics))

        graph_result = build_rem_graph(raw_rems, raw_cards)
        diagnostics.extend(graph_result.diagnostics)
        graph = graph_result.data
        if graph is None:
            return Result(data=summary, diagnostics=tuple(diagnostics))

        path_result = generate_markdown_paths(graph)
        diagnostics.extend(path_result.diagnostics)
        path_map = path_result.data
        if path_map is None:
            return Result(data=summary, diagnostics=tuple(diagnostics))

        markdown_result = render_markdown_documents(graph)
        diagnostics.extend(markdown_result.diagnostics)
        documents = markdown_result.data or ()
        manifest_result = generate_ai_manifest(graph, path_map)
        diagnostics.extend(manifest_result.diagnostics)
        manifest = manifest_result.data

        summary = replace(
            summary,
            graph_node_count=len(graph.nodes),
            markdown_document_count=len(documents),
        )

        if request.dry_run or _has_errors(diagnostics):
            return Result(data=summary, diagnostics=tuple(diagnostics))

        write_result = self._vault_writer.write_documents(request.output_directory, documents)
        diagnostics.extend(write_result.diagnostics)
        summary = replace(summary, written_markdown_count=len(write_result.data or ()))

        if manifest is not None:
            ai_write_result = self._ai_context_writer.write_manifest(request.output_directory, manifest)
            diagnostics.extend(ai_write_result.diagnostics)
            summary = replace(summary, ai_context_written=ai_write_result.is_success)

        return Result(data=summary, diagnostics=tuple(diagnostics))


def _has_errors(diagnostics: list[Diagnostic]) -> bool:
    """Return whether diagnostics contain at least one blocking error."""
    return any(diagnostic.severity == "error" for diagnostic in diagnostics)


def _optional_object(value: object) -> JsonObject | None:
    """Return a JSON object when optional loaded data has object shape."""
    if isinstance(value, dict):
        return value
    return None
