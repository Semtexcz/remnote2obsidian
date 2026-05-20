---
task: TASK-010
title: "Build Rem graph nodes"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - US-005
  - US-006
---

# Build Rem graph nodes

## Goal

Build internal graph nodes from parsed raw Rem models. Each graph node must preserve the original RemNote ID, known fields, parsed content fragments, references, and unknown source data.

## Context

The internal graph is the boundary between parsing and later transformations. It must be deterministic and must not depend on filesystem or CLI behavior.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- define graph node models
- create nodes keyed by original `_id`
- preserve known and unknown raw source data
- include parsed `key` and `value` content
- report duplicate IDs deterministically

## Out of Scope

- reconstructing hierarchy edges
- generating Markdown paths
- attaching card metadata

## Done

- [ ] graph node model exists
- [ ] nodes are keyed by original RemNote ID
- [ ] duplicate IDs are reported
- [ ] source metadata and unknown fields remain available
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: duplicate ID fixtures produce stable diagnostics
- Verify: graph nodes preserve original RemNote IDs

## Notes

- this is the first graph slice, not the full graph builder
- keep graph construction independent of Markdown output
