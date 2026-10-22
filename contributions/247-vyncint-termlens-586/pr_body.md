## What & why

Fixes both defects in #586:

- **Decorated blank runs are drawn.** `to_svg` trimmed each run's trailing blanks and skipped a run left empty, decoration and all, so an underlined empty form field (`printf 'Name: \033[4m   \033[0m|'`) vanished from the SVG while `to_html` drew it. A run with underline or strikethrough now keeps its blanks, so the line is drawn under them as a terminal draws it. That includes the trailing blanks of a decorated run that has text: an underlined "ab   " is now underlined across all five cells, as in `to_html`, where before the line stopped after "ab". Undecorated runs are trimmed as before. Concealed text still draws nothing in the SVG; `to_html` draws the underline of a concealed underlined run, and I left that existing difference alone.
- **No characters XML forbids.** `escape_xml` now writes every character outside the XML 1.0 `Char` production (C0 controls other than tab, LF and CR, plus U+FFFE and U+FFFF) as U+FFFD, one for one so a cell stays one column. A window title holding `\x01` or a cell holding U+FFFF no longer makes an SVG no parser opens. `to_html` shares the function, so it gets the same treatment.

Tests in `crates/termlens/tests/export.rs`: a decorated-blanks screen, U+FFFF in a cell (both built with `Screen::parse`, no PTY), and `\x01` in an OSC 0 title through the `emit` fixture (ignored on Windows with the usual #149 reason, like the other fixture-driven export tests). Each checks the output with a small `assert_well_formed_xml` helper: every character is an XML `Char` and the tags nest. That is not a full parse (entities and attribute syntax aren't checked); I also parsed the test SVGs with `xmllint` by hand and they are well-formed. I kept it dependency-free rather than adding an XML parser as a dev-dependency. If you'd prefer a real parse (as asked in #376), I'm happy to switch it to `roxmltree` or `quick-xml`.

Closes #586

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below; per CONTRIBUTING §6 the commit carries no AI attribution and I'm the author of record under the DCO. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all.

## Checklist

- [x] Linked an issue (#586)
- [x] Tests added/updated for the change: three new tests; all three fail with only `render.rs` reverted and pass with it
- [x] `cargo fmt --all` and `cargo clippy --workspace --all-targets --all-features` are clean; `cargo test --workspace --all-features` passes
- [x] **All commits are signed off** (`check-dco.sh main..HEAD`: OK)
- [x] **No AI attribution trailers** (`check-no-ai-attribution.sh main..HEAD`: OK)
- [x] `CHANGELOG.md` updated under `[Unreleased]` → `Fixed`
- [x] Snapshot changes (if any) were reviewed with `cargo insta review`, not blind-accepted (none in this PR: no existing snapshot had a decorated blank run or a forbidden character)
