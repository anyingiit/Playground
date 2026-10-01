# AUDIT — reticlehq/reticle @ 14085e6 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/reticle` — 2799 text files scanned, 0 committed binaries.

| Hit | Reviewed | Verdict |
|---|---|---|
| `vitest.config.ts`, `init/vitest.config.ts`, other `*/vitest.config.ts`, `vitest.shared.ts` | Read | Benign — only test options, tsconfig-paths plugin, alias of `@reticlehq/core` to source. |
| `test/global-setup.ts` | Read | Benign — probes local ports with `net.createServer`, makes a temp dir; no network/exec. Not used by `init` unit tests. |
| `adapters/realm/browser/vitest.setup.ts` | Not run (other package) | Not executed for this change. |
| `apps/tauri-smoke/src-tauri/build.rs` | Not built | Standard tauri build script; not run. |
| `apps/electron-vue-pinia/package.json` postinstall `electron-builder install-app-deps` | Inspected | Standard electron step; fixture app — install done with `--ignore-scripts` / filtered to `init` deps so it is not executed. |
| root `package.json` scripts | Read | No `preinstall`/`postinstall`/`prepare` at root; `hooks:install` only symlinks repo hooks (not run). |
| pipe-to-shell (8) | Read | All comments/docs about the project's own `curl \| sh` installer (`install/install.sh`); not executed. |
| secret-paths (19) | Read | Deny-lists for `.npmrc`/`.env`, gitignore entries, local verdaccio script for gates; no exfiltration. Not executed. |

Verdict: **no malicious code found**. Only `init` package unit tests, eslint, prettier and tsc are run.
