# Malicious-code audit — cubrid-lab/sqlalchemy-cubrid @ main (shallow clone)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/sqla-cubrid` (101 text files) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Pattern findings / committed binaries / npm hooks | none reported | benign |
| `test/conftest.py` (runs every pytest session) | registers Hypothesis profiles; CI-only guard that exits if all integration tests are skipped; loads SQLAlchemy's testing plugin only for `--dburi`; reads `test/known_failures.txt` to apply strict xfail. No network, subprocess or file writes | benign |
| `tox.ini` | pytest/ruff commands only | benign (tox not used here) |
| `.pre-commit-config.yaml` | ruff, mypy, bandit from official repos | benign (pre-commit not installed/run) |
| `pyproject.toml` build | standard setuptools metadata; runtime dep `sqlalchemy>=2.0,<2.3` only; no custom build hooks | benign |
| `Makefile` | wrappers for pytest/ruff/mypy/bandit/docker compose | benign (not run except equivalent commands by hand) |
| `docker-compose.yml`, `scripts/` | CUBRID container, docs generator — not executed | not run |

Verdict: **no malicious code found**. Installed with `pip install -e .` + the test/lint tools into a venv inside `/home/user/work/`; only offline tests run (no CUBRID/docker).
