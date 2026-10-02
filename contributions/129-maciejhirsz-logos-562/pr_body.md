## Description

As noted in #562, the rustdoc page of the `Logos` derive macro only lists the helper attributes, so all explanations of how to use them live in the external handbook and are missing from `cargo doc --offline`.

This PR adds a reference section to the re-exported derive macro (the doc comment sits on `pub use logos_derive::Logos;` in `src/lib.rs`, so rustdoc merges it into the derive page and the examples run as doctests of the `logos` crate). It covers:

- a getting-started example and how the `Lexer` iterator / `span` / `slice` work;
- `#[token]` and `#[regex]` syntax (`literal`, callback, `priority`, `ignore(case)`);
- token disambiguation and how priorities are computed;
- callbacks and the table of supported return types;
- every `#[logos(...)]` option: `skip` (incl. callback form), `extras`, `error` (incl. `error(Type, callback)`), `utf8 = false`, `lifetime`, `subpattern`, `type`, `crate`, `export_dir`.

All examples are compiled and run as doctests (9 new). The crate-level docs now link to the derive macro docs in addition to the handbook. The handbook itself is left unchanged; I kept the rustdoc version as a compact reference rather than copying every chapter (longer tutorials such as context-dependent lexing, the examples, debugging and contributing remain in the book). Happy to adjust the scope — e.g. move more chapters in, or `include_str!` shared snippets — if you prefer a different split.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #562

## Checklist

- [x] Tests pass locally (`cargo test --doc -p logos`: 18 passed, 9 of them new; also with `--features state_machine_codegen` and `--features forbid_unsafe`; `cargo test --workspace`: all passed; `cargo fmt --check` and `cargo clippy --features debug -- -D warnings` clean; `RUSTDOCFLAGS="-D warnings" cargo doc -p logos --no-deps --features debug` builds without warnings)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no changelog file)
- [x] Documentation is updated (if applicable) — rustdoc of the `Logos` derive macro and crate-level docs
