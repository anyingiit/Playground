# AUDIT — vega/altair (shallow clone of main, 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/altair` → 454 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (setup.py/build hooks) | none found; build backend is hatchling (pyproject.toml) | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| conftest.py | none in repo | benign |
| pyproject `[tool.taskipy.tasks]` | only ruff / mypy / ty / pytest / hatch commands | benign |

Verdict: nothing suspicious; safe to install deps and run targeted tests.
