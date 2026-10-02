# Malicious-code audit — BfArM-MVH/grz-tools @ 6ed9cb0 (main, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/grz-tools` (287 text files) + manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `packages/grz-db/tests/conftest.py` (auto-run) | Only imports fixtures from `grz_db.testing` and loads a JSON example from `grz_pydantic_models_testing` | benign |
| `grz_db/testing.py` (imported by conftest) | pytest-postgresql fixtures; starts a local throw-away PostgreSQL only if `pg_config` exists (skipped here), sqlite otherwise; no network/subprocess beyond that | benign |
| `tests/conftest.py`, `packages/grzctl/tests/conftest.py`, `packages/grzctl/tests/cli/conftest.py`, `packages/grz-cli/tests/conftest.py` (auto-run) | grep for subprocess/os.system/urlopen/requests/eval/exec/base64: none; URLs are config placeholders (`s3.amazonaws.com`, `bfarm.localhost`, `example.invalid`) used as test config values | benign (not run anyway: only grz-db tests executed) |
| `.gitignore:173,188` secret-paths | comments / `.pypirc` ignore entries | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| Build backend | hatchling (grz-db); maturin/Rust only for `grz-check`, which is **not** built here (`uv sync --package grz-db`) | benign |
| tox config (`pyproject.toml [tool.tox]`) | runs pytest / ruff / mypy via uv only | benign |

**Verdict: nothing suspicious. Safe to install grz-db and run its tests.**
