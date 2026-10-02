# Audit — OpsiMate/OpsiMate @ 7593155 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/OpsiMate` + manual review of install/test hooks.

| Hit | Reviewed | Verdict |
|---|---|---|
| root `package.json` `prepare: husky \|\| exit 0` | Only installs the git pre-commit hook | benign |
| `.husky/pre-commit` | `pnpm exec lint-staged` → `prettier --write --ignore-unknown` on staged files | benign (patch committed with plain git; hook not triggered by format-patch flow) |
| `apps/server/vitest.config.ts` | node env, `pool: 'forks'`, setupFiles `tests/setup.ts`, path alias to `packages/shared/src` | benign |
| `apps/server/tests/setup.ts` | In-memory better-sqlite3 DB, express app via supertest, registers a local test user; no network | benign |
| `apps/server/vitest.config.ts`/`apps/client/vitest.config.ts` | Test runner configs, nothing downloaded | benign |
| raw-ip-url `aiConfig.test.ts:192`, `rootCause.test.ts:190` (169.254.169.254) | Test inputs asserting SSRF rejection; never fetched | benign |
| secret-paths (`.gitignore .npmrc`, "local state" comments) | False positives | benign |
| Committed binaries | none | — |
| No other `preinstall`/`postinstall` in workspace package.json files | dependency install scripts (better-sqlite3 prebuilt binary, esbuild) are standard | benign |

Verdict: nothing malicious; safe to run `pnpm install`, vitest, eslint and prettier for `apps/server`.
