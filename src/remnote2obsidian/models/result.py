"""Shared result and diagnostic models for migration workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Generic, TypeVar


T = TypeVar("T")


class DiagnosticSeverity(StrEnum):
    """Severity levels for migration diagnostics."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True, order=True)
class SourceContext:
    """Optional source location for a migration diagnostic."""

    file_path: str | None = None
    rem_id: str | None = None


@dataclass(frozen=True, slots=True, order=True)
class Diagnostic:
    """A deterministic diagnostic message emitted during migration."""

    severity: DiagnosticSeverity
    code: str
    message: str
    source: SourceContext | None = None

    @classmethod
    def error(
        cls,
        code: str,
        message: str,
        source: SourceContext | None = None,
    ) -> Diagnostic:
        """Create an error diagnostic."""
        return cls(
            severity=DiagnosticSeverity.ERROR,
            code=code,
            message=message,
            source=source,
        )

    @classmethod
    def warning(
        cls,
        code: str,
        message: str,
        source: SourceContext | None = None,
    ) -> Diagnostic:
        """Create a warning diagnostic."""
        return cls(
            severity=DiagnosticSeverity.WARNING,
            code=code,
            message=message,
            source=source,
        )


@dataclass(frozen=True, slots=True)
class Result(Generic[T]):
    """Container for migration data and associated diagnostics."""

    data: T | None = None
    diagnostics: tuple[Diagnostic, ...] = field(default_factory=tuple)

    @classmethod
    def success(cls, data: T, diagnostics: tuple[Diagnostic, ...] = ()) -> Result[T]:
        """Create a successful result with optional diagnostics."""
        return cls(data=data, diagnostics=diagnostics)

    @classmethod
    def failure(cls, diagnostics: tuple[Diagnostic, ...]) -> Result[T]:
        """Create a failed result with diagnostics and no data."""
        return cls(data=None, diagnostics=diagnostics)

    @property
    def errors(self) -> tuple[Diagnostic, ...]:
        """Return diagnostics whose severity is error."""
        return tuple(
            diagnostic
            for diagnostic in self.diagnostics
            if diagnostic.severity == DiagnosticSeverity.ERROR
        )

    @property
    def warnings(self) -> tuple[Diagnostic, ...]:
        """Return diagnostics whose severity is warning."""
        return tuple(
            diagnostic
            for diagnostic in self.diagnostics
            if diagnostic.severity == DiagnosticSeverity.WARNING
        )

    @property
    def is_success(self) -> bool:
        """Return whether the result has no error diagnostics."""
        return not self.errors
