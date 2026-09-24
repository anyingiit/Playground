# Malicious-code audit — Mozart2234/herdr-agent-pulse @ 971ca17

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/herdr-agent-pulse` (24 text files).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (setup.py / conftest / hooks / Makefile) | none exist; project is stdlib-only, no install step | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none (0 bytes) | benign |
| env-dump `tests/test_config.py:12,80` `dict(os.environ)` | snapshot of env in setUp so tearDown can restore it; nothing sent anywhere | benign |
| `tests/fake_server.py` (socket) | local AF_UNIX fake server in a temp dir, no network | benign |
| `tests/test_schema_smoke.py` subprocess | runs `herdr api schema --json` only if `herdr` is on PATH (skipped here) | benign |
| `agent_pulse/client.py` socket | AF_UNIX client to herdr's local socket | benign |
| `bin/ensure-daemon` | reads pidfile, `kill -0`, nohup `python3 -m agent_pulse.daemon`; not run by tests | benign |
| `.github/workflows/ci.yml` | sh -n, py_compile, unittest | benign |

Verdict: **no malicious code found**; safe to run the unit tests (stdlib only, no installs).
