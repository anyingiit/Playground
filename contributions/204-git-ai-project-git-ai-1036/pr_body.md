## Description

`git-ai install-hooks` / uninstall rewrote `~/.codex/config.toml` with `toml::to_string_pretty`, so every user comment was lost and keys were re-sorted. This adds a small `update_toml_preserving_format` helper in `src/mdm/utils.rs` that applies the desired config (still computed with the existing `toml::Value` logic) onto a `toml_edit` document parsed from the original file: unchanged entries stay byte-for-byte, changed values are updated in place, removed keys are dropped and new tables are appended. The three Codex write sites now use it; `toml_edit` was already in the lockfile as a transitive dependency.

**Disclosure:** prepared with Claude Code and verified as listed below. Feel free to close it if it doesn't fit.

## Related issue

Closes #1036

## Checklist

- [x] New tests `test_install_hooks_preserves_comments_and_formatting` / `test_install_hooks_keeps_comments_inside_updated_tables` fail on `main` and pass with the fix; 3 unit tests for the helper
- [x] `cargo test --lib` → 2547 passed, 1 ignored; `cargo test --test integration codex` → 64 passed
- [x] `cargo fmt -- --check`, `cargo clippy --all-targets -- -D warnings`, `cargo doc --no-deps` clean
