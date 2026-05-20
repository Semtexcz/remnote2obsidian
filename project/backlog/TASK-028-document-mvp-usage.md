---
task: TASK-028
title: "Document MVP usage"
status: backlog
priority: P2
type: docs
created: 2026-05-20
related:
  - FEATURE-005
  - US-001
  - US-013
---

# Document MVP usage

## Goal

Document how to run the migration MVP, including full migration, dry-run mode, verbose mode, and expected outputs.

## Context

Once the CLI workflow exists, users need concise instructions for running the tool safely against a RemNote export and inspecting generated output.

## Touchpoints

- `README.md`
- `docs/`
- `CHANGELOG.md`

## Scope

- document required input and output paths
- document dry-run and verbose usage
- describe generated Markdown and AI context outputs
- mention that export files are treated as read-only input
- include the test command for contributors

## Out of Scope

- writing a full user manual
- documenting unsupported future features
- adding screenshots or marketing material

## Done

- [ ] README or docs explain basic CLI usage
- [ ] dry-run and verbose modes are documented
- [ ] output structure is described
- [ ] read-only source behavior is stated
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: documented commands match implemented CLI options
- Verify: documentation does not promise out-of-scope behavior

## Notes

- keep documentation implementation-oriented and concise
- update changelog according to repository rules
