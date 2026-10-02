# Malicious-code audit — spec-kitty/spec-kitty @ d78aa2345e61 (main, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/spec-kitty` (11061 text files), then manual review of every category, with extra care for what runs on install/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| Build backend: `hatchling==1.31.0` (pyproject `[build-system]`), no `setup.py`, no custom build hook in use for an editable `uv sync` | pyproject read | benign |
| npm lifecycle hooks / committed binaries | none reported | n/a |
| ~29 `conftest.py` files (auto-run by pytest) — reviewed `tests/conftest.py` (env/HOME isolation, `git init` in tmp dirs, optional test venv via `pip install -e REPO_ROOT`), `tests/charter/conftest.py` (fixtures only), `tests/zeitgeist_client/conftest.py` (binds a localhost socket on port 0 to get a closed port) | read the relevant parts | benign — test isolation only, no outbound network, no secrets read |
| process-spawn (69) | `subprocess.run` of `git`, `python -m venv`, `pip install -e .`, CLI under test | benign, standard test harness |
| pipe-to-shell (5) | `curl … | sh` text in an install hint string in `init.py` and *hostile prompt-injection fixture strings* in `tests/zeitgeist_client/*` (used to test that the client neutralises them) | benign — strings, not executed |
| env-dump (48) / secret-paths (49) | reading env flags, `.netrc/.pypirc/.npmrc` in a **redaction** deny-list, "local state" wording in docstrings | benign |
| marshal (1) `src/specify_cli/cli/commands/_bytecode_doctor.py:126` | unmarshals local installed `.pyc` bodies to diagnose corruption; documented | benign |
| long-base64-blob (1) in a docs report JSON | decodes to `.venv/bin/pytest -q -p no:cacheprovider 'tests/architectural/test_no_legacy_terminology.py::…'` | benign |

Verdict: **no malicious code found.** Only `uv sync`, `mypy`, `ruff` and targeted `pytest` (tests/charter / doctrine agent-profile tests) were run, in an isolated `.venv` inside `/home/user/work/spec-kitty`.
