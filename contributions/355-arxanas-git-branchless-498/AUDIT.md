# Malicious-code audit — arxanas/git-branchless @ 03d6ab8 (master, 2026-07-15; re-checked HEAD unchanged 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/w6-git-branchless-498` (209 text files scanned), then manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `git-branchless-revset/build.rs` (only build script in the workspace) | 3 lines: `lalrpop::process_root().unwrap()` — generates the parser from `grammar.lalrpop` | benign |
| proc-macros / `build =` overrides / `.cargo/config*` | none in the workspace (no `proc-macro = true`, no custom `build =`, no `.cargo/` dir) | — |
| `Cargo.toml` dependencies | all from crates.io or workspace `path =` crates; no `git =` sources, no `[patch]` | benign |
| `secret-paths` hits in `git-branchless-submit/tests/test_github_forge.rs` (`Local state:`) | text inside insta snapshot strings of a mocked GitHub forge test | benign (false positive) |
| `git-branchless-lib/src/testing.rs` (test harness) | creates temp repos and runs the `git` binary from `TEST_GIT` / PATH; no network | benign |
| `.github/workflows/*.yml` | build git from source (linux), `cargo build/test/fmt/clippy/doc`; not run locally | benign |
| `.devcontainer`, `.gitpod.yml`, `.vscode/settings.json`, `flake.nix` | dev-environment config; not used here | benign |
| npm lifecycle hooks / committed binaries | none | — |

Verdict: **no malicious code found**; safe to build and run the `git-branchless-revset` tests locally (CARGO_TARGET_DIR inside the work dir).
