# Malicious-code audit — medusajs/medusa (develop @ 08f73ec7)

Tool: `python3 tools/audit_repo.py` + manual review. **Verdict: no malicious code found.**

| Hit | Location | Reviewed verdict |
|---|---|---|
| Test-runner configs (auto-exec) | ~60 `jest.config.js`, `vitest.config.ts` | Benign: all delegate to the shared `define_jest_config.js` / standard transforms; no process spawning or network (the scanner's exec/network rules found nothing in them) |
| Test global setup | `packages/medusa/setupTests.js` | Benign: sets `global.performance` and an `afterEach` that awaits `setImmediate` |
| npm lifecycle hooks | root `package.json` | none in the repo's own packages |
| "secret-paths" | 3 hits on the phrase "local state" in UI comments | False positives |
| Committed binaries | none | — |

Note: `yarn install` also runs lifecycle scripts of third-party npm dependencies (pinned by `yarn.lock`); those
are outside this repo's code. What was executed here: `yarn install`, `yarn build` + `yarn test` in `packages/core/utils`.
