# AUDIT — lycheeverse/lychee (HEAD 2c1fb3a, 2026-09-21)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/lychee` (243 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `lychee-bin/build.rs` (cargo build script) | Runs `git show --no-patch --format=%cs HEAD` in the crate dir and exports `GIT_DATE` via `cargo:rustc-env` for the man page | Benign |
| `lychee-bin/build.rs:1,15` process-spawn | Same `git show` call as above; no network, no file writes | Benign |
| `.cargo/config.toml` | Only `rustflags = ["--cfg", "tokio_unstable"]` (tokio-console) | Benign |
| raw-ip-url `valid.rs:294`, `filter/mod.rs:284-285` | Test constants for loopback / link-local filtering (127.0.0.0, 169.254.x.x) | Benign |
| Committed binaries `fixtures/fragments/zero.bin` (2 B), `fixtures/dump_inputs/subfolder/example.bin` (0 B) | Tiny test fixtures | Benign |
| npm lifecycle hooks | none | n/a |
| Makefile `test`/`lint` | `cargo nextest`/`cargo test`/`cargo fmt`/`cargo clippy` only; `scripts/update_readme.py` only runs `lychee --help` and rewrites README | Benign |

Verdict: nothing malicious found; safe to build and test.
