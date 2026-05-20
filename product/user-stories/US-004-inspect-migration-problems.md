---
story: US-004
title: "Inspect migration problems"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-005
---

# Inspect migration problems

## As a

technical user migrating from RemNote

## I want

clear reports about validation and graph issues

## So that

I can understand migration risks and decide whether to continue, fix input data, or review generated output.

## Scope

- report missing required files and invalid JSON
- report graph issues such as missing IDs or broken relationships
- distinguish blocking errors from non-blocking warnings
- support detailed reporting for debugging workflows

## Out of Scope

- automatic repair of RemNote data
- editing source export files
- semantic cleanup of migrated notes

## Acceptance

- [ ] blocking problems are easy to identify
- [ ] non-blocking warnings are visible without stopping all inspection
- [ ] reports include enough context for the user to locate affected source records
- [ ] debugging information can be requested through the migration workflow
- [ ] unknown data is reported or preserved instead of silently discarded

## Notes

- supports PRD-001 auditable migration goals
- useful for large and partially undocumented exports
