---
story: US-010
title: "Rerun migration deterministically"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
  - FEATURE-005
---

# Rerun migration deterministically

## As a

technical user maintaining a migrated vault

## I want

repeated migrations from the same export to produce the same output

## So that

I can review changes with Git and trust that differences reflect real input or tool changes.

## Scope

- keep generated paths and metadata stable for identical input
- keep Markdown and AI-context output reproducible
- avoid time-dependent or order-dependent output changes
- support safe reruns during migration refinement

## Out of Scope

- synchronizing user edits back into RemNote
- merging hand-edited vault changes automatically
- generating intentionally randomized output

## Acceptance

- [ ] identical input produces identical generated output
- [ ] repeated runs do not modify the source export
- [ ] output is suitable for Git review
- [ ] generated manifests remain stable for identical input
- [ ] validation and warning behavior is consistent across repeated runs

## Notes

- supports PRD-001 repeatable migration workflow
- determinism is required for reliable debugging and future automation
