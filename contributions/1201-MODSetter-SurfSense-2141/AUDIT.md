# Audit — MODSetter/SurfSense (branch `dev` @ bbfa32a, 2026-10-01)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/SurfSense-2141` (5232 text files scanned).
Only `surfsense_local/frontend` is installed/run for this contribution (pnpm install + vitest/eslint/tsc/prettier). Nothing in the Python backends, plugins, docker or electron trees is executed.

| Hit | Reviewed | Verdict |
|---|---|---|
| Many `conftest.py` files (surfsense_backend, surfsense_local/backend, plugins/core) | Not executed (no pytest run). Spot-checked plugins/core conftests: spawn the local CLI/app via `subprocess`, probe a free port with `socket`, poll `http://127.0.0.1/.../health` | benign test harness; not run |
| `.pre-commit-config.yaml` | Not installed / not run | n/a |
| network-call / process-spawn (plugins/core/*/conftest.py) | localhost-only health probes and starting the app under test | benign |
| pipe-to-shell (docker/scripts/install.sh, migrate-database.sh) | Usage text documenting `curl … install.sh \| bash` from the project's own raw URL | benign docs; not run |
| powershell-download (install.ps1, surfsense_web downloadFile, lockfile hash) | Installer fetching project files from its own repo; UI download helper; false-positive in integrity hash | benign |
| raw-ip-url (169.254.169.254 etc.) | SSRF guard and its tests (`net_guard.py`) — blocking metadata endpoint | benign (security code) |
| env dump (`environment = dict(os.environ)`, electron supervisor test) | Passing env to child processes in tests | benign |
| secret-paths | Comments mentioning "local state", Dockerfile copying `.npmrc*` | false positives |
| `surfsense_local/frontend/package.json` | No `preinstall`/`install`/`postinstall`/`prepare` scripts. `test` = `pnpm translations && vitest run` (formatjs extract/compile of local files) | benign |
| `surfsense_local/frontend/pnpm-workspace.yaml` | `allowBuilds: esbuild: true, msw: false` — only esbuild's standard postinstall binary selection runs | benign |
| `vite.config.ts` / `src/test-setup.ts` | Plugins formatjs/react/tailwind; setup file only stubs two jsdom DOM APIs | benign |

Verdict: **no malicious code found**; safe to install and test the frontend package.
