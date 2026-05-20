"""Tests for shared migration result models."""

from remnote2obsidian.models import Diagnostic, DiagnosticSeverity, Result, SourceContext


def test_diagnostic_constructors_capture_severity_and_source() -> None:
    """Diagnostic helpers should build explicit error and warning messages."""
    source = SourceContext(file_path="rem.json", rem_id="rem-1")

    error = Diagnostic.error("missing_file", "Required file is missing.", source)
    warning = Diagnostic.warning("unknown_field", "Unknown field preserved.", source)

    assert error.severity == DiagnosticSeverity.ERROR
    assert warning.severity == DiagnosticSeverity.WARNING
    assert error.source == source
    assert warning.source == source


def test_result_groups_errors_and_warnings_in_input_order() -> None:
    """Result diagnostics should remain deterministic and preserve input order."""
    warning = Diagnostic.warning("unknown_field", "Unknown field preserved.")
    error = Diagnostic.error("invalid_json", "JSON could not be decoded.")
    result: Result[object] = Result.failure((warning, error))

    assert result.diagnostics == (warning, error)
    assert result.errors == (error,)
    assert result.warnings == (warning,)
    assert not result.is_success


def test_success_result_can_include_data_and_non_error_diagnostics() -> None:
    """A result with data and only warnings should be considered successful."""
    warning = Diagnostic.warning("optional_missing", "Optional file was skipped.")
    result: Result[dict[str, object]] = Result.success({"docs": []}, diagnostics=(warning,))

    assert result.data == {"docs": []}
    assert result.warnings == (warning,)
    assert result.errors == ()
    assert result.is_success
