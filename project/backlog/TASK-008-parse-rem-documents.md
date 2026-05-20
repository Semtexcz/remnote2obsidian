---
task: TASK-008
title: "Parse raw Rem documents"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - US-005
  - US-006
---

# Parse raw Rem documents

## Goal

Convert validated `rem.json` docs entries into raw RemNote models. The parser should preserve every record that can be represented and report record-level issues without generating output files.

## Context

Graph construction needs raw Rem models keyed by original IDs. This task converts loaded JSON records into raw models while keeping parsing separate from rendering.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- parse `rem.json` `docs` entries into raw Rem models
- report records that are not JSON objects
- report missing `_id` values
- preserve original record order for deterministic diagnostics
- keep unknown fields attached to parsed records

## Out of Scope

- constructing hierarchy
- parsing rich text fragments
- attaching card metadata
- writing files

## Done

- [ ] valid docs entries become raw Rem models
- [ ] missing IDs are reported
- [ ] non-object docs entries are reported
- [ ] parser output is deterministic
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: parser preserves IDs and unknown fields from fixtures
- Verify: parser does not depend on adapters or CLI

## Notes

- malformed records should produce diagnostics rather than silent drops
- keep enough source context for debugging
