---
task: TASK-004
title: "Implement JSON file adapter"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-001
  - US-002
  - US-003
---

# Implement JSON file adapter

## Goal

Implement a filesystem adapter that reads JSON files from disk without modifying them. The adapter should provide clear diagnostics for missing, unreadable, and invalid JSON files.

## Context

Export loading belongs in `adapters/`. RemNote export files are read-only input, and validation must happen before graph parsing or transformation.

## Touchpoints

- `src/remnote2obsidian/adapters/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- add a JSON file reading adapter
- return parsed JSON data and diagnostics
- handle missing files, permission errors, and invalid JSON
- keep file reads read-only
- add unit tests using temporary files

## Out of Scope

- validating RemNote envelope structure
- parsing RemNote records into models
- writing output files

## Done

- [x] adapter reads valid JSON
- [x] adapter reports missing and unreadable files
- [x] adapter reports invalid JSON
- [x] adapter does not write or modify input files
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: invalid JSON fixture produces a diagnostic
- Verify: adapter has no dependency on domain or CLI modules

## Notes

- use only standard-library filesystem and JSON APIs
- preserve parsed data exactly as loaded
