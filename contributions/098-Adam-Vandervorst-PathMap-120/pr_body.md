## Description

Adds reverse counterparts to the existing iteration methods, as requested in #120:

- `ZipperMoving::to_prev_step` / `to_prev_step_observed` — visits every existing position in the exact reverse of the `to_next_step` order. If the focus has a previous sibling it moves there and descends the last child at each level down to a leaf; otherwise it ascends one byte. Called at the root it moves to the last position in the trie, and it returns `false` once it is back at the root, so calling it repeatedly cycles just like `to_next_step`.
- `ZipperIteration::to_prev_val` / `to_prev_val_observed` — visits values in the exact reverse of the `to_next_val` order (a value that has descendants comes right after its last descendant). It follows the same path as repeated `to_prev_step` calls, but uses `descend_last_path_observed` to reach the last leaf under a subtrie in one call, which made it ~1.8x faster than a plain `to_prev_step` loop on `binary_keys`.

Both are default implementations built on `to_prev_sibling_byte` / `descend_last_byte` / `ascend_byte`, so every zipper gets them. The zipper lens macro and `PathTracker` forward them to the wrapped zipper (the same as `to_next_*`), so a native implementation can be dropped in later. As discussed in the issue, `to_prev_k_path` / `descend_last_k_path` are not added.

Tests: `to_prev_step_test1` was added to `zipper_moving_tests!`, and `zipper_prev_iter_test1` / `zipper_prev_iter_test2` to `zipper_iteration_tests!`, so they run for every zipper type that uses those macros (read, owned read, write, prefix, product, overlay, poly, path_tracker, arena_compact, ...). They check that the reverse order is exactly the forward order reversed, that the `PathObserver` agrees with `path()`, that stepping back from the middle of the trie works, and that iteration works from a zipper rooted below the map root.

Benchmarks: `binary_zipper_prev_iter` / `binary_zipper_prev_step_iter`, `sparse_zipper_prev_cursor` / `sparse_zipper_prev_step_iter`, `superdense_zipper_prev_cursor` / `superdense_zipper_prev_step_iter`, next to the existing forward benches. Medians on my machine (shared, noisy) at the largest size:

| bench | forward | reverse |
|---|---|---|
| binary step (1600) | 2.68 ms | 2.66 ms |
| binary val (1600) | 70 µs | 1.65 ms |
| sparse step (1600) | 596 µs | 412 µs |
| sparse val (1600) | 50 µs | 344 µs |
| superdense step (3200) | 37 µs | 48 µs |
| superdense val (3200) | 24 µs | 51 µs |

Reverse stepping is about as fast as forward stepping. `to_prev_val` is slower than `to_next_val`, mostly on sparse/binary tries. The forward path uses the native `descend_first_byte`/`descend_until`, while the reverse path goes through the default `descend_last_byte` (`child_count` + `descend_indexed_byte`) and `to_prev_sibling_byte`. Native `to_prev_*` implementations (or a native `descend_last_byte`) for the read zipper could close that gap in a follow-up, and these benches are there to measure it.

The book's iteration chapter now mentions the new methods.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #120

## Checklist

- [x] Tests pass locally
  - New tests fail when `to_prev_step_observed` / `to_prev_val_observed` are stubbed to return `false` (28 failed), and pass with the change.
  - `cargo build --release --all-targets` (no new warnings)
  - `cargo test --release`: 1058 passed, 0 failed (lib) + integration and doc tests OK
  - `cargo test --release --features arena_compact,random`: 1220 passed, 0 failed (lib) + integration and doc tests OK
  - `cargo doc --no-deps`: OK (the one existing warning at `src/write_zipper.rs:201` is unchanged)
  - `cargo bench --bench {binary_keys,sparse_keys,superdense_keys} -- prev`
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no CHANGELOG)
- [x] Documentation is updated (if applicable) — rustdoc on the new methods + `pathmap-book/src/1.02.05_zipper_iter.md` / `api_links.md`
