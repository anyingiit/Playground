# Malicious-code audit — ProjectMirador/mirador @ b4602a7 (main, shallow clone)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/mirador` (664 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `vitest.config.ts` (auto-executing test config) | read in full: vitest config (react plugin, happy-dom, `@tests` alias, `setupTest.js`) | benign |
| `setupTest.js` (test setup file, not flagged but runs on test) | read in full: jest-dom, fetch mock, Path2D/fullscreen stubs, i18next init | benign |
| npm lifecycle hooks | none in package.json (`build`, `lint`, `test`, ... only) | benign |
| `scripts/container-lint.js`, `scripts/i18n-lint.js` (run by `npm run lint`) | read: glob + fs read of `src/containers` / `src/locales`, console output only; no network/exec | benign |
| `.npmrc` | only `legacy-peer-deps=true` | benign |
| `.github/workflows/node.js.yml` | npm ci, npm test --coverage, codecov upload (CI only) | benign |
| Committed binaries | none | — |
| Pattern findings | none | — |

Dependencies installed with `npm ci --ignore-scripts` (no dependency install scripts executed).

**Verdict: no malicious code found; safe to install/test.**
