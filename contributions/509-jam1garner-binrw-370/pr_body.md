## Description

With `#[br(stream = ident)]` on a data enum, the generated prelude moves the original reader into `ident` (`let ident = reader;`). Each variant, however, is generated as a standalone struct that has no stream identifier of its own, so the variant body still referred to the original (now moved) reader. Any variant that touched the reader therefore failed with E0382 "borrow of moved value" — `count` was the reported trigger because its error path calls `stream_position` inside a closure, but plain field reads in a variant hit the same problem.

The fix makes each variant inherit the enum's stream identifier (unless the variant specifies its own), so variant code uses the same reader variable as the enum prelude. Unit-only enums and structs already used `stream_ident_or(READER)` correctly and are unaffected. The `binwrite` side was checked with an equivalent enum and already works.

A regression test `enum_named_stream_with_count` is added to `binrw/tests/derive/enum.rs` (mirroring the existing `move_named_stream_with_count` struct test). It fails to compile without the fix (E0382) and passes with it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #370

## Checklist

- [x] Tests pass locally (Rust 1.97.0 stable: `cargo fmt -- --check` OK; `cargo clippy --all-targets -- -D warnings` and `cargo clippy --all-targets --all-features -- -D warnings` clean; `cargo test` all suites pass, incl. the new test; new test fails to compile on `master` with E0382)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [ ] Documentation is updated (if applicable) — n/a, bug fix with no API change
