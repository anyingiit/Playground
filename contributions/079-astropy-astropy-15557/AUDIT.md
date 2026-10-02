# AUDIT — astropy/astropy @ bab4b9c4 (shallow clone, 2026-10-01)

Tool: `python3 tools/audit_repo.py /home/user/work/astropy` (1261 text files). Reviewed manually before any build/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| setup.py | extension_helpers `get_extensions()` + stub-generation install hook (`astropy.units.typing_utils.create_stubs`) | benign — standard C-extension build |
| conftest.py (root, astropy/, wcs/, wcsapi/, io/fits, table, cosmology, docs) | pytest config/header, hypothesis profiles, fixtures building WCS objects; no network/subprocess | benign |
| tox.ini / .pre-commit-config.yaml | standard tox envs / ruff etc.; not executed except ruff run manually | benign |
| marshal/pickle-exec (59) | all `pickle.loads(pickle.dumps(...))` round-trip tests | benign |
| secret-paths (1) `.circleci/config.yml` ssh key path | CI deploy-key reference for docs deployment, not run locally | benign |
| npm hooks / committed binaries | none | — |

Verdict: **no malicious code found**. Built with `uv pip install -e ".[test]"` in a local py3.12 venv.
