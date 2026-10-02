# Malicious-code audit — maciejhirsz/logos @ fba6c4d (master, 2026-09-11)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/logos` (120 text files scanned): pattern findings none, committed binaries none, npm hooks none. Then manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` | only pre-commit-hooks (check-yaml/toml, whitespace) and pretty-format yaml/toml; not run locally | benign |
| `build.rs` | none anywhere in the repo | — |
| proc macro (`logos-derive` → `logos-codegen`, runs at compile time) | grep for `std::fs`/`std::net`/`env::var`/`Command`: only `generate_graphs()` in `logos-codegen/src/lib.rs`, which writes .dot/.mmd files when the user opts in via `#[logos(export_dir = ...)]`; no network, no env reads, no process spawning | benign |
| `logos-cli/src/main.rs` `Command::new("rustfmt")` | CLI pipes generated code through local rustfmt; not built/run by the doc tests | benign |
| `logos-codegen/tests/*.rs` fs reads/writes | read test fixtures, write/remove a local `*_export_tmp` dir | benign |
| `.github/workflows/*.yml` | standard cargo test/clippy/fmt/doc/mdbook/msrv jobs | benign |

Verdict: **no malicious code found**; safe to build and run `cargo test` / `cargo doc` locally (CARGO_TARGET_DIR inside /home/user/work/logos).
