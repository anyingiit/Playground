## Description

Fixes the stack overflow in `Pdf::new` on deeply nested arrays/dictionaries reported in #1347.

**Root cause:** skipping nested arrays and dictionaries in `hayro-syntax` was recursive (`Array::skip` / `Dict::skip` → `Object::skip` → …) with no depth limit, so a ~20 KB file with a few thousand nested `[` could overflow the stack and abort the process (not catchable via `catch_unwind`). There was a second unbounded path through the *read* side: when `parse_dict_with` encounters garbage in key position (e.g. `<< << << …`), it called `Object::read`, which reads a `Dict`, which calls `parse_dict_with` again, and so on.

**Approach:**
- `Array::skip`, `Dict::skip` and `Object::skip` now delegate to crate-private `skip_array` / `skip_dict` / `skip_object` helpers that carry a `depth` and return `None` once `MAX_NESTING_DEPTH` (256) is reached. The public `Skippable` trait and the observable behaviour for normal files are unchanged (same leniency, same offset restore on failure). 256 is well above the spec's Annex C implementation limit of 28, and low enough to stay far away from the stack limit even in debug builds.
- The garbage-key path in `parse_dict_with` now *skips* the object instead of reading it (the result was discarded anyway), so it goes through the depth-limited code as well.

Objects that exceed the limit simply fail to parse, like any other malformed object.

Tests (in `hayro-syntax`):
- `pdf::tests::deeply_nested_arrays`, `deeply_nested_dicts`, `deeply_nested_garbage_dicts`: a small PDF with 10 000 levels of nesting. All three abort with `has overflowed its stack` (SIGABRT) on `main` and pass with this change. (I also checked that the garbage-dict test still overflows if only the skip side is fixed.)
- `pdf::tests::moderately_nested_arrays`: 100 levels still parse fine and resolve via the catalog.
- `object::array::tests::nesting_depth_limit`: pins the boundary (256 levels ok, 257 rejected).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1347

## Checklist

- [x] Tests pass locally (`cargo test -p hayro-syntax --lib nested` → 4 passed, red on `main` (stack overflow) → green; `cargo test -p hayro-syntax` → 204 passed (incl. `nesting_depth_limit`), the only 2 failures are `pdf_version_*`, which need the downloaded corpus (`hayro-tests/downloads`) and fail identically without this change; CI's `cargo test -p hayro-tests -- "load::"` → 112 passed; `cargo fmt --check --all` clean; `cargo clippy -p hayro-syntax --tests --examples` no new warnings; `cargo doc -p hayro-syntax --no-deps` with `-D warnings` clean; `cargo check -p hayro-syntax --no-default-features [--features std|images|unsafe]` with `-D warnings` clean)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (no changelog in the repo)
- [ ] Documentation is updated (if applicable) — n/a (internal change)
