---
task: TASK-019
title: "Write Obsidian vault files"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-003
  - US-008
---

# Write Obsidian vault files

## Goal

Implement an output adapter that writes generated Markdown documents to an Obsidian-compatible directory. The adapter should write deterministic content and avoid modifying source export files.

## Context

Filesystem writing belongs in `adapters/`, while Markdown rendering belongs in `domain/`. This task connects rendered documents to disk output without adding CLI orchestration.

## Touchpoints

- `src/remnote2obsidian/adapters/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- write Markdown document content to output paths
- create output directories as needed
- overwrite generated files deterministically
- report write failures through diagnostics
- add tests using temporary directories

## Out of Scope

- rendering Markdown content
- loading RemNote exports
- merging user edits in existing vaults

## Done

- [ ] Markdown files are written to the output directory
- [ ] directories are created as needed
- [ ] write failures are reported
- [ ] source export files are never modified
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: temporary output directory contains expected files
- Verify: repeated writes produce identical file contents

## Notes

- use temporary directories in tests
- keep adapter independent from graph construction
