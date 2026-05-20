---
task: TASK-006
title: "Validate export envelope"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-001
  - US-003
  - US-004
---

# Validate export envelope

## Goal

Validate the top-level structure of loaded RemNote export files. The validator should identify missing required fields and incompatible envelope shapes before graph parsing begins.

## Context

Most RemNote export files use a shared envelope with `docs`, while `metadata.json` has a different top-level structure. Validation must remain separate from transformation logic.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- validate that `rem.json` has the expected envelope and `docs` list
- validate optional shared-envelope files when present
- allow `metadata.json` to use its documented non-`docs` structure
- report clear diagnostics for incompatible structures
- preserve unknown top-level fields

## Out of Scope

- validating individual RemNote records
- parsing rich text content
- writing migration output

## Done

- [x] valid envelopes pass validation
- [x] missing `docs` in shared-envelope files is reported
- [x] non-list `docs` values are reported
- [x] `metadata.json` is handled as a special documented case
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: valid and invalid fixture envelopes produce expected diagnostics
- Verify: unknown fields remain available after validation

## Notes

- follow `context/remnote/JSON_DOKUMENTACE.md`
- validation does not normalize or rewrite loaded data
