# AUDIT: femboypuppy/Tessera-Notes @ 2f0281d (main, 2026-10-22)

`python3 tools/audit_repo.py` result:

| Surface | Result |
|---|---|
| build.rs | `apps/desktop/src-tauri/build.rs`: Tauri command list, not built here |
| npm lifecycle hooks | root `prepare` = `node scripts/git-hooks/install.ts`: sets `core.hooksPath` to the repo's hooks (commit-msg Conventional Commits check, lint-staged); read, harmless |
| Committed binaries | none |
| Pattern findings | none |

Ran locally: `pnpm install`, `pnpm test` (vitest, jsdom), `pnpm typecheck` in packages/ui, eslint/prettier on the changed files. No network beyond the npm registry.

Verdict: nothing suspicious.
