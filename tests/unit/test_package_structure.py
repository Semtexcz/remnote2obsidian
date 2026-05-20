"""Smoke tests for the migration package structure."""

import importlib


def test_migration_package_boundaries_are_importable() -> None:
    """The architectural package boundaries should import successfully."""
    module_names = (
        "remnote2obsidian.adapters",
        "remnote2obsidian.cli",
        "remnote2obsidian.domain",
        "remnote2obsidian.models",
        "remnote2obsidian.services",
        "remnote2obsidian.utils",
    )

    for module_name in module_names:
        assert importlib.import_module(module_name).__name__ == module_name
