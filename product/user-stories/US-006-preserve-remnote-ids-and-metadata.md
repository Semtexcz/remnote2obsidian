---
story: US-006
title: "Preserve RemNote IDs and metadata"
status: draft
created: 2026-05-20
related:
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
---

# Preserve RemNote IDs and metadata

## As a

technical user migrating a knowledge base

## I want

original RemNote IDs and important metadata to remain available after migration

## So that

I can trace generated files back to source records and rerun migrations safely.

## Scope

- preserve original RemNote `_id` values
- preserve available source metadata needed for traceability
- include IDs in Markdown metadata or equivalent stable output
- include IDs in AI-readable context files

## Out of Scope

- exposing sensitive metadata unnecessarily
- changing source RemNote IDs
- creating a synchronization system back to RemNote

## Acceptance

- [ ] generated notes retain the original RemNote ID
- [ ] AI-readable context can map source IDs to generated files
- [ ] source metadata used for traceability is stable across runs
- [ ] unknown metadata is not silently discarded
- [ ] users can inspect which source record produced a generated note

## Notes

- supports PRD-001 traceability and repeatability
- preservation should be balanced with privacy for sensitive export metadata
