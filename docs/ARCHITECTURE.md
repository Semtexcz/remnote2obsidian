# Architecture

## Purpose

This repository is designed for AI-assisted development.

Use this file to understand:

- where code belongs
- which boundaries must be preserved
- where project knowledge is stored
- how RemNote export data should be handled

The project converts RemNote JSON exports into a Markdown/Obsidian vault optimized for both humans and AI agents.

---

## Repository Structure

### Documentation and Planning

- `docs/`
  - architecture, workflow, ADRs, project-level technical guidance

- `product/`
  - PRDs, features, user stories

- `project/`
  - implementation backlog and execution planning

These directories must not contain runtime application logic.

---

### Context and Reverse Engineering Knowledge

- `context/`
  - long-term technical context for AI agents and developers
  - reverse-engineering notes
  - parsing observations
  - migration strategy notes

#### RemNote Context

- `context/remnote/JSON_DOKUMENTACE.md`
  - primary reverse-engineered documentation of the RemNote export format
  - must be read before implementing parsing logic

This file documents:

- `rem.json`
- `cards.json`
- metadata files
- object relationships
- attachment handling
- observed object types
- known uncertainties in the export format

---

### Export Data

- `data/remnote_full_export/`
  - full real-world RemNote export
  - used for development, debugging, and migration validation

Important:

- this directory contains sensitive and large data
- data should not be modified by migration logic
- migration code must treat export files as read-only input
- agents should avoid unnecessary processing of the full export unless required

Primary files:

- `rem.json`
  - primary knowledge source

- `cards.json`
  - spaced repetition metadata linked through `rId -> rem._id`

- `metadata.json`
  - export and sync metadata

---

### Application Code

- `src/remnote2obsidian/`
  - all runtime behavior belongs here

Preferred structure:

- `domain/`
  - core migration logic
  - internal knowledge graph
  - Markdown generation rules

- `services/`
  - orchestration of migration workflows

- `adapters/`
  - filesystem access
  - RemNote loaders
  - Obsidian writers

- `cli/`
  - command-line interface
  - if a CLI is implemented, it must be built with Typer

- `models/`
  - shared data structures

- `utils/`
  - small generic helpers

---

### Tests

- `tests/`
  - validation of behavior

Test hierarchy:

1. unit tests
2. integration tests
3. e2e tests

Test behavior, not implementation details.

Prefer small deterministic fixtures over using the full export.

Future recommended structure:

```text
tests/
  fixtures/
````

Example fixtures:

```text
tests/fixtures/simple_rem_tree.json
tests/fixtures/rem_with_references.json
tests/fixtures/rem_with_attachments.json
```

---

## Architectural Principles

### Preserve First

The migration should prioritize preserving information over aggressive optimization.

Unknown fields or structures must not be silently discarded.

---

### Deterministic Output

Migration output should be:

- reproducible
- Git-friendly
- auditable

Repeated migration runs should produce stable results.

---

### Internal Knowledge Graph

The migration pipeline should conceptually work as:

```text
RemNote Export
→ Internal Graph Representation
→ Markdown Transformation
→ Obsidian Vault
→ AI Context Layer
```

Do not tightly couple parsing directly to Markdown rendering.

---

### AI-Agent Compatibility

The generated vault should support:

- human navigation
- AI-agent context loading
- future automation workflows

The system should preserve:

- original RemNote IDs
- hierarchy
- references
- attachment relationships
- metadata where possible

---

## Boundary Rules

- `domain/` must not depend on CLI or filesystem details
- `services/` may coordinate domain and adapters
- `adapters/` handle external I/O
- `cli/` should remain thin
- CLI entry points must use Typer for argument parsing and command definitions
- `utils/` must not become a dumping ground

Do not put application logic in:

- markdown files
- tests
- scripts

---

## Change Rule

Before making changes, identify:

- related PRD
- related feature
- related task
- affected modules
- required tests

Modify only the minimum relevant files.

Prefer small vertical slices over large refactors.

---

## Important Rules for Agents

Before implementing RemNote parsing logic, read:

- `context/remnote/JSON_DOKUMENTACE.md`
- `docs/ARCHITECTURE.md`

The RemNote export format is partially undocumented and reverse engineered from real exports.

Important assumptions:

- `rem.json` is the primary knowledge source
- `cards.json` enriches rems through `rId -> _id`
- object types may evolve over time
- attachment references may exist as:

  - `%LOCAL_FILE%...`
  - S3 URLs

The migration must preserve original RemNote IDs whenever possible.

```
