# Audit — conventional-changelog/commitlint @ 0737aba (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/commitlint` (581 text files) + manual review of lifecycle scripts and hooks.

| Hit | Reviewed | Verdict |
|---|---|---|
| `package.json` `"prepare": "husky"` (only lifecycle script in the whole workspace; checked every `package.json` for install/prepare/prepack) | husky 9 only sets `core.hooksPath` to `.husky/_` | benign; install was run with `--ignore-scripts` anyway, so no git hooks were installed |
| `.husky/pre-commit` (`pnpm lint-staged`), `.husky/commit-msg` (`pnpm build` + `node @commitlint/cli/lib/cli.js --edit $1`) | Only repo-local tooling | benign; not active here (hooks not installed, commits made with `core.hooksPath=/dev/null`) |
| `vitest.config.ts` | Test runner config; custom env `vitest-environment-commitlint` = `@packages/test-environment` (local workspace package, creates tmp dirs) | benign |
| `pnpm-workspace.yaml:13` "secret-paths" pattern | False positive: a comment about supply-chain hardening. The file sets `allowBuilds` (all false), `strictDepBuilds: true`, `minimumReleaseAge: 2880` | benign (hardening) |
| Committed binaries | none | — |

Commands run after the audit: `pnpm install --frozen-lockfile --ignore-scripts --store-dir /home/user/work/commitlint/.pnpm-store`, `pnpm build` (`tsc -b`), `pnpm vitest run --maxWorkers=2 …`, `pnpm format` (oxfmt --check), `pnpm lint` (oxlint), local `@commitlint/cli/lib/cli.js`.

Verdict: nothing malicious; safe to install/build/test.
