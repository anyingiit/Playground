# AUDIT: ZcashFoundation/zebra @ 6c0bfba (main, 2026-10-22)

`python3 tools/audit_repo.py zebra`. Only `zebra-chain` (and its dependencies from Cargo.lock) was built and tested.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `zebrad/build.rs`, `zebra-rpc/build.rs` (git/cargo `Command`s for version info / proto build) | not in zebra-chain's dependency graph; not built | not executed |
| pipe-to-shell (`scripts/install-zebra.sh` rustup install) | user-facing installer, not run | benign |
| secret-paths hits (`wallet.dat` comment, "local state" text in CI script) | plain comments/strings | benign |
| long hex hits | test vectors (transactions, block solutions) | benign |
| Dependencies | crates.io via Cargo.lock (zcash/librustzcash, RustCrypto, etc.); ZcashFoundation runs `cargo deny` + `cargo vet` (`supply-chain/`) | benign |
| Toolchain | `rust-toolchain.toml` pins 1.91.0 (official rustup download) | benign |

Verdict: nothing suspicious; safe to build and test zebra-chain.
