# Malicious-code audit — commitizen-tools/commitizen @ 642b8beb81a8fe5d50a805b168bede25a3563eea

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/commitizen` (159 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (auto-exec surface) | Hooks: pre-commit-hooks, uv-pre-commit, blacken-docs, codespell, commitizen itself, taplo, local `poe format` / `poe lint`. Not installed/run here (only ran ruff/mypy/pytest/mkdocs directly). | benign |
| `tests/conftest.py` (auto-exec) / `:145` `subprocess.run` | Only in the `tmp_commitizen_project_with_gpg` fixture: runs `gpg --batch --quick-gen-key` with a temporary `GNUPGHOME`; other fixtures create temp git repos. No network, no reads outside tmp. | benign |
| `tests/commands/conftest.py` (auto-exec) | Fixtures for config / mocking; no subprocess or network. | benign |
| env-dump `commitizen/hooks.py:29`, `tests/test_bump_hooks.py:22-23` | Copies `os.environ` to pass env to user-configured bump hooks (`CZ_PRE_*` vars); tests assert on it. Nothing sent anywhere. | benign |
| npm lifecycle hooks / committed binaries | none | — |

Dependencies installed from the repo's `uv.lock` (PyPI) via `uv sync --frozen`.

**Verdict: no malicious code found; safe to build and test.**
