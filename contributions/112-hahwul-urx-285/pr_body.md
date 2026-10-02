## Description

Adds unit tests for `fmt_count` in `src/runner/mod.rs`, the private helper that adds thousands separators to the URL counts in the progress summary.

The issue suggested creating a new `#[cfg(test)]` module, but `src/runner/mod.rs` now already has one (`mod tests { use super::*; ... }`), so I put the two new tests there instead of adding a second module:

- `test_fmt_count_inserts_thousands_separators`: `0`, `7`, `999`, `1000`, `12345`, `999_999`, `1_000_000`, `1_234_567` (the three values from the issue, plus values on each side of the grouping boundaries).
- `test_fmt_count_handles_usize_max`: `usize::MAX` → `"18,446,744,073,709,551,615"`, gated on `#[cfg(target_pointer_width = "64")]` so 32-bit builds don't fail.

This is a test-only change with no effect on runtime behavior. To check that the tests catch real regressions, I temporarily broke `fmt_count` in two ways and confirmed they failed each time: grouping by 4 instead of 3 (`"1000"` instead of `"1,000"`) and dropping the `i > 0 &&` guard (`",999"` instead of `"999"`).

Side note, not changed here: `src/cache/command.rs` has a similar thousands-separator helper. I left it alone to keep this PR focused on the issue.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #285

## Checklist

- [x] Tests pass locally
  - `cargo test --bin urx fmt_count` — 2 passed
  - `cargo test` — all pass (1228 passed, 2 ignored in the binary's unit tests; the other test targets also pass)
  - `cargo clippy -- --deny warnings` and `cargo clippy --tests -- --deny warnings` — clean
  - `cargo fmt --check` — clean
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (test-only change)
- [ ] Documentation is updated (if applicable) — n/a
