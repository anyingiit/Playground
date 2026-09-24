# AUDIT — DioxusLabs/taffy (HEAD at clone time, 2026-09-24)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/taffy`

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs, npm hooks) | none found (`find . -name build.rs` empty, no package.json) | n/a |
| Committed binaries | none | n/a |
| Pattern findings (process-spawn, network, obfuscation…) | none | n/a |
| `justfile` | only `cargo run/bench/clippy/fmt` wrappers; `gentest`/`getchrome` download Chrome for Testing into `.chrome-for-testing` — **not run** for this doc-only change | Benign |
| `scripts/*` (gentest, getchrome, import-yoga-tests, format-fixtures) | workspace dev tools only invoked via `just`; not built/run by `cargo build`/`cargo test` of the root crate | Benign / not executed |
| `.github/workflows/ci.yml` | plain `cargo build` / `cargo test --tests` feature matrix | Benign |

Verdict: nothing malicious; safe to build, test and `cargo doc` the `taffy` crate.
