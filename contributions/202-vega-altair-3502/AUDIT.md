# AUDIT — vega/altair (clone of main @ e0a40339, 2026-10-22)

`python3 -I $PG/tools/audit_repo.py altair` → 456 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (setup.py/build hooks) | none; build backend is hatchling (pyproject.toml) | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| conftest.py | none in repo | benign |
| pyproject `[tool.taskipy.tasks]` | only ruff / mypy / ty / pytest / hatch commands | benign |

Verdict: nothing suspicious; safe to install deps and run targeted tests.
