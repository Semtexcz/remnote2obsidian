# Remnote2Obsidian

Migration tool from RemNote to Obsidian.

## Structure

- `product/` — features, PRDs, user stories
- `project/` — backlog and workflow tracking
- `docs/` — architecture, vision, decisions, task sequencing
- `src/` — runtime implementation
- `tests/` — behavioral validation

## AI-First Workflow

1. Define product intent in `product/`
2. Capture architecture boundaries in `docs/`
3. Break work into scoped tasks in `project/backlog/`
4. Follow `docs/TASK_SEQUENCE.md`
5. Implement in `src/remnote2obsidian/`
6. Validate with `poetry run pytest`

For the full human-oriented playbook, see `docs/WORKFLOW.md`.

## Getting Started

```bash
poetry install
poetry run pytest
```

## MVP Usage

Run the migration with explicit source and destination paths:

```bash
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault
```

The input path must point to a RemNote JSON export directory containing `rem.json`.
Optional supported export files, such as `cards.json` and `metadata.json`, are loaded
when present. Export files are treated as read-only input; migration output is written
only under the requested Obsidian vault directory.

Preview a migration without writing output files:

```bash
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault --dry-run
```

Show detailed diagnostics during a full migration or dry run:

```bash
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault --verbose
poetry run remnote2obsidian migrate path/to/remnote-export path/to/obsidian-vault --dry-run --verbose
```

Generated output currently includes Markdown notes under `notes/` and an AI-readable
manifest at `.remnote2obsidian/manifest.json`. The manifest maps original RemNote IDs
to generated Markdown paths and relationship metadata for agent-assisted inspection.

For contributor validation, run:

```bash
poetry run pytest
```

See `docs/MVP_USAGE.md` for the concise implementation-oriented usage reference.
