## Description

In a Cargo workspace where the RON files live outside any crate (e.g. `assets/defs/user.ron` next to `crates/proj_core/src/user.rs`), an annotation such as `/* @[proj_core::user::User] */` failed with `Could not find type: proj_core::user::User`.

**Root cause:** `file_path_to_module_path` keys every scanned type as `crate::<mods>::Type`, so the analyzer never knew which crate a type belonged to. A type could only be named as `crate::...` or by its bare name, and same-named modules in different workspace members overwrote each other in the type cache.

**Fix (backward compatible):**
- While `scan_workspace` walks the `.rs` files, it finds each file's crate. That is the nearest `Cargo.toml` above the file that has a `[package] name`, with `-` replaced by `_`. `[workspace]`-only manifests are skipped. Results are cached per directory.
- Types and type aliases are also registered under `<crate_name>::<mods>::Type`. They go into separate maps (`crate_types`, `crate_type_aliases`), so:
  - `get_all_types` (completion, the "Found N types" count) does not return duplicates;
  - `proj_core::user::User` and `other::user::User` resolve to their own types even though both are `crate::user::User`;
  - alias targets written as `crate::...` are rewritten to the alias's own crate.
- `get_type_info` (both before and after the lazy rescan) and the alias lookup in `has_custom_deserializer` also consult these maps. Existing `crate::...` and bare-name annotations behave exactly as before.

Not changed: a `crate::...` annotation in a file outside any crate is still ambiguous when several members share that path. The crate-qualified form is the way to disambiguate. It might be worth mentioning the `<crate_name>::path` form in the README, next to the `@[crate::models::User]` examples. It also works for `type = "..."` in `ron.toml` `[[types]]`. I left the docs alone in case you'd prefer to word that yourself.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #15

## Checklist

- [x] Tests pass locally:
  - `cargo test`: 72 + 1 passed, including the new `rust_analyzer::tests::resolves_crate_qualified_paths_in_workspace`. That test builds a temp workspace with two members that both define `user::User`. It fails on `main` with "proj_core::user::User should resolve".
  - `cargo fmt --check`: clean.
  - `cargo clippy`: no warnings.
  - Manual check: `ron-lsp check assets/defs/user.ron` with `/* @[proj_core::user::User] */` in a workspace fixture now reports "All files valid!", and a misspelled field is reported as a missing required field.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — not done; see the README suggestion above
