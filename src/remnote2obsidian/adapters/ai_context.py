"""Filesystem adapter for writing generated AI context files."""

from __future__ import annotations

from pathlib import Path

from remnote2obsidian.domain.ai_context import serialize_ai_manifest
from remnote2obsidian.models import (
    AI_CONTEXT_MANIFEST_PATH,
    AiManifest,
    Diagnostic,
    Result,
    SourceContext,
)


class AiContextWriter:
    """Write AI context files into the generated vault."""

    def write_manifest(self, output_directory: Path | str, manifest: AiManifest) -> Result[Path]:
        """Write the AI manifest to its stable vault-relative path."""
        destination = Path(output_directory) / AI_CONTEXT_MANIFEST_PATH
        source = SourceContext(file_path=str(destination))
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(serialize_ai_manifest(manifest), encoding="utf-8")
        except OSError as error:
            return Result.failure(
                (
                    Diagnostic.error(
                        code="ai_context_manifest_write_failed",
                        message=f"Could not write AI manifest: {destination}: {error}",
                        source=source,
                    ),
                )
            )
        return Result.success(destination)
