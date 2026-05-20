---
task: TASK-002
title: "Add deterministic RemNote fixtures"
status: done
priority: P1
type: test
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - US-002
  - US-003
---

# Add deterministic RemNote fixtures

## Goal

Create small deterministic fixture exports for unit and integration tests. The fixtures should represent valid, invalid, and edge-case RemNote export structures without relying on the large real export.

## Context

The test strategy prefers small deterministic fixtures. The real export is sensitive and large, so implementation tasks need compact test data that exercises loading, validation, graph construction, references, attachments, and unknown fields.

## Touchpoints

- `tests/fixtures/`
- `tests/unit/`

## Scope

- add a minimal valid export fixture containing `rem.json`
- add a fixture with optional `cards.json` and `metadata.json`
- add fixtures for invalid JSON and missing `rem.json`
- add a fixture containing hierarchy, references, unknown fields, and attachment references
- document fixture intent in fixture-local README or test names

## Out of Scope

- copying the full real export into tests
- implementing loaders or parsers
- testing Markdown output

## Done

- [x] deterministic fixtures exist
- [x] fixtures are small and safe to commit
- [x] fixtures cover valid and invalid export cases
- [x] fixtures include representative hierarchy and metadata
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: fixture files are valid where intended
- Verify: invalid fixtures are clearly named and isolated

## Notes

- use artificial data with fake IDs and no personal information
- keep fixture structure close to `context/remnote/JSON_DOKUMENTACE.md`
