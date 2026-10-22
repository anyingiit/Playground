# Audit — speedyk-005/yasbd-lib @ 60c9c48

`python3 tools/audit_repo.py /home/user/work/yasbd-lib` (132 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (auto-exec surface) | Only `astral-sh/ruff-pre-commit` v0.15.13 hooks `ruff-format` / `ruff --fix`; not installed/run here | benign |
| npm lifecycle hooks | none (no package.json) | n/a |
| Committed binaries | none | n/a |
| `.gitignore:193`, `.gitignore:210` (secret-paths) | Comment and `.pypirc` ignore entries from the standard Python gitignore template | benign |
| Install path (`pyproject.toml`) | setuptools build backend, no custom setup.py/build hooks; deps regex, retrie, radicli, beartype (+ pytest/ruff for dev) | benign |
| Test setup | No `conftest.py`; `tests/__init__.py` + plain pytest modules and data files | benign |
| `scripts/reformat_sets.py` | Imports only `re`, `pathlib`; rewrites set literals in `src/yasbd/rules` | benign |

Verdict: nothing suspicious; safe to install and run tests.
