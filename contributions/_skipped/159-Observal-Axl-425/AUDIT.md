# AUDIT — Observal/Axl @ 02cb573 (main, 2026-09-25)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/Axl-425` (539 text files), then manual review. Reviewed BEFORE running `pnpm install` or any test.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (auto-exec surface) | Standard pre-commit-hooks + local hooks running `biome check`, `scripts/check-boundaries.ts`, `scripts/check-generated.ts`, `reuse lint`. pre-commit was not installed/run. | benign |
| npm lifecycle hooks | None in any `package.json` (no preinstall/install/postinstall/prepare). `pnpm-workspace.yaml` sets `allowBuilds: esbuild: false`, so no dependency build scripts run on install. | benign |
| Committed binaries | none | benign |
| raw-ip-url `169.254.169.254` in `packages/ai/test/*.test.ts` | Test fixtures asserting that cloud-metadata endpoints are rejected (SSRF / transport-safety tests). No request is made to them in the code under test path. | benign |
| reverse-shell `/dev/tcp/127.0.0.1/...` in `packages/sandbox/test/{bubblewrap,seatbelt,oci}.test.ts` | Sandbox tests that check network isolation by trying to open a TCP socket to localhost inside the sandbox and expecting it to fail. Localhost only, no remote host. Not run here (only `packages/tui` tests run). | benign |
| secret-paths `.npmrc` in `.github/workflows/ci.yml:45` and `scripts/build-release-metadata.ts:66` | CI path filter list; release script writes an empty temp `.npmrc-release` to isolate `npm install --ignore-scripts` from user config. No secret read/exfiltration. | benign |
| Extra manual check: `packages/tui/test/productivity.test.ts` (the test file run) | Pure unit tests importing `../src/index.ts`; no network/process spawning. `packages/tui/src` uses `child_process` only in clipboard.ts / external-editor.ts / app.ts (expected TUI features: copy to clipboard, `$EDITOR`). | benign |

Verdict: no malicious code found. Safe to install the locked toolchain (`pnpm install --frozen-lockfile`) and run the TUI tests, lint, format, and typecheck.
