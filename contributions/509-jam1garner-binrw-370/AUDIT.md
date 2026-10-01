# Audit — jam1garner/binrw @ 585d481 (2026-10-01)

`python3 tools/audit_repo.py /home/user/work/binrw` (183 text files).

| Hit | Reviewed | Verdict |
|---|---|---|
| binrw/build.rs, binrw_derive/build.rs (identical) — `Command::new(rustc)` | Runs `$RUSTC --version`, emits `cargo:rustc-check-cfg` / `rustc-cfg=nightly` only | benign |
| binrw/tests/derive/data/test_file.bin (128 B), deref_now.bin (32 B) | small test fixtures read by tests | benign |
| Dependencies | crates.io only: array-init, bytemuck, either, owo-colors, proc-macro2, quote, syn; dev: modular-bitfield, trybuild, runtime-macros | standard, benign |

No npm hooks, no network access at build/test time. **Verdict: safe to build/test.**
