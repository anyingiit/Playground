# AUDIT — reticlehq/reticle @ 14085e6 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/reticle` — 2799 text files, 0 committed binaries.
Reviewed before running anything. Install was done with `pnpm install --frozen-lockfile --ignore-scripts`.

| Hit | Reviewed | Verdict |
|---|---|---|
| `*/vitest.config.ts` (root, init, core, server, engine, …) | read `init/vitest.config.ts` + `vitest.shared.ts` | benign — aliases/timeouts only |
| `test/global-setup.ts` | read | benign — probes local ports, creates tmp state dir (integration config only, not run) |
| `adapters/realm/browser/vitest.setup.ts` | not executed (browser package tests not run) | n/a |
| `apps/tauri-smoke/src-tauri/build.rs` | Rust fixture, never built | not run |
| `apps/electron-vue-pinia` postinstall `electron-builder install-app-deps` | standard electron-builder hook; skipped via `--ignore-scripts` | benign |
| pipe-to-shell ×8 | all comments / the project's own documented `install.sh` usage line | benign |
| secret-paths ×19 | `.npmrc` mentions in a deny-list, gitignore, tests and the local Verdaccio helper script (`scripts/local-registry.sh`, writes a localhost token only when invoked manually) | benign, not run |

Verdict: no malicious code found. Commands run: `pnpm install --ignore-scripts`, turbo build of `@reticlehq/core` + `@reticlehq/eslint-plugin`, init lint/typecheck/vitest, prettier, `scripts/check-boundaries.mjs`, `scripts/check-lossy-transforms.mjs`.
