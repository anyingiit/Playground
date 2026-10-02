# Malicious-code audit — cubrid-lab/pycubrid @ 3db0907

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pycubrid-371` (131 text files) + manual review.
Reviewed BEFORE installing or running anything.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (ruff, mypy, bandit hooks from upstream repos) | Read in full; only standard public hooks; not installed/run here | benign |
| `tests/conftest.py` (auto-exec on every pytest session) | Read in full: registers Hypothesis profiles, skips `integration`-marked tests unless `CUBRID_TEST_URL/HOST` set, monkeypatches backslash-escape probe. No I/O, no network, no subprocess | benign |
| conftest.py:64 "network-call" pattern | False positive — word "probing … socket" in a docstring | benign |
| `socket.create_connection` in `pycubrid/connection.py`, `pycubrid/aio/connection.py` | The driver's own TCP connect to the configured CUBRID broker (expected for a DB driver); only reached by integration tests, which are skipped offline | benign |
| `socket.create_connection` in tests (test_ssl, test_ping, test_network_edge_cases, …) | All are `patch`/`monkeypatch` of the call with fakes | benign |
| `scripts/check_translation_sync.py` uses `subprocess.run` | Docs CI helper (git log calls); not invoked by tests/install | benign |
| Build backend | `setuptools.build_meta`, no `setup.py`, no custom build hooks, `dependencies = []` | benign |
| npm hooks / committed binaries | none | — |

Verdict: **no malicious code found**. Safe to `pip install -e ".[dev]"` in a venv and run offline tests.
