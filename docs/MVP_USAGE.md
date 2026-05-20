# MVP Usage

## Purpose

This document describes how to run the current migration MVP from a RemNote JSON export
directory into an Obsidian-compatible output vault.

## Required Paths

The CLI requires two positional paths:

- `EXPORT_DIRECTORY`: a RemNote JSON export directory containing `rem.json`
- `OUTPUT_DIRECTORY`: the destination directory for the generated Obsidian vault

The export directory is read-only input. The migration loads supported JSON files from
that directory and writes generated files only under the output directory.

## Full Migration

```bash
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault
```

On success, the command prints a deterministic summary with loaded file counts, graph
counts, planned output counts, written Markdown counts, AI-context status, warnings, and
errors. On blocking errors, the command exits with a non-zero status.

## Dry Run

```bash
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault --dry-run
```

Dry-run mode validates and plans the migration without creating the output directory or
writing Markdown or AI-context files. Use it before writing a large vault or when
inspecting validation problems.

## Verbose Diagnostics

```bash
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault --verbose
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault --dry-run --verbose
```

Verbose mode includes ordered diagnostics in addition to the standard summary. It does
not change migration behavior.

## Output Structure

The MVP writes these generated files:

```text
path/to/obsidian-vault/
  notes/
    <title>--<remnote-id>.md
  .remnote2obsidian/
    manifest.json
```

Markdown files preserve RemNote IDs in frontmatter and represent supported hierarchy,
references, attachments, card metadata, and unsupported fragments in deterministic
Obsidian-compatible output.

The AI manifest maps original RemNote IDs to generated Markdown paths and relationship
metadata so humans and AI agents can trace generated notes back to source graph nodes.

## Contributor Validation

Run the deterministic test suite before committing changes:

```bash
poetry run pytest
```

Large real-export validation is opt-in and skipped by default. See
`context/test-strategy.md` for the explicit large-export smoke-test command.
