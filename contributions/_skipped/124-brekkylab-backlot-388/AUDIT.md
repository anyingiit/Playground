# Malicious-code audit — brekkylab/backlot @ 0b08910 (main, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/backlot` (202 text files), then manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/conftest.py` (auto-run, 983 lines) | imports only json/shutil/sys/pathlib/pytest/yaml + backlot; builds an in-memory SQLite sample corpus, a TestClient, and a `live_server` fixture that starts backlot via `backlot.serve` on 127.0.0.1 (0.0.0.0 only when docker is present, for the MCP container tests). No downloads, no shell, no env exfiltration | benign |
| Pattern findings (curl\|sh, eval/base64, etc.) | none reported | — |
| npm lifecycle hooks / committed binaries | none | — |
| `pyproject.toml` build | setuptools + setuptools-scm, no custom build hooks; no `setup.py` | benign |
| `.github/workflows/ci.yml` | `uv sync --all-extras --locked`, `pytest -rs`, Linear example via npm; lint job `ruff format --check .` / `ruff check .`. Only `pytest` and ruff are run here, on a `.[dev]` install | benign |

Verdict: **no malicious code found**; safe to install `.[dev]` into a venv under /home/user/work/backlot and run pytest/ruff.
