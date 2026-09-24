# Malicious-code audit — rnag/dataclass-wizard @ 57535e9 (main, v1.0.0)

Command: `python3 /home/user/Playground/tools/audit_repo.py dataclass-wizard` (173 text files scanned), then manual review of every auto-executing file **before** installing or running anything.

| Hit | Reviewed | Verdict |
|---|---|---|
| `pyproject.toml` build (setuptools>=64, `version` from `dataclass_wizard/__version__.py`) | Read full file incl. `[tool.tox]` legacy ini (`uv pip install -e .[all]`, `pytest`) | Benign — standard setuptools build, no custom build hooks, no `setup.py` |
| `.pre-commit-config.yaml` | rstcheck on README + `check-ast` | Benign (not run) |
| `tests/conftest.py` | Fixtures (`restore_logger`, `data_file_path`, `snake`), version-based `collect_ignore` | Benign |
| `tests/unit/conftest.py`, `tests/unit/v0/conftest.py` | `SampleClass`, `MyUUIDSubclass`, caplog fixtures | Benign |
| `benchmarks/conftest.py` | `n` fixture + `--all` option | Benign (benchmarks not run) |
| `Makefile` | `init` = pip install extras + pre-commit; clean targets | Benign (not run) |
| Pattern findings (network, eval/exec of remote data, obfuscation, base64 blobs) | none reported | — |
| Committed binaries | none | — |

Runtime dependency set installed for tests (into throw-away venvs under `/home/user/work/`): `pytest==8.3.4`, `pytest-mock`, `python-dotenv`, `pytimeparse==1.1.8`, `tomli-w`, `PyYAML`, `tzdata`, `typing-extensions` (3.11/3.12), `flake8`. No install scripts from the repo beyond the editable setuptools install.

**Verdict: no malicious or suspicious code found.** Safe to build and test.
