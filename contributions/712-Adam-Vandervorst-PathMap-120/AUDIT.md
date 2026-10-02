# Audit — Adam-Vandervorst/PathMap @ ec818cf6 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/PathMap` + manual review of build-time code (no `build.rs` anywhere; `pathmap-derive` proc macro; `.cargo/config.toml`).

| Hit | Reviewed | Verdict |
|---|---|---|
| `.github/workflows/ci.yml:46/80/141/199/200` `curl … \| sh` | CI-only rustup / elan (Lean) bootstrap on the maintainers' self-hosted runner; not executed here | benign / not run |
| `lean/corpus/*.bin` (250–265 bytes) | Fuzz corpus inputs for the Lean differential checker; not used by `cargo build/test` | benign |
| `pathmap-derive/src/lib.rs` (proc macro, runs at compile time) | Pure `syn`/`quote` token generation for `PolyZipper` derive; no fs/net/process/env access | benign |
| `.cargo/config.toml` | Only `rustflags = -C target-cpu=native` and a riscv cross target section (linker/qemu runner, not used for x86_64) | benign |
| `src/`, `tests/`, `benches/` grep for `Command::new`/`TcpStream`/network | no hits | benign |

Verdict: nothing malicious; safe to run `cargo build` / `cargo test` / `cargo doc` / `cargo bench --no-run` on the crate.
