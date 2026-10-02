## Description

`&LinearMap` implements `IntoIterator`, but `&mut LinearMap` does not, so `for (k, v) in &mut map { ... }` fails to compile even though `LinearMap::iter_mut()` already exists.

This adds `impl IntoIterator for &'a mut LinearMapInner<K, V, S>` (mirroring the existing `&'a LinearMapInner` impl), returning the existing `IterMut<'a, K, V>`. Because it is implemented on `LinearMapInner<K, V, S>` with `S: LinearMapStorage + ?Sized`, it covers both `&mut LinearMap<K, V, N>` and `&mut LinearMapView<K, V>`. A unit test (`linear_map::test::into_iter_mut`) exercises both; it fails to compile without the impl. A CHANGELOG entry is added under Unreleased.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #492

## Checklist

- [x] Tests pass locally (`cargo test --lib` → 250 passed; `cargo test --doc --features alloc` → 197 passed; new test fails to compile without the fix and passes with it; `cargo clippy --all-targets --features "alloc,defmt,portable-atomic-critical-section,serde,ufmt,bytes,zeroize,embedded-io-v0.7"` (host target) → no warnings; `cargo fmt --all -- --check` (stable rustfmt) → clean)
- [x] `CHANGELOG.md` is updated (if applicable) — added an entry under `[Unreleased]`
- [ ] Documentation is updated (if applicable) — n/a (trait impl, shows up in rustdoc automatically)
