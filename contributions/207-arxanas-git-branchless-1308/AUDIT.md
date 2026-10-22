# Malicious-code audit — arxanas/git-branchless @ 03d6ab8 (master, 2026-07-15; HEAD unchanged on 2026-10-22)

Tool: `python3 -I $PG/tools/audit_repo.py <clone>` (209 text files scanned), then manual review. HEAD is the same commit audited for contribution 058; re-checked the hits below.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `git-branchless-revset/build.rs` (only build script) | 3 lines: `lalrpop::process_root().unwrap()` — generates the parser from `grammar.lalrpop` | benign |
| proc-macros / `.cargo/config*` / `git =` deps / `[patch]` | none | — |
| `secret-paths` hits in `git-branchless-submit/tests/test_github_forge.rs` (`Local state:`) | text inside insta snapshot strings | benign (false positive) |
| `git-branchless-lib/src/testing.rs` (test harness) | creates temp repos, runs `git` from `TEST_GIT`/PATH; no network | benign |
| `.github/workflows/*.yml`, `flake.nix`, devcontainer | CI / dev env config, not run locally | benign |
| npm lifecycle hooks / committed binaries | none | — |

Verdict: **no malicious code found**; safe to build and run targeted crate tests with `CARGO_TARGET_DIR` inside the work dir.
