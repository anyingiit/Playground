# AUDIT — agavra/tuicr (shallow clone of default branch, 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/tuicr` — 175 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none; no `build.rs`, no git/path deps in Cargo.toml | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| secret-paths: `src/app/comments.rs:526` | doc comment mentioning "local state" | benign (false positive) |

Tests are plain `cargo test` (unit + `tests/` integration tests using tempdirs and the local git binary). Nothing downloads or executes remote code at build/test time.

**Verdict: safe to build and test.**
