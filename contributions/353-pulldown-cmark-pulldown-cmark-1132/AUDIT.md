# Malicious-code audit — pulldown-cmark/pulldown-cmark @ c61583e (master)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/w6-pulldown-cmark-1132` (95 text files), then manual review. Done before building or running anything.

| Hit | Reviewed | Verdict |
|---|---|---|
| `pulldown-cmark/build.rs` (only build script in the repo) | 389 lines. Without the `gen-tests` feature it is an empty function. With `gen-tests` it reads `specs/*.txt` and `third_party/**/*.txt` and writes `tests/suite/*.rs` test files. No process spawning, no network, no env-var exfiltration | benign |
| `dos-fuzzer/src/main.rs` `Command::new(&args[0]).exec()` | the fuzzer re-execs itself after a thread timeout; it only runs in the CI `regression` job (`cargo run --release -- --regressions`) | benign |
| `guide/prepare-demo.rs` `Command::new("cargo")` | builds the wasm demo for the mdBook guide; not part of build or test | benign |
| proc-macros / npm hooks / committed binaries | none | — |
| `.github/workflows/rust.yml` | fmt, build, test with feature matrices, dos-fuzzer regressions, bench check, wasm build | benign |
| Dependencies (`bitflags`, `unicase`, `memchr`, `getopts`, dev: `regex`, `serde_json`, `bincode`) | well-known crates.io crates from the committed Cargo.lock | benign |

Verdict: **no malicious code found**. Safe to run `cargo test` with `CARGO_TARGET_DIR` under the work dir.
