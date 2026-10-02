# Audit — ipython/ipython @ 93dde62b (shallow clone of `main`, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/ipython` (363 text files, 0 committed binaries) + manual review of everything that runs on install/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| conftest.py (root) | Autouse fixture that stops the `%%script` asyncio loop after each test | benign |
| tests/conftest.py | Sets `IPYTHONDIR` to `./tmp-ipython-pytest-profiledir`, builds a TerminalInteractiveShell for tests, removes the temp dir afterwards | benign |
| setup.py | Python version check + setuptools setup; not executed (installed via `pip install -e` using pyproject / setuptools backend only) | benign |
| IPython/testing/plugin/setup.py | Legacy nose plugin metadata; never executed | benign |
| .pre-commit-config.yaml | pre-commit-hooks + darker(ruff); not run automatically | benign |
| pyproject `addopts` `-pIPython.testing.plugin.pytest_ipdoctest` | In-repo doctest plugin | benign |
| env-dump: osm.py:457, tests/test_kitty.py:264, tests/test_pretty.py:538 | Copy of os.environ for `%env` magic / subprocess env / pretty-print test; nothing sent anywhere | benign |
| pickle: deduperreload.py:465, external/pickleshare.py:91, tests/test_macro.py:75 | AST deep copy, local profile DB, round-trip test | benign |

Verdict: nothing malicious; safe to `pip install -e .[test]` and run pytest / ruff / mypy.
