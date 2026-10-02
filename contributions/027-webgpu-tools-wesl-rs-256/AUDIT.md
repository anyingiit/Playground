# Malicious-code audit — webgpu-tools/wesl-rs (main @ 2026-09-23, commit reviewed before any build)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/wesl-rs` (172 text files) + manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `crates/wesl-c/build.rs` | Runs `cbindgen` to write `include/wesl.h` | Benign (standard C-binding generation) |
| `examples/buildrs_wesl/build.rs`, `examples/random_wgsl/build.rs`, `examples/dependency-resolution/{a,b,c1,c2,d1,d2}/build.rs` | Call the crate's own `wesl::Compiler` / `wesl::PackageBuilder` on local shader dirs | Benign (the project's own documented build.rs usage) |
| `samples/binding0.bin` (640 B), `samples/binding1.bin` (4 B) | Tiny data blobs used as shader binding samples | Benign (not executable) |
| npm lifecycle hooks | none | — |
| Pattern findings (eval/base64/curl-pipe/etc.) | none | — |
| `.cargo/config` | only `xtask = "run --package xtask --"` alias | Benign |
| Git dependency `bevy-wgsl` (crates/wesl-test/Cargo.toml) | Pinned rev in the same `webgpu-tools` org, only shader sources | Benign |
| `crates/wesl-test/tests/testsuite.rs` `Command::new("git")` | `git clone/fetch/checkout` of pinned test-suite revisions (modeled after wgpu's CTS xtask) | Benign, network-only; that suite was not needed for this change |

**Verdict: no malicious code found. Safe to build/test.**
