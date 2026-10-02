# Malicious-code audit — microsoft/litebox @ 9b8d757 (main)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/litebox` (297 text files scanned), then manual review of every hit and of everything that runs during `cargo build/clippy/test` for the crates exercised here (`litebox`, `litebox_platform_linux_kernel`, `litebox_common_linux`).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `litebox_platform_linux_kernel/build.rs` | Read in full: runs `bindgen` on the in-repo headers `src/host/snp/wrapper.h` / `snp-sandbox.h` and writes `$OUT_DIR/bindings.rs`. No network, no process spawning besides libclang, no file writes outside `OUT_DIR`. | benign |
| `litebox_shim_linux/build.rs`, `litebox_runner_linux_on_windows_userland/build.rs` | Empty `main()` (comment only: makes cargo set `OUT_DIR`). | benign |
| `litebox_runner_linux_on_windows_userland/tests/test-bins/litebox_rtld_audit.so` (14 KB) | Committed test fixture for the Windows runner tests (last touched by #919). Not built, loaded or executed by any command run here (we only build/test `litebox`, `litebox_common_linux`, `litebox_platform_linux_kernel` on Linux). | benign / not executed |
| secret-paths: `litebox_runner_lvbs/src/lib.rs:744` | A comment about "session-local state"; false positive. | benign |
| `.github/tools/github_actions_run_cargo` | Bash wrapper: runs `cargo build/check/clippy/fmt/test/nextest/doc` with `--locked` and pipes JSON diagnostics through `jq` into GitHub annotations. No downloads or side effects. Not needed locally (commands run directly). | benign |
| `.github/workflows/*.yml`, `copilot-setup-steps.yml` | CI only: rustup, nextest install, `sudo tun-setup.sh`, apt installs. None of it is run here. | benign / not executed |
| Dependencies (`litebox/Cargo.toml`) | crates.io deps (`buddy_system_allocator 0.11`, `spin`, `smoltcp`, `hashbrown`, ...) + one pinned git dep `gz/rust-slabmalloc@19480b2` (the well-known slabmalloc author's repo). `Cargo.lock` is committed; builds use `--locked`. No proc-macro / build script of note in `litebox` itself. | benign |
| No `.cargo/config.toml`, no npm/python hooks | `rust-toolchain.toml` just pins `stable`. | benign |

Conclusion: nothing malicious found; safe to build and test.
