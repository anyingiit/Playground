# Malicious-code audit — smol-machines/smolvm @ c890ec3 (shallow clone)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/smolvm` (443 text files) + manual review.
Scope of what was executed locally: `cargo build/test/clippy/fmt` for the root `smolvm` crate only
(this runs the root `build.rs` and build scripts of crates.io dependencies / workspace path deps).

| Hit | Reviewed | Verdict |
|---|---|---|
| `build.rs` (root, runs on build/test) | Read fully. On Linux `main()` does nothing: every action (placeholder Mach-O section, `link_libkrun`, `install_name_tool`, `codesign`, optional `cargo build` of the libkrun submodule behind `LIBKRUN_BUILD`) is `#[cfg(target_os = "macos")]` and gated on `CARGO_CFG_TARGET_OS == "macos"`. | Benign |
| `crates/smolvm-cuda/build.rs` | Hashes a fixed list of local source files with FNV-1a and emits `SMOLVM_PROTO_HASH`. No I/O beyond reading those files. | Benign |
| `crates/smolvm-cuda-shim/build.rs`, `crates/smolvm-cudart-shim/build.rs` | Only emit `-Wl,-soname,...` linker args for linux targets. | Benign |
| `sdks/node/smolvm-embedded/vitest.config.ts` | JS SDK test config; not executed (no npm used). | Not run / benign |
| Committed "binaries" `lib/**/libkrun*.{so,dylib,dll}` etc. (132–133 bytes) | They are Git LFS pointer text files (`version https://git-lfs.github.com/spec/v1 ...`), not real binaries; LFS objects were not fetched. Linux loads libkrun via `dlopen` at runtime only. | Benign |
| pipe-to-shell in `scripts/build-libkrun-linux.sh` (rustup installer) and `scripts/install.sh` (usage comments/help text for the project's own installer) | Release/dev scripts, not invoked by cargo build/test. | Benign, not run |
| `Command::new(...)` in `build.rs` (install_name_tool, codesign, cargo) | macOS-only paths (see above). | Benign |
| raw-IP URLs (`100.96.0.1` guest gateway, `169.254.169.254` in an SSRF-refusal unit test, `1.1.1.1` default connectivity-test target) | Product/test constants; the metadata URL is in a test asserting it is *refused*. | Benign |
| "reverse-shell" `tests/test_network.sh:727` `/dev/tcp/127.0.0.1/$proxy_port` | Localhost port-probe in an integration shell test (needs KVM; not run). | Benign, not run |
| secret-paths (`~/.docker/config.json` docs in `src/docker_config.rs`; `local state` false positives) | Documented registry-credential lookup feature for image pulls; no exfiltration. Not exercised by the tests run. | Benign |

**Verdict: nothing malicious found; safe to build and run the unit tests of the root crate.**
