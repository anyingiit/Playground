# Audit — jasonjmcghee/ron-lsp @ b5e8023 ("Release 0.1.4", shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/ron-lsp` + manual review of the auto-exec surface (build scripts, install hooks).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Pattern findings | none reported | — |
| `tree-sitter-ron/build.rs`, `tree-sitter-ron/bindings/rust/build.rs` | Only compile the generated `parser.c` with the `cc` crate | benign |
| `tree-sitter-ron/setup.py`, `tree-sitter-ron/package.json` (node-gyp-build) | Python/Node bindings; not used by cargo, not executed here | not run |
| `jetbrains-plugin/gradle/wrapper/gradle-wrapper.jar` | Standard Gradle wrapper; JetBrains plugin not built here | not run |

Verdict: nothing malicious; safe to run `cargo build` / `cargo test` / `cargo fmt` / `cargo clippy` on the Rust crate.
