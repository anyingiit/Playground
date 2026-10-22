# AUDIT: open-nexus-OS/open-nexus-OS @ 9a81e5a (main, 2026-10-22)

`python3 tools/audit_repo.py onx`:

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Committed binaries (10) | `source/kernel/neuron/tests/vectors/ipc_header_v1.bin` (13 B test vector) and `docs/board/measurements/**` register/EDID dumps | benign, data only, never executed |
| pipe-to-shell `podman/Containerfile:50` | `curl https://sh.rustup.rs \| sh`, the standard rustup install in their dev container; not run | benign |
| secret-paths ×6 | all match "local state" in comments | false positives |
| build scripts run | `tools/nxs-pack/build.rs` and `userspace/nexus-idl-runtime/build.rs`: `capnpc` compiling in-repo `.capnp` schemas into `OUT_DIR` | benign |

Ran only `cargo test`/`clippy` on the `nxs-pack` crate (pinned `nightly-2025-01-15`), `cargo fmt --check` with their config, and `scripts/check-structure.sh` (read-only `find`/`wc`). No QEMU, no `just`, no OS build.

Verdict: nothing suspicious.
