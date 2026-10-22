Fixes #877

## Problem

`:ConformInfo` gets the LSP formatters with only the buffer number:

```lua
local lsp_clients = lsp_format.get_format_clients({ bufnr = vim.api.nvim_get_current_buf() })
```

`format()` merges the filetype options from `formatters_by_ft` first, so `name`, `id` and `filter` are applied when formatting but not in the info window. With the config from the issue (a `filter` that drops `lua_ls`), ConformInfo still shows `LSP: lua_ls` even though `lua_ls` is never used to format.

## Change

- `conform.list_lsp_format_clients(bufnr)` (marked `---@private`) resolves the clients with the filetype options from `get_opts_from_filetype()`, the same source `format()` and `list_formatters_to_run()` use for `name`, `id` and `filter`.
- `health.lua` uses it for the "LSP:" line, and the `lsp_format` require there is no longer needed.

Options passed directly to `conform.format()` (e.g. a `filter` in a keymap) can't be known by ConformInfo, so they are still not reflected. This only covers the options from `formatters_by_ft`.

## Tests

New `tests/health_spec.lua`. It stubs `vim.lsp.get_clients` with two clients, sets a `filter` for `lua` in `formatters_by_ft`, opens ConformInfo and checks the window shows `LSP: other_ls`. It fails without the change (the line is `LSP: lua_ls, other_ls`) and passes with it.

With Neovim 0.12.6, `./run_tests.sh` passes except for three tests: `fuzzer formats correctly`, `injected formatter inline.ts` and `runner e2e sets the correct output`. They fail the same way on `master` in my environment, where nvim-treesitter could not download the parsers. `luacheck lua tests` is clean, and `stylua --check` is clean on the changed files.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
