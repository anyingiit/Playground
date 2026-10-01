# AUDIT — pmxt-dev/pmxt @ 4a367d81 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/pmxt` — 580 text files scanned. No npm lifecycle hooks, no committed binaries.

| Hit | Reviewed | Verdict |
|---|---|---|
| `sdks/typescript/jest.config.cjs`, `core/jest.config.js` (test runner config) | read | benign — standard ts-jest config; not executed here (only the Python SDK tests were run) |
| `core/jest.config.js:10` network-call | read | benign — `transformIgnorePatterns` regex listing package names (`axios`, `ky`, ...), no network access |
| `.github/workflows/sync-mcp.yml:69` secret-paths | read | benign — CI publish step writes an npm auth token from `NODE_AUTH_TOKEN` secret; not run locally |
| `sdks/python/tests/*`, `pytest.ini` (no `conftest.py`) | reviewed what pytest loads | benign — unit tests with mocked transports; `addopts = -m "not integration"` keeps sidecar tests off |

Only code executed locally: `pip install -e sdks/python` (setuptools, no custom setup.py) + `pytest` in `sdks/python`. Verdict: **no malicious code found**.
