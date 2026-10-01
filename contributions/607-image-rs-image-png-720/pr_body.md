## Description

`parse_cicp` reported invalid field values (non-zero matrix coefficients, a video full-range flag other than 0/1) and trailing bytes as `DecodingError::IoError(InvalidData)`. Only `DecodingError::Format` errors in ancillary chunks are downgraded to `Decoded::BadAncillaryChunk`, so these bubbled up and made `read_info()` fail for an otherwise valid image, contrary to #525.

This PR reports them as format errors instead: two new `FormatErrorInner` variants (`InvalidCicpFullRangeFlag(u8)`, `InvalidCicpMatrixCoefficients(u8)`, following the existing `InvalidSrgbRenderingIntent(u8)` pattern) and `ChunkLengthWrong { kind: cICP }` for trailing bytes. The chunk is now skipped and `info.coding_independent_code_points` stays `None`.

A regression test builds a small PNG with each bad cICP payload and checks that `read_info()` and `next_frame()` succeed. It fails without the fix (`read_info failed for cICP payload [9, 16, 1, 1]: invalid data`). I also added a `CHANGES.md` entry under Unreleased / Fixes.

Side note, not changed here: `parse_mdcv`, `parse_clli` and one branch of `parse_bkgd` still use `IoError(InvalidData)` the same way, so trailing bytes in those chunks would also be fatal. I can do the same for them here or in a follow-up if you'd like.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #720

## Checklist

- [x] Tests pass locally (`cargo test --workspace --all-targets`: lib 102 passed / 1 ignored, all other targets pass; `cargo test --doc`: 8 passed; `cargo check --tests --no-default-features`: OK; `cargo fmt -- --check`: clean)
- [x] `CHANGES.md` is updated (if applicable): Unreleased → Fixes entry referencing #720
- [ ] Documentation is updated (if applicable): n/a (`FormatErrorInner` is internal)
