# AUDIT: KnockOutEZ/wigolo @ 3507bb8 (main, 2026-10-22)

`python3 tools/audit_repo.py wigolo` (1439 text files):

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| npm lifecycle hooks | none in the root package; installed with `npm ci --ignore-scripts` | benign |
| `npm rebuild better-sqlite3` | ran that one dependency's install script (prebuilt native binary for better-sqlite3 from its GitHub release), needed by the DB unit tests | benign, standard dependency |
| pytest conftests (sdks/python, packages/*) | spawn a local wigolo daemon and poll `/health`; not run | benign (not run) |
| raw-ip-url ×49 (`169.254.169.254`, `127.x`, `172.x`) | SSRF-guard tests and docs; the tool is a scraper with SSRF protection | benign |
| destructive `rm -rf /` | string fixture in `searxng/docker.test.ts` asserting shell-escaping of a container name | benign |
| env-dump ×3 | Python SDK passes `os.environ` to its child; a test asserts env is not mutated | benign |
| pipe-to-shell ×6 | their own `curl \| sh` installer docs/uninstall text; not run | benign |
| Committed binaries | none | benign |

Ran: `npm run lint` (tsc), `vitest run tests/unit`, `vitest run tests/integration/fetch/browser-pool.test.ts` (launches local headless Chromium against a 127.0.0.1 test server).

Verdict: nothing suspicious.
