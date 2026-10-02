# AUDIT — mochajs/mocha @ 79db2ee (main, 2026-10-01)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/mocha` (543 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| npm lifecycle hooks | none in root package.json (only `prepublishOnly`, `pretest-browser:playwright`, `prelint` scripts, none run on install); installed with `npm ci --ignore-scripts` as CI does | benign |
| `playwright.config.js` | standard Playwright config for browser tests (not run here) | benign |
| `test/browser/global-setup.js` | bundles `test/browser-specific/setup.cjs` with Rollup for the browser; no network/exec | benign |
| `test/integration/fixtures/plugins/global-fixtures/*.fixture.cjs` | test fixtures that only `console.log` / throw for mocha global-fixture tests | benign |
| `.mocharc.yml` → `test/setup.cjs` | sets up `unexpected` assertion library globals | benign |
| Committed binaries | none | — |
| Pattern findings | none | — |

Verdict: **no malicious code found**; safe to install (`npm ci --ignore-scripts`) and run unit tests.
