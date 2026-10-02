## Description

`#` is a valid character in Git ref names, but the revset lexer only accepted `[a-zA-Z0-9_$@/-]` (plus single `.`) in unquoted names, so an expression like `git hide -D 'stack(mr/1229#crc)'` failed with `parse error: Invalid token at 13`.

This adds `#` to the character class of the `Name` token in `git-branchless-revset/src/grammar.lalrpop`. `#` is not used by any revset operator, so it does not introduce ambiguity. A parser regression test (`test_revset_parse_hash_in_name`) covers a bare name, a name inside a function call, and names next to the `..` operator / after a `.`. Also added a CHANGELOG entry under Unreleased → Fixed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #498

## Checklist

- [x] Tests pass locally: `cargo test -p git-branchless-revset` (16 passed; the new test fails without the grammar change with `Invalid token at 7`), `cargo test -p git-branchless-query` (6 passed); manually checked `git branchless query 'stack(mr/1229#crc)'` returns the stack. `cargo fmt --all -- --check` and `cargo clippy -p git-branchless-revset --all-features --all-targets -- --deny warnings --allow renamed_and_removed_lints` are clean.
- [x] `CHANGELOG.md` is updated (if applicable) — entry under Unreleased → Fixed
- [ ] Documentation is updated (if applicable) — n/a
