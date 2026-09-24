# Malicious-code audit — ulyssa/iamb @ a99b116

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/iamb-617` (42 text files scanned) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `build.rs` (runs on build/test) | 8 lines: `vergen_gitcl` emits the git SHA as a cargo env var (`Gitcl::builder().sha(true)`). No network, no file writes outside `OUT_DIR`. | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| Pattern findings (curl/eval/base64/etc.) | none | n/a |
| Dependencies | `Cargo.toml` has only commented-out `git =` lines (modalkit); `Cargo.lock` has no `source = "git+…"` entries — all 772 packages come from crates.io. | benign |
| `.envrc` | `use flake` (direnv; not used here) | benign |
| CI (`.github/workflows/ci.yml`, `check-imports-format.sh`) | fmt / import-format sed script / clippy / `cargo test --locked`; the sed script only reads `src/*.rs` | benign |

Verdict: nothing suspicious; safe to build and run `cargo test`.
