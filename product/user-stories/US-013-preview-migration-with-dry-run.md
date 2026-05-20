---
story: US-013
title: "Preview migration with dry run"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-005
---

# Preview migration with dry run

## As a

technical user preparing a migration

## I want

to run a dry-run migration preview

## So that

I can inspect validation results and planned work before writing files.

## Scope

- run loading and validation without writing output files
- report expected migration inputs and detected optional files
- report blocking errors and non-blocking warnings
- support verbose inspection when requested

## Out of Scope

- writing Markdown output
- writing AI-context files
- modifying the source export

## Acceptance

- [ ] dry run accepts the same input path as full migration
- [ ] dry run reports validation status
- [ ] dry run does not write output files
- [ ] dry run makes blocking issues visible
- [ ] verbose dry run provides additional inspection detail

## Notes

- supports PRD-001 repeatable and auditable migration
- useful before running migration against a large export
