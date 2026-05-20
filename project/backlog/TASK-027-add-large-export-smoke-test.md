---
task: TASK-027
title: "Add large export smoke test"
status: backlog
priority: P2
type: test
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-005
  - US-014
---

# Add large export smoke test

## Goal

Add an optional smoke test or documented test path for validating behavior against a large real-world export. The test should not expose sensitive data or make normal test runs slow.

## Context

PRD-001 success criteria include parsing a real RemNote export. The repository contains a real export for development, but tests should avoid unnecessary processing of sensitive and large data.

## Touchpoints

- `tests/integration/`
- `data/remnote_full_export/`
- `context/test-strategy.md`

## Scope

- add a guarded smoke test or documented marker for large export validation
- keep normal `poetry run pytest` fast and deterministic
- validate loading and graph construction on the large export when explicitly enabled
- avoid asserting on sensitive content
- document how to run the large export check

## Out of Scope

- running the large export test by default
- committing additional real export data
- requiring the large export for contributors

## Done

- [ ] large export check is optional or guarded
- [ ] normal test suite remains fast
- [ ] check validates real export loading and graph construction
- [ ] sensitive content is not printed in test output
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: normal tests do not process the full export
- Verify: documented large-export check can be run explicitly

## Notes

- use environment gating or pytest markers
- never mutate files under `data/remnote_full_export/`
