---
task: TASK-005
title: "Load RemNote export directory"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-001
  - US-002
---

# Load RemNote export directory

## Goal

Load a RemNote export directory by reading `rem.json` and any supported optional JSON files that are present. The loader should return raw loaded data without interpreting RemNote records.

## Context

FEATURE-001 requires `rem.json` as the primary file and recognizes optional export files. This task builds on the generic JSON adapter and keeps loading separate from parsing.

## Touchpoints

- `src/remnote2obsidian/adapters/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- define the supported RemNote export filenames
- load required `rem.json`
- load optional files when present
- skip absent optional files without errors
- return loaded raw data and diagnostics

## Out of Scope

- envelope validation beyond file presence
- graph construction
- Markdown generation

## Done

- [ ] export loader reads `rem.json`
- [ ] optional files are loaded when present
- [ ] absent optional files do not block loading
- [ ] loaded raw data is preserved without transformation
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: valid fixture with only `rem.json` loads
- Verify: fixture with optional files loads them deterministically

## Notes

- supported optional files should match FEATURE-001
- do not process the full real export in unit tests
