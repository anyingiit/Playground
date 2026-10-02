# AUDIT — uutils/acl @ 2340e96 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/acl`: 22 text files, 0 pattern findings, 0 committed binaries, no npm hooks.

| Hit | Reviewed | Verdict |
|---|---|---|
| `build.rs` (cargo build script) | Read in full: reads `CARGO_FEATURE_*` env vars, writes `uutils_map.rs` into `OUT_DIR` via `phf_codegen`. No network, no process spawn, no writes outside OUT_DIR. | benign (standard uutils multicall map generator) |
| `util/` scripts | Not invoked by `cargo build/test/fmt/clippy`; not run. | n/a |
| Cargo dependencies | crates.io only (clap, uucore, uutests, xattr, uzers, phf, tempfile …), no git/path deps outside repo. | benign |

Conclusion: safe to build and test.
