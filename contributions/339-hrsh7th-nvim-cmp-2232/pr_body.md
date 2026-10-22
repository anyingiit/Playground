Fixes #2232

## Problem

`custom_entries_view.open` only moves the menu left when the cursor is in the right half of the editor:

```lua
if math.floor(vim.o.columns * 0.5) <= col + border_offset_col and vim.o.columns - col - border_offset_col <= width then
```

When the cursor is in the left half and the menu is still too wide (a long item, or a narrow terminal as in the issue), the column is left as requested. Neovim then clamps the float on screen by itself, but `entries_win.style` (and therefore `view:info()`) still holds the requested `col`/`width`. `docs_view.open` computes `left_space`/`right_space` from that `info()`, so it places the documentation window on what it thinks is free space, which is actually covered by the menu.

## Change

Drop the "right half" part of the condition: whenever the menu does not fit to the right of its column, apply the existing clamp (shift left, and shrink if it is wider than the editor). Menus that end before the last column are not touched (the same one-column margin the right-half case already used), and the right-half case behaves as before.

With that, `info()` describes the geometry Neovim actually draws, and the docs view either finds the real free side or closes when there is no room (the "expected behavior" in the issue). This keeps the fix in the menu instead of reading back `nvim_win_get_position`, as suggested in the issue, and it can be tested headlessly.

## Tests

New `lua/cmp/view/custom_entries_view_spec.lua`:

- a menu wider than the editor, opened at column 0, must stay within `vim.o.columns`
- a menu opened at column 20 that overflows the right edge must stay within `vim.o.columns`
- a menu that fits is not moved

The first two fail without the change and pass with it. `vusted ./lua` passes (76 successes) with Neovim 0.11.4, `luacheck lua` reports 0 warnings, and `stylua --check` is clean on the changed files.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
