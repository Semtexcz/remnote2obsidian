---
task: TASK-013
title: "Integrate card metadata"
status: backlog
priority: P2
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - US-006
---

# Integrate card metadata

## Goal

Attach available `cards.json` metadata to graph nodes using `rId -> rem._id`. Card metadata should be preserved for traceability without implementing spaced repetition behavior.

## Context

PRD-001 notes that `cards.json` enriches rems through `rId`. Full spaced repetition is out of scope, but metadata should remain available for future migration improvements.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- parse `cards.json` docs into raw card models
- attach cards to matching graph nodes by `rId`
- support multiple cards per Rem
- report card records that reference missing Rem IDs
- preserve unknown card metadata

## Out of Scope

- implementing spaced repetition scheduling
- generating flashcard output
- requiring `cards.json` for migration

## Done

- [ ] cards attach to matching graph nodes
- [ ] multiple cards per Rem are supported
- [ ] missing `cards.json` is accepted
- [ ] unmatched cards produce diagnostics
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: card fixture attaches metadata by `rId`
- Verify: missing optional card file does not fail graph construction

## Notes

- keep card metadata read-only and preservation-focused
- do not infer study behavior from card state
