"""Tests for user-facing documentation promises."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_mvp_usage_documentation_matches_cli_contract() -> None:
    """MVP usage docs should document the implemented CLI surface."""
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    usage = (PROJECT_ROOT / "docs/MVP_USAGE.md").read_text(encoding="utf-8")
    combined = f"{readme}\n{usage}"

    assert "poetry run remnote2obsidian migrate" in combined
    assert "EXPORT_DIRECTORY" in usage
    assert "OUTPUT_DIRECTORY" in usage
    assert "--dry-run" in combined
    assert "--verbose" in combined
    assert "read-only input" in combined
    assert "notes/" in usage
    assert ".remnote2obsidian/manifest.json" in combined
    assert "poetry run pytest" in combined
