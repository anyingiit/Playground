# Malicious-code audit — mloda-ai/mloda (main, 2026-09-24)

Tool: `python3 tools/audit_repo.py` + manual review. **Verdict: no malicious code found.**

| Hit | Location | Reviewed verdict |
|---|---|---|
| conftest.py ×8, tox.ini (auto-exec) | `tests/**/conftest.py`, `tox.ini` | Benign: fixtures (Spark session, DuckDB/SQLite connections, plugin loader state); no subprocess/network calls. `tox.ini` runs pytest, ruff, mypy, bandit, pip-licenses and an optional `flock` wrapper |
| pickle.loads ×27 | `mloda/core/abstract_plugins/compute_framework.py`, tests | Benign: round-trip pickling of the project's own objects (`pickle.loads(pickle.dumps(x))`), already `# nosec`-annotated for bandit |
| pipe-to-shell ×2 | `.devcontainer/Dockerfile` (Claude Code + uv installers) | Benign: dev-container image only; not run by tests |
| npm hooks / committed binaries | none | — |

What was executed here: `pip install -e ".[test,pandas,spark]"`, pytest (Spark filter tests), full `tox -e python311`.
