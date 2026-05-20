---
story: US-012
title: "Handle unknown object types safely"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
---

# Handle unknown object types safely

## As a

technical user migrating a partially undocumented export

## I want

unknown RemNote fields and object types to be preserved or reported safely

## So that

the migration does not lose information just because the export format is not fully understood.

## Scope

- preserve unknown fields and nested structures
- report unsupported object types when they affect migration quality
- keep output inspectable even when some structures cannot be fully interpreted
- avoid silently dropping data during loading, parsing, or generation

## Out of Scope

- fully reverse engineering every RemNote object type
- guessing unsupported semantics aggressively
- blocking all migration output because of every unknown field

## Acceptance

- [ ] unknown fields are preserved or represented in output
- [ ] unsupported object types can be inspected after migration
- [ ] warnings are produced when unknown structures may affect output quality
- [ ] migration continues when unknown data is non-blocking
- [ ] no unknown data is silently discarded

## Notes

- supports PRD-001 preservation-first constraint
- RemNote export format is partially reverse engineered
