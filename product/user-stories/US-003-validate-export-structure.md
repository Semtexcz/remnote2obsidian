---
story: US-003
title: "Validate export structure"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
---

# Validate export structure

## As a

RemNote user

## I want

the tool to validate my export before migration continues

## So that

I know early whether the export can be migrated safely.

## Scope

- check that required export files are present
- detect invalid or unreadable JSON files
- identify incompatible top-level structures
- report validation problems clearly

## Out of Scope

- repairing corrupted exports
- interpreting RemNote object types
- generating output files

## Acceptance

- [ ] missing `rem.json` is reported as a blocking validation problem
- [ ] invalid JSON is reported with a clear message
- [ ] incompatible export structure is reported before migration output is written
- [ ] valid optional files are accepted when present
- [ ] validation does not alter export files

## Notes

- supports PRD-001 safety and repeatability goals
- validation should help users fix input problems before running a full migration
