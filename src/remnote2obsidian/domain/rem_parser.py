"""Parse validated `rem.json` envelope data into raw RemNote models."""

from __future__ import annotations

from remnote2obsidian.models import Diagnostic, JsonObject, RawRemDocument, Result, SourceContext


def parse_raw_rem_documents(rem_envelope: JsonObject) -> Result[tuple[RawRemDocument, ...]]:
    """Parse `rem.json` `docs` entries into raw RemNote document models."""
    docs = rem_envelope.get("docs")
    if not isinstance(docs, list):
        return Result.failure(
            (
                Diagnostic.error(
                    code="raw_rem_docs_not_list",
                    message="rem.json top-level `docs` must be a list before parsing.",
                    source=SourceContext(file_path="rem.json"),
                ),
            )
        )

    parsed_documents: list[RawRemDocument] = []
    diagnostics: list[Diagnostic] = []

    for index, record in enumerate(docs):
        source = SourceContext(file_path=f"rem.json:docs[{index}]")
        if not isinstance(record, dict):
            diagnostics.append(
                Diagnostic.error(
                    code="raw_rem_record_not_object",
                    message=f"rem.json docs[{index}] must be a JSON object.",
                    source=source,
                )
            )
            continue

        raw_rem = RawRemDocument.from_json(record)
        if raw_rem.rem_id is None:
            diagnostics.append(
                Diagnostic.error(
                    code="raw_rem_id_missing",
                    message=f"rem.json docs[{index}] is missing a string `_id`.",
                    source=source,
                )
            )
            continue

        parsed_documents.append(raw_rem)

    return Result(data=tuple(parsed_documents), diagnostics=tuple(diagnostics))
