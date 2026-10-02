# AUDIT — Rohithgilla12/data-peek @ 78a6187 (main)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/data-peek` (828 text files scanned).
Reviewed before installing/running anything.

| Hit | Reviewed | Verdict |
|---|---|---|
| vitest/playwright configs (packages/cli, apps/desktop, apps/web) | read `apps/desktop/vitest.config.ts`: node env, include globs, path aliases only, no setupFiles | benign |
| root `postinstall`: `pnpm --filter @data-peek/desktop exec electron-builder install-app-deps \|\| true` | standard native-module rebuild for Electron | benign; skipped anyway via `--ignore-scripts` |
| `apps/desktop` `postinstall`: `electron-builder install-app-deps \|\| true` | same | benign; skipped |
| `apps/docs` `postinstall`: `fumadocs-mdx` | docs codegen, not installed (filtered install) | benign |
| powershell-download: `install.ps1:27` | official installer downloading the release asset from GitHub releases; not executed | benign |
| powershell-download: `downloadFile(...)` in `lib/export.ts` / webapp | false positive (browser Blob download helper) | benign |
| secret-paths (9) | test fixtures/placeholders (`~/.ssh/id_rsa` placeholder), comments containing "local state", `SET LOCAL statement_timeout` SQL | benign (false positives) |
| Committed binaries | none | — |

Verdict: **no malicious code found**. Install was done with `--ignore-scripts` and `ELECTRON_SKIP_BINARY_DOWNLOAD=1`; only vitest / tsc / eslint / prettier were run.
