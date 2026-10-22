Thanks for the review notes. I pushed two follow-up commits (no rebase, per AGENTS.md):

1. Tests first: the interrupt-during-spawn test now records the old `UnboundLocalError`, so without the fix it fails on its assertion instead of erroring. A second test sends SIGINT after pexpect has created the child but before `spawn()` returns, and checks the child isn't left running. It fails on that commit.
2. The fix: `system()` holds back SIGINT while pexpect spawns, and raises `KeyboardInterrupt` again right after `spawn()` returns, so the existing handler forwards ^C to the child and terminates it. Outside the main thread it doesn't touch the handler, since Python only raises ^C in the main thread anyway. The handler also copes with `child.before` still being `None` at that point.

`tests/test_process.py` passes locally (22 passed, 5 skipped), and ruff is clean.
