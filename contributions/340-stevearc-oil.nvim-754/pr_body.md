Fixes #754

## Problem

When `enforce_action_order` finds a move cycle, it first checks whether the move is a parent being moved into itself:

```lua
if vim.startswith(loop_action.dest_url, loop_action.src_url) then
  error("Detected cycle in desired paths")
end
```

That is a plain string prefix check, so for the swap in the issue (`foo` -> `foo2` and `foo2` -> `foo`) the move `foo` -> `foo2` is treated as "moving `foo` into itself" and the whole save fails. Whether it happens depends on which of the two moves ends up as `loop_action`, which matches the reporter's note that it is not always reproducible.

## Change

Compare against `src_url .. "/"`, the same way the check for selected actions a few lines below already does (`Cannot move or copy parent into itself`). A real move of a directory into its own child (`/a` -> `/a/b`) is still rejected, and the existing "Detects move directory loops" test still passes.

## Tests

Added `Resolves MOVE loops between names that share a prefix` to `tests/mutator_spec.lua`. It runs `enforce_action_order` on the two moves in both orders and expects the loop to be split into three moves: one file moved to a temporary name, the other moved into place, then the temporary moved to its destination. Without the change it fails with `Detected cycle in desired paths`, and with it `./run_tests.sh` passes. `luacheck lua tests` is clean and `stylua --check` is clean on the changed files.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
