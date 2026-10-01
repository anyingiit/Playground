## Summary

Wrapped lines (and nested content) of list, enum and term items were indented by the configured `tab_spaces` (`--tab-width`), so with `--tab-width=4` a wrapped list item got a four-space hanging indent. This PR makes item bodies always use a two-space hanging indent (the width of `- `), while `tab_spaces` keeps applying to code.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #478

## Changes

- `convert_list_item_like` / `convert_term_item` (`crates/typstyle-core/src/pretty/markup.rs`) now nest the item body by a fixed 2 instead of `self.indent(...)` (which used `tab_spaces`).
- New fixture `tests/fixtures/unit/markup/list-indent-tab4.typ` (`/// typstyle: tab_spaces=4 wrap_text`) covering wrapped list/enum/term items, nested lists, and a list inside a code block (code still indents by 4).
- `CHANGELOG.md`: added an `Unreleased` entry.

Note: with the default `tab_spaces = 2` output is unchanged (no existing snapshot changed). One consequence worth flagging: with a non-default tab width, nested list items are now also indented by 2 rather than by `tab_spaces`. If you'd prefer nested items to keep following `tab_spaces` and only change the wrapped-line indent, I'm happy to adjust.

## Checklist

- [x] **Updated CHANGELOG.md**: added an `Unreleased` entry with an example
- [ ] **Updated documentation**: n/a (no documented behaviour for item indentation)
- [x] **Added tests**: new snapshot fixture `list-indent-tab4.typ` (fails on `master` with a 4-space hanging indent, passes with this change)

## Testing

- `cargo test -p typstyle-tests --test tests -- --skip e2e` → 2675 passed, 0 failed (e2e repo tests not run locally)
- `cargo test -p typstyle-core` → 25 passed
- `cargo test -p typstyle --test test_style_args` → 6 passed
- `cargo clippy -p typstyle-core -p typstyle-tests --all-targets --all-features` → no warnings
- `cargo fmt --check --all` → clean
