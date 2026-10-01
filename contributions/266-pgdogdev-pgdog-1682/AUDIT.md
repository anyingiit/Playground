# Malicious-code audit — pgdogdev/pgdog @ 80d6059 (main)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pgdog` (1127 text files scanned), then manual review of every hit and of everything that runs during `cargo build` / `cargo test`.

| Hit | Reviewed | Verdict |
|---|---|---|
| `pgdog/build.rs` (build script; `Command::new("git").args(["rev-parse","HEAD"])`) | compiles the in-tree `src/frontend/router/sharding/hashfn.c` (Postgres hash function port, only `#include <stdint.h>`) via `cc`, and reads the git hash into `GIT_HASH` env | benign |
| `pgdog-plugin/build.rs` (`Command::new($RUSTC).arg("--version")`) | records rustc version into `RUSTC_VERSION` env | benign |
| `pgdog-macros` (proc-macro crate, 144 lines) | pure token manipulation; no fs/net/process/env access | benign |
| secret-paths x4: `integration/python/test_session_mode.py:130,310`, `integration/python/test_asyncpg.py:554,658` | false positives: SQL `SET LOCAL statement_timeout` strings in integration tests (not run here) | benign |
| `.cargo/config.toml` | rustflags `--cfg tokio_unstable`, clang+mold linker, `RUST_MIN_STACK` env; no runners/aliases | benign (mold not installed here, so `RUSTFLAGS="--cfg tokio_unstable"` is set to drop the mold link arg) |
| git dependencies (`pg_raw_parse`, `scram`, pinned revs under github.com/pgdogdev) | first-party forks pinned by commit | benign |
| `.github/workflows/*`, `integration/ci/*.sh` | CI only (apt-get postgres, docker, cargo llvm-cov nextest); not executed locally | benign |
| npm lifecycle hooks / committed binaries | none | — |

Verdict: **no malicious code found**. Only `cargo build`/`cargo test` of the `pgdog` crate's unit tests is run locally (CARGO_TARGET_DIR inside the clone, 2 jobs).
