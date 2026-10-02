# Malicious-code audit — cuga-project/cuga-apps (fix target for cuga-project/cuga-agent#822)

Issue #822 is filed on cuga-agent, but the code it names (`cuga-apps/mcp_servers/text/server.py`) lives in the
sibling repo **cuga-project/cuga-apps** (path `cuga-apps/mcp_servers/text/server.py`). Both repos were cloned; only
cuga-apps code was executed.

- cuga-apps clone: `/home/user/work/cuga-apps-822` @ `51b087ee7a34f8f556c350eac0b24fc6901ebed9` (main, 2026-06-25)
- cuga-agent clone (read-only reference, nothing executed): `/home/user/work/cuga-agent-822` @ `a899ff36208b`
- Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/cuga-apps-822` (293 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `cuga-apps/tests/conftest.py` (pytest conftest, exec surface) | Read in full. Puts `apps/` and repo root on `sys.path`, imports `apps._ports` (port constants), and in `pytest_collection_modifyitems` skips every test if `localhost:3001` (umbrella UI) is not listening; helpers open MCP/HTTP sessions only to `localhost` ports from `_ports.py`. | benign |
| `cuga-apps/tests/conftest.py:41` network-call `socket.create_connection((host, port))` | TCP liveness probe to `CUGA_TEST_HOST` (default `localhost`) with 0.5 s timeout. | benign |
| `cuga-apps/chief_of_staff/tests/conftest.py` | 8 lines: adds the `asyncio` marker to async tests. Not collected by the run used here. | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |

Also read before running: `mcp_servers/text/server.py` (pure string functions + FastMCP tool wrappers; docling/tiktoken
imported lazily inside tools), `mcp_servers/_core/serve.py` (FastMCP bootstrap), `apps/_ports.py` (constants),
`pytest.ini`, `requirements.test.txt`.

**Verdict: no malicious code found.** Safe to run the targeted test described in README.
