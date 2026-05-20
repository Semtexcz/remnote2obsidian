"""Read-only JSON file adapter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from remnote2obsidian.models import Diagnostic, JsonValue, Result, SourceContext


class JsonFileAdapter:
    """Filesystem adapter for reading JSON files without modifying them."""

    def read(self, path: Path | str) -> Result[JsonValue]:
        """Read and decode a JSON file from disk."""
        file_path = Path(path)
        source = SourceContext(file_path=str(file_path))

        try:
            with file_path.open("r", encoding="utf-8") as file:
                raw_data: Any = json.load(file)
        except FileNotFoundError:
            return Result.failure(
                (
                    Diagnostic.error(
                        code="json_file_missing",
                        message=f"JSON file does not exist: {file_path}",
                        source=source,
                    ),
                )
            )
        except PermissionError:
            return Result.failure(
                (
                    Diagnostic.error(
                        code="json_file_unreadable",
                        message=f"JSON file is not readable: {file_path}",
                        source=source,
                    ),
                )
            )
        except json.JSONDecodeError as error:
            return Result.failure(
                (
                    Diagnostic.error(
                        code="json_file_invalid",
                        message=f"JSON file is invalid: {file_path}: {error.msg}",
                        source=source,
                    ),
                )
            )
        except OSError as error:
            return Result.failure(
                (
                    Diagnostic.error(
                        code="json_file_unreadable",
                        message=f"JSON file could not be read: {file_path}: {error}",
                        source=source,
                    ),
                )
            )

        return Result.success(cast(JsonValue, raw_data))
