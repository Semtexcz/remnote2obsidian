---
feature: FEATURE-001
title: "Load RemNote export"
status: planned
created: 2026-05-20
---

# Load RemNote export

## Goal

Load a RemNote JSON export from disk and validate its expected file structure so later migration steps can run deterministically and repeatably.

## Problem

RemNote exports are partially reverse engineered and may contain undocumented fields, optional files, and changing internal structures. The migration needs a safe first step that accepts the export as read-only input, confirms that required data is present, and reports validation problems before any parsing, transformation, Markdown generation, or AI-context generation occurs.

## Scope

- load export files from a user-provided export directory through adapter logic
- require `rem.json` as the primary knowledge export file
- detect optional export files such as `cards.json`, `metadata.json`, `user_data.json`, `knowledge_base_data.json`, `knowledgebase_local_stored_data.json`, `local_stored_data.json`, and `spaced_repetition_scheduler.json`
- validate that loaded JSON files are readable, valid JSON, and structurally compatible with the documented RemNote export envelope where applicable
- preserve unknown fields and nested structures without modification
- return loaded export data and validation results for later pipeline steps
- report missing required files, unreadable files, invalid JSON, and incompatible top-level structures with clear error messages

## Out of Scope

- parsing `rem.json` into an internal graph
- interpreting RemNote object types or rich text fragments
- transforming RemNote data into domain models
- generating Markdown or Obsidian files
- generating AI-readable context files or manifests
- modifying, normalizing, deleting, or rewriting export files

## Success Criteria

- [ ] loading succeeds when a valid export directory contains `rem.json`
- [ ] optional export files are loaded when present and skipped when absent
- [ ] missing `rem.json` produces a clear validation error
- [ ] invalid or unreadable JSON files produce clear validation errors
- [ ] unknown fields and structures are preserved in the loaded output
- [ ] validation logic remains separate from transformation logic
- [ ] loading behavior is deterministic for identical input files

## Notes

- loading logic belongs in `adapters/`
- validation must remain separate from later parsing and transformation logic
- export files must be treated as read-only input
- `context/remnote/JSON_DOKUMENTACE.md` is the source of current reverse-engineered export format knowledge
- the feature should preserve data first because the RemNote export format is partially undocumented
