## Description

When an enum gets its id from `id = "..."` (typically from `ctx`), the id is not read from the input, so an `id_pat` variant has no id storage field. `DekuRead` already handles this — `pad_id` is only set when `id` is `None` — but `DekuWrite` treated the first field of *every* `id_pat` variant as id storage. That field was then written with the enum's `endian`/`bits`/`bytes` and without its own attributes, so:

- a first field with `#[deku(ctx = "...")]` failed to compile (`expected u8, found ()`), as reported in #655;
- a first field with its own `endian` (or `bits`, …) silently wrote the wrong bytes.

The fix makes the write side match the read side: the first field is only treated as id storage when `id_pat` is set **and** the enum has no `id`. Note that the change suggested in the issue (passing `f.ctx` to the id-storage path) fixes the compile error but not the second case — with it, the added test still fails with `left: [128, 0, 18, 52]`, `right: [128, 0, 52, 18]`.

Added `test_enum_id_pat_ctx_id_first_field_attributes` in `tests/test_attributes/test_ctx.rs`, covering the issue's example and a big-endian first field. It fails to compile without the fix and passes with it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #655

## Checklist

- [x] Tests pass locally (`cargo test --all`, `cargo test --all-features`, `cargo test --no-default-features --features=bits,alloc` all ok; `cargo clippy --all-targets -- -D warnings` and `cargo fmt --all -- --check` clean)
- [x] `CHANGELOG.md` is updated (if applicable) — entry under `[Unreleased]` / `Fixed`
- [ ] Documentation is updated (if applicable) — n/a
