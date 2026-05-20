---
story: US-009
title: "Use AI-readable context"
status: draft
created: 2026-05-20
related:
  - FEATURE-004
---

# Use AI-readable context

## As a

user building AI-assisted knowledge workflows

## I want

machine-readable context files generated with the vault

## So that

AI agents can understand note locations, source IDs, and relationships without scanning the entire vault manually.

## Scope

- generate a manifest mapping RemNote IDs to Markdown paths
- include relationship information useful for AI navigation
- include enough metadata for traceability
- keep context files deterministic and machine-readable

## Out of Scope

- automatic semantic rewriting of notes
- replacing Markdown as the human-readable output
- duplicating Markdown document bodies

## Acceptance

- [ ] AI context includes a source ID to Markdown path mapping
- [ ] relationship context is available where known
- [ ] context files are deterministic across repeated runs
- [ ] AI agents can identify where migrated content lives in the vault
- [ ] context generation does not require modifying source export files

## Notes

- supports PRD-001 AI-agent compatibility
- generated context should complement Markdown rather than replace it
