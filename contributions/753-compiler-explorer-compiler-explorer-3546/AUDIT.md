# Audit — compiler-explorer/compiler-explorer @ 4fac2f0d (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/compiler-explorer` (1872 text files scanned) + manual review of install/build/test hooks.

| Hit | Reviewed | Verdict |
|---|---|---|
| package.json `prepare = husky` | Only installs git hooks into `.husky/`; no network or downloads | benign |
| .husky/pre-commit | `make prereqs` (= `npm clean-install`), `npx lint-staged`, `check-frontend-imports.js`, `check-license-headers.js` — all local repo checks | benign (we won't commit through the hook in our clone anyway, or it just runs lint/ts-check/vitest) |
| lint-staged.config.mjs | Runs `npm run lint` (biome), `ts-check`, `vitest related` | benign |
| vitest.config.ts | Two projects (unit `test/**/*.ts`, frontend `static/tests/**`); setup files `test/_setup-fake-aws.ts` (sets fake AWS credentials) and `test/_setup-log.ts` (silences logger) | benign |
| etc/scripts/ce-properties-wizard/run.sh:29 `curl … astral.sh/uv/install.sh \| sh` | Optional interactive wizard installing the official uv installer when missing; never run by npm/test/build | benign / not run |
| Committed binaries | none | — |

Verdict: nothing malicious. Safe to `npm ci` (with `--ignore-scripts` not needed, only husky) and run `npx vitest run test/<file>`, `npm run ts-check:backend`, `npx biome check`.
