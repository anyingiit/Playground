## Description

`HashTrieMap::new_with_degree(1)` (and every other constructor that funnels into
`new_with_hasher_and_degree_and_ptr_kind`, including the `HashTrieSet` ones) was accepted because 1 is a
power of two. With degree 1, `index_from_hash` uses `trailing_zeros() == 0` bits per level and a mask of 0,
so every key maps to index 0 at every depth and the shift never reaches the end of the hash. Two distinct
keys therefore can never be separated, and `insert` recurses until the stack overflows.

This adds `assert!(degree >= 2, "degree must be at least 2")` next to the existing power-of-two and
upper-bound assertions, so the bad degree is rejected at construction time as the issue suggests, and adds a
`#[should_panic]` regression test.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #113

## Checklist

- [x] Tests pass locally: new test `test_new_with_degree_one_panics` fails without the fix ("test did not panic as expected") and passes with it; `cargo test --all-targets --all-features` (277 passed), `cargo test --all-targets --no-default-features` (259 passed), `cargo test --doc --all-features` (29 passed), `cargo fmt -- --check`, `cargo clippy --all-targets -- -D warnings`, `cargo doc --no-deps --all-features` all clean with `RUSTFLAGS=-Dwarnings`
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, happy to add a `release-notes.md` entry if you'd like one
- [ ] Documentation is updated (if applicable) — n/a
