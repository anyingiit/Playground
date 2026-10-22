# AUDIT: XAGI-Lab/melra @ 330625b (main, 2026-10-22)

`python3 tools/audit_repo.py melra` (306 text files). Ran `pnpm install --frozen-lockfile --ignore-scripts`, `pnpm build`, `apps/cli` vitest/tsc, and the docs scripts.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `packages/browser-runtime/vitest.config.ts` | test config only; that package's tests were not run | benign |
| npm lifecycle hooks | none; install used `--ignore-scripts` | benign |
| env-dump (`sdk-ts/src/index.test.ts:292`) | test writes a child's env to a temp file to assert isolation | benign (not run) |
| pipe-to-shell (`approval-console.test.ts:873`) | string fixture of a dangerous write the policy must block | benign |
| raw-ip-url `169.254.169.254` ×4 | SSRF test fixtures asserting the metadata IP is blocked | benign |
| secret-paths (`.npmrc` mentions) | Dockerfile copy and policy comments | benign |
| Committed binaries | none | benign |
| Scripts run (`check-env-docs`, `check-links`, `check-changelog`, `check-readme-examples`, `check-dist`, `run-recursive`) | read repo files / run tsc and vitest; no network, no writes outside repo | benign |

Verdict: nothing suspicious; this is a security-focused project and the hits are its own guardrail fixtures.
