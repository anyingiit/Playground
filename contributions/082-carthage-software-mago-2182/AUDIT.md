# AUDIT — carthage-software/mago @ 9608b8c (shallow clone 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/mago` — 2448 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| `build.rs` (root cargo build script) | Read fully: sets `TARGET` env, builds `mago_prelude::Prelude` in a thread and writes `prelude.bin` to `OUT_DIR`. No network, no process spawning. | benign |
| `crates/wasm/build.rs` | Same as root build.rs (prelude encode to OUT_DIR). | benign |
| `crates/prelude/src/build.rs` | Not a cargo build script — it is a library module gated by the `build` feature (Cargo.toml `build = [...]`); grep shows no `Command`, network or env access. | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| Pattern findings | none | n/a |

Also reviewed: `Justfile` (`test`/`check` recipes only call cargo and `cargo run -- fmt/lint/analyze`), `.github/workflows/commit-authorship.yml` (CI check, not run locally).

Verdict: **no malicious code found**; safe to build/test. Only the `mago-formatter` crate tests (+ `cargo fmt`/`clippy` on it) are run here.
