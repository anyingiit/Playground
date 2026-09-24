# Malicious-code audit — etiennebacher/jarl (shallow clone of `main` @ 6ccdf00, 2026-09-23)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/jarl` (377 text files) + manual review
of everything that executes during `cargo build` / `cargo test`, including git dependencies fetched by
`cargo fetch --locked`.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `crates/jarl-core/build.rs` | Read in full: lists `docs/rules/*.md`, writes a `match` of `include_str!` into `$OUT_DIR/rule_docs.rs` | Benign — no network, no process spawning, writes only to OUT_DIR |
| `.github/workflows/release.yml:70,130` pipe-to-shell (`cargo-dist` installer, `rustup`) | Release CI only, official installers over HTTPS | Benign — not run by build/test |
| "powershell-download" in `rule_set.rs`, `download_file.rs`, `analyze/call.rs` | These are the `download_file` *lint rule* (it flags R's `download.file()`) | False positive |
| `Command::new("git")` in `vcs.rs`; `Command::new("R"/"Rscript")` in `package_cache.rs`, `library_paths.rs` | Queries git status / R library paths — expected linter functionality | Benign (R is not installed here; code paths degrade gracefully) |
| `Command::new(binary_path())` in integration-test helpers | Runs the freshly built `jarl` binary | Benign |
| Git deps `etiennebacher/air_pratt`, `etiennebacher/ark` (forks of Posit's air/ark), `lionel-/biome` (pinned rev) | Pinned in `Cargo.lock`. Build scripts actually compiled: `air_pratt/crates/crates/build.rs` (runs `cargo metadata --no-deps`, writes crate-name list to OUT_DIR) and `biome_diagnostics_categories/build.rs` (quote!-based codegen into OUT_DIR). `ark`/`harp` build.rs are not in the dependency graph (`cargo tree`) | Benign |
| `justfile` | `document` runs R scripts in `docs/`; `lint` runs clippy/fmt | Benign; only `cargo` commands used here |
| npm lifecycle hooks / committed binaries | none | — |

**Verdict: no malicious code found. Safe to build and test.**
