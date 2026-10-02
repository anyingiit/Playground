# AUDIT — jnsahaj/lumen @ a8447c0

`python3 tools/audit_repo.py /home/user/work/lumen` (52 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs / npm hooks / Makefile) | none present | benign |
| Committed binaries | none | benign |
| secret-paths: src/command/diff/app.rs:284,1539,1579,1609 ("local state" in comments) | comments about syncing viewed-file state | benign (false positive) |
| `.github/workflows/release.yml` | manual release workflow, SHA-pinned actions; not run by tests | benign |
| `flake.nix`, `release.sh` | nix packaging / release helper; not executed here | benign |

Only `cargo build/test/fmt/clippy` were run; dependencies come from crates.io via Cargo.lock (plus one new crate `tree-sitter-php`, whose build.rs only compiles the bundled C parser with `cc`).

Verdict: no malicious code found; safe to build and test.
