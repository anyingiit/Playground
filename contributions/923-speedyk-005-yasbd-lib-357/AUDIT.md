# AUDIT — speedyk-005/yasbd-lib @ 60c9c48 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/yasbd-lib` → 132 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (auto-exec surface) | Only `astral-sh/ruff-pre-commit` v0.15.13 hooks `ruff-format`, `ruff --fix` | benign; not installed/run here anyway |
| `.gitignore:193`, `.gitignore:210` (secret-paths) | Standard GitHub Python `.gitignore` comment and `.pypirc` ignore entry | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |

Manual extra checks: no `setup.py`, no `conftest.py`; `pyproject.toml` uses plain `setuptools.build_meta`; test
files only import the library and read `tests/test_data`. CI (`build-and-test.yml`) just runs `pip install -e ".[dev]"` + pytest.

**Verdict: nothing suspicious; safe to install and run tests.**
