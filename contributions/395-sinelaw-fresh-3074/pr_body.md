Fixes #3074.

A terminal whose shell had exited before the editor quit came back as `*Terminal N* (exited)` instead of `bash — <cwd> (exited)`. Only explicit titles were saved (`title`), and an auto-named tab re-derives its name from the live process after restore. A restored dead terminal has no process, so it fell back to the generic name, and two dead shells in different directories looked the same.

What changed:

- When an auto-named terminal exits, the name it derived is kept on its `ExitedTerminal` record as `auto_title`. The `*Terminal N*` fallback isn't kept, since restore generates its own.
- The workspace saves it in `ExitedTerminalState.auto_title`, an optional serde field, so older workspace files still load. Restoring a dead terminal puts the name back on the tab before the `(exited)` marker.
- The tab stays auto-named. The restart path is unchanged: restarting drops the record and `sync_terminal_titles` names the tab from the new process. Explicit titles still go through `title`, as before.

Test: `test_exited_auto_named_terminal_keeps_its_name_across_an_editor_restart` in `tests/e2e/restart_exited_terminal.rs` (Linux-only, like the other auto-naming tests). It turns on `terminal_auto_title`, opens a shell, waits for the tab to show the shell's name, runs `exit`, saves the session, and reopens it. It then checks on the rendered tab bar that the dead tab shows the shell's name and not `*Terminal`, and that restarting it from the status-bar indicator names the tab from the new shell again. Without the change it fails with `Tab bar:  *Terminal 0* (exited)`. It passed five runs in a row. I only exercised the local, single-window path.

Checked: `cargo fmt`; `cargo check --all-targets -p fresh-editor`; plain `cargo clippy -p fresh-editor --all-targets` (no new warnings in the touched code); the `restart_exited_terminal` e2e tests, all e2e tests matching `terminal` (203 passed), and the `workspace`/`exited_terminal` unit tests. No Settings or plugin API change, so there's nothing to regenerate.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

- [x] I agree my contributions are licensed under GPL-3.0-or-later and may be relicensed in the future at the maintainer's discretion (see [CONTRIBUTING.md](../CONTRIBUTING.md#license)).
