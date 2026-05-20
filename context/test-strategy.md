# Test Strategy

- Prefer unit tests first.
- Add integration tests when multiple modules interact.
- Use e2e tests only for critical workflows.
- Tests must be deterministic.
- Run tests with: `poetry run pytest`
- Large real-export smoke tests are opt-in and skipped by default.
- Run the large export check explicitly with:

```bash
REMNOTE2OBSIDIAN_RUN_LARGE_EXPORT=1 poetry run pytest -m large_export tests/integration/test_large_export_smoke.py
```
