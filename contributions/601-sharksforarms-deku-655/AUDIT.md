# AUDIT — sharksforarms/deku @ 1d3258a

`python3 tools/audit_repo.py /home/user/work/deku` (131 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs / hooks) | none found; `find -name build.rs` empty | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |

Manual: proc-macro crate `deku-derive` runs at compile time; reviewed the touched file
`deku-derive/src/macros/deku_write.rs` — only token generation, no I/O/network. Dev-deps are
standard crates.io crates. Verdict: **safe to build/test**.
