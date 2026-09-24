# Malicious-code audit — fsspec/projspec @ dc5de4c (main, 2026-07-12)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/projspec` (142 text files), then manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/conftest.py` (auto-run) | 12 lines: one fixture `Project(<repo root>, walk=True)` | benign |
| `.pre-commit-config.yaml` | standard hooks (pre-commit-hooks, black, absolufy-imports, yesqa, blacken-docs); not run locally | benign |
| `pyproject.toml` build | hatchling + hatch-vcs, no custom build hooks besides vcs version file | benign |
| `src/projspec/tools.py` pipe-to-shell strings (uv/pixi/nvm/rustup/pulumi/nixpacks/bun/deno installers) | data in `ToolInfo.install_suggestions` shown to users; only executed by `install_tool()` on explicit user request; all official vendor URLs | benign |
| `tests/test_tools.py` curl\|sh strings | every `install_tool` test patches `subprocess.call` (mock) — nothing is downloaded/executed | benign |
| `subprocess` in `src/projspec/artifact/*`, `proj/*` | runs project tools (uv, npm, flask, …) only when an artifact's `make()` is called; tests that do this (`test_webapp.py`, `test_marimo.py`) start local flask/marimo processes on 127.0.0.1 and clean them up | benign |
| npm lifecycle hooks / committed binaries | none | — |
| `.github/workflows/main.yaml` | `pip install -e .[test]` + `pytest -v --cov projspec`; pre-commit lint job | benign |

Verdict: **no malicious code found**; safe to install and run the test suite in an isolated venv under /home/user/work.
