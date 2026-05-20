# Remnote2Obsidian

Migration tool from RemNote to Obsidian..

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
poetry run remnote2obsidian
```
