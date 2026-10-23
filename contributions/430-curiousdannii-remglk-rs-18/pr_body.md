Fixes #18

The Glk spec says that `glk_set_echo_line_event()` "does not affect a pending line input request". Right now `handle_line_input` reads the window's *current* `echo_line_input`. So if a game turns echo off while a line request is pending, the input is not echoed when it arrives or when the request is cancelled. This is the case discussed in i7/extensions#187: the Glk Input Suspending extension turns echo off and then cancels the pending request.

### Change

- `BufferWindow` gets a `line_input_echo` field.
- `request_line_event` copies `echo_line_input` into it when a line request is made on a buffer window.
- `handle_line_input` uses that field instead of the live setting.
- Grid windows are unchanged: they always echo.

### Test

I added `tests/echolinetest.ulx` and its regtest, and added it to `tests/runtests.sh`.
- The Inform 6 source is included as `tests/echolinetest.inf`. It has no library dependencies and calls the Glk functions directly through `@glk`.
- Build it with `inform6 -G echolinetest.inf`. I used Inform 6.44.
- The test reads two lines:
  - The first request is made with echo on, and echo is turned off while it is pending. The input must still be echoed.
  - The second request is made with echo off, and echo is turned on while it is pending. The input must not be echoed.

Results:
- Without the fix, both checks fail (`<LiteralCheck "xyzzy">: not found` and `<LiteralCheck !"plugh">: inverse test should fail`).
- With the fix, `./tests/runtests.sh` passes completely, using glulxe master and regtest.py from plotex.
- `cargo clippy` shows no warnings.

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
