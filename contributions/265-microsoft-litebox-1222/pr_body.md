## Description

`SafeZoneAllocator`'s `LockedHeapWithRescue` callback called `unimplemented!()` whenever a request was larger than the buddy allocator's maximum block size (`1 << (ORDER - 1)`). This violates the `GlobalAlloc::alloc` contract (out-of-memory must be signalled by returning null) and turns fallible APIs such as `Vec::try_reserve` into a panic/abort — e.g. with `HEAP_ORDER = 25` any 32 MiB request panics regardless of available memory.

The rescue callback now simply returns without growing the heap for such requests. `LockedHeapWithRescue::alloc` then retries, fails again, and returns null. The `MemoryProvider` is not asked for memory in this case, since adding memory could never satisfy a block of that order. Behaviour for all requests within the maximum order is unchanged. The struct docs now mention that larger requests fail with null.

Tests (covering both acceptance-criteria cases):
- unit tests in `mm::allocator`: over-max-order requests return null and do not call the memory provider; allocations up to the largest supported block (slab, 4 KiB, 2 MiB, `1 << (ORDER - 1)`) still succeed and grow the heap; an exhausted memory provider yields null for all sizes;
- integration test `litebox/tests/safe_zone_allocator.rs` installs `SafeZoneAllocator` as `#[global_allocator]` and checks that `Vec::try_reserve_exact` beyond the maximum order returns `Err`, and that the largest supported block still works afterwards.

Without the fix, `over_max_order_allocation_returns_null` panics at the `unimplemented!()`, and the integration test hangs (the panic happens while the buddy allocator's spin lock is held, and the panic machinery then tries to allocate). With the fix all of them pass.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1222

## Checklist

- [x] Tests pass locally (`cargo test --locked -p litebox -- --skip nine_p`: 110 unit + 1 integration + 3 doc tests pass; the 24 `fs::nine_p` tests need the `diod` server, which isn't installed in my environment, and fail identically without this change. `cargo fmt --check` clean; `cargo clippy --locked --all-targets --all-features -p litebox`: no warnings; `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features --document-private-items -p litebox`: clean)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [x] Documentation is updated (if applicable) — doc comment on `SafeZoneAllocator` notes that over-max-order requests return null
