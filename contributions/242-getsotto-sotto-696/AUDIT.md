# AUDIT: getsotto/sotto @ 88b204b (main, 2026-10-22)

`python3 tools/audit_repo.py sotto` (389 text files). Only the `web/` package was installed and run (`npm ci --ignore-scripts`, then vitest/tsc).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `web/vitest.config.ts` | react plugin + happy-dom, `include: src/**/*.test.tsx`, no setup files | benign |
| `web/playwright.config.ts`, `web/e2e/global-setup.ts` | e2e only, not run | not executed |
| `crates/server/build.rs` | Rust crate, not built in this task | not executed |
| npm lifecycle hooks | none in web/package.json; install ran with `--ignore-scripts` anyway | benign |
| env-dump hits (`dict(os.environ)` ×12) | Python ops/test scripts pass env to subprocesses; not run | benign |
| Committed binaries | none | benign |
| Dependencies | react, react-dom; dev: vite, vitest, testing-library, happy-dom, typescript, playwright (lockfile, all well-known) | benign |

Verdict: nothing suspicious; safe to run the web unit tests.
