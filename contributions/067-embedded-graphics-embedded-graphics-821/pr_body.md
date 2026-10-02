- [x] Check that you've added passing tests and documentation
- [x] Add a `CHANGELOG.md` entry in the **Unreleased** section under the appropriate heading (**Added**, **Fixed**, etc) if your changes affect the **public API**
- [x] Run `rustfmt` on the project
- [ ] Run `just build` (Linux/macOS only) and make sure it passes. If you use Windows, check that CI passes once you've opened the PR. — ran `just test` and `just check-formatting` equivalents plus CI's clippy command locally; drawing-example/readme/link checks were not run (no docs/examples changed)

## PR description

## Description

`ImageRaw::draw_sub_image` checked whether the requested area lies inside the image with `area.top_left.x as u32 + area.size.width > self.size.width` (same for `y`/`height`). For very large areas (e.g. `Size::new(u32::MAX, 1)` at `x = 1`) this addition overflows: debug builds panic with "attempt to add with overflow", and in release builds the sum wraps around to a small value, so the check passes and `row_skip = data_width - area.size.width` underflows, producing a `ContiguousPixels` iterator with bogus parameters.

The fix uses `checked_add` and treats an overflow as "area is outside the image", so nothing is drawn — the same behavior as for any other out-of-bounds area. Once the check holds, `top_left + size <= image size <= data width`, so the later `initial_skip`/`row_skip` calculations can no longer underflow. `map_or(true, ..)` is used instead of `is_none_or` to stay compatible with the 1.81 MSRV.

A regression test (`draw_sub_image_with_overflowing_area`) covers overflowing widths and heights, including `x`/`y = i32::MAX`. It panics without the fix and passes with it. A `CHANGELOG.md` entry was added under **Unreleased → Fixed** (it links the issue; happy to change it to the PR number).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #821

## Checklist

- [x] Tests pass locally (`cargo test --workspace`: all pass; new test fails before the fix with an overflow panic at `src/image/image_raw.rs:227` and passes after; `cargo fmt --all -- --check` clean; `cargo clippy --all-targets -- --deny=warnings` clean)
- [x] `CHANGELOG.md` is updated (if applicable) — entry under Unreleased → Fixed
- [ ] Documentation is updated (if applicable) — n/a, no API change
