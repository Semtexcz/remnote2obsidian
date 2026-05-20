## [0.8.0] - 2026-05-20

### Added

- AI manifest models for mapping RemNote IDs to generated Markdown paths and relationship metadata.
- Deterministic AI manifest generation and JSON serialization.
- AI context writer adapter that writes the manifest to `.remnote2obsidian/manifest.json`.

## [0.7.0] - 2026-05-20

### Added

- Markdown document and path mapping models for Obsidian vault output.
- Deterministic Markdown rendering with YAML frontmatter, child links, attachment listings, and unsupported fragment fallbacks.
- Stable ID-backed Markdown path generation and Obsidian wikilink rendering.
- Obsidian vault writer adapter for generated Markdown files.

## [0.6.0] - 2026-05-20

### Added

- Internal Rem graph models for nodes, roots, hierarchy links, cards, and attachments.
- Rem graph builder with duplicate ID diagnostics, deterministic hierarchy reconstruction, and unsupported type warnings.
- Raw card metadata parsing and card-to-Rem integration by `rId`.
- Attachment reference extraction for `%LOCAL_FILE%...` placeholders and HTTP asset URLs.

## [0.5.0] - 2026-05-20

### Added

- Raw RemNote document and card metadata models that preserve known fields, unknown fields, and original JSON records.
- Raw `rem.json` document parser with deterministic diagnostics for malformed records and missing RemNote IDs.
- Preservation-first rich text fragment parser for plain text, RemNote references, and unsupported fragment data.

## [0.4.0] - 2026-05-20

### Added

- Read-only JSON file adapter with diagnostics for missing, unreadable, and invalid JSON files.
- Raw RemNote export directory loader for required `rem.json` and supported optional export files.
- RemNote export envelope validator for shared `docs` envelopes and the documented `metadata.json` exception.

## [0.3.0] - 2026-05-20

### Added

- Initial migration package boundaries for adapters, domain, services, models, CLI, and utilities.
- Deterministic artificial RemNote export fixtures for valid, optional-file, invalid JSON, missing-file, hierarchy, reference, and attachment cases.
- Shared migration diagnostic and result models for errors, warnings, source context, and generic operation results.

## [0.2.0] - 2026-04-21

### Added

- Copier template configuration with a minimal variable set for project identity and Python packaging.
- Template usage and maintenance documentation for generating and updating projects.
- A workflow playbook that explains how to move from idea to implementation and how to use the Markdown artifacts with an AI agent.

### Changed

- Generalized starter metadata, README, CI, and package layout for Copier-based project generation.
- Replaced the concrete starter package path with a templated `src/{{package_name}}/` structure.

### Fixed

- Corrected `AGENTS.md` references to the actual `docs/ARCHITECTURE.md` path.
