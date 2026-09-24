# Malicious-code audit — uutils/coreutils @ 76774a6

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/coreutils` (1035 text files scanned), run **before** any `cargo` build/test. Every hit was then reviewed by hand.

| Hit | Reviewed | Verdict |
|---|---|---|
| `build.rs` (root, runs on build) | Read in full: emits `cargo:rerun-if-changed`/`rustc-cfg`, turns enabled `CARGO_FEATURE_*` into a generated `uutils_map.rs` in `OUT_DIR`. Its only "network" hit is a `cargo:warning` **string** telling users how to curl the tldr archive; nothing is downloaded | benign |
| `src/uucore/build.rs` | Generates `embedded_locales.rs` in `OUT_DIR` from the repo's own `locales/*.ftl` files; no process spawn, no network | benign |
| `src/uu/stty/build.rs` | Only `cfg_aliases!` for BSD targets | benign |
| `src/uu/stdbuf/build.rs` (process-spawn) | Runs `$CARGO build` on the in-repo `src/libstdbuf` crate so `include_bytes!` can embed `libstdbuf.so`, then copies/symlinks it inside `target/`. Uses the inherited environment, no network, no writes outside `OUT_DIR`/`target` | benign (not built here: only the `who` feature was compiled) |
| `src/uu/stdbuf/src/libstdbuf/build.rs` | Linker args only (`-fPIC`, `-z defs`) | benign |
| `.pre-commit-config.yaml` | Standard hooks (pre-commit-hooks, fluent linter, cspell, cargo fmt/clippy); only runs if a contributor installs pre-commit. Not run here | benign |
| `util/android-commands.sh:429` (secret-paths: `cat ~/.ssh/id_rsa.pub`) | Manual helper for the Android emulator CI job: pushes the **public** key into the emulator's `authorized_keys`. Not called by build or tests | benign |
| `src/uu/factor/benches/factor_bench.rs:88` (long base64 blob) | A long decimal number literal used as benchmark input, not base64 | benign |
| `tests/fixtures/join/non-unicode_{1,2}.bin` (7/9 bytes) | Tiny invalid-UTF-8 fixtures for `join` tests | benign |
| npm lifecycle hooks | none | n/a |

Also checked by hand: `tests/uutests` (test harness crate) spawns only the built `coreutils` binary and, for GNU-comparison tests, the system `who`. Nothing fetched from the network during `cargo test`.

**Verdict: no malicious code found; safe to build and test.**
