## Description

Pressing Ctrl+C during `EvoSci deploy` / `EvoSci serve` startup (before the ready banner) left `langgraph dev` running in the background with its PID file and workspace sidecar on disk.

**Root cause:** `start_langgraph_dev()` spawns the server with `start_new_session=True` (POSIX) / `CREATE_NEW_PROCESS_GROUP` (Windows), so the terminal's SIGINT only reaches the CLI. The callers' atexit / signal cleanup is registered only after `start_langgraph_dev()` returns, and the health-wait loop had no cleanup for `KeyboardInterrupt`, so the half-started server was orphaned.

**Fix (as suggested in the issue):** everything after `Popen` — the PID-file / sidecar writes, module-state assignment and the `/ok` health wait — now runs inside `try: ... except BaseException: stop_langgraph_dev(proc); raise`. The existing "exited immediately" and "not healthy within 60 seconds" paths now just raise and go through the same cleanup instead of calling `stop_langgraph_dev(proc)` inline, so their behaviour and error messages are unchanged. The happy path (`return proc`) is untouched.

**Tests:** added `TestStartLanggraphDevInterruptedStartup` in `tests/test_langgraph_manager.py`:
- `test_keyboard_interrupt_during_health_wait_stops_server` — raises `KeyboardInterrupt` from the health probe inside the wait loop and asserts the spawned process is terminated, the PID file and sidecar are removed, and `_PROCESS` / `_PROCESS_WORKSPACE` are cleared. Fails on `main` (process never terminated), passes with this change.
- `test_early_exit_still_stops_and_raises_runtime_error` — guards the existing early-exit path (still `RuntimeError`, still cleaned up).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #534

## Type of change

- [x] Bug fix

## Checklist

- [x] I have read the [Contributing Guidelines](../CONTRIBUTING.md)
- [x] This targets **core functionality** used by the majority of users
- [x] I have added/updated tests where applicable
- [x] `uv run ruff check .` passes (`All checks passed!`; `ruff format --check .` → 459 files already formatted)
- [x] `uv run pytest` passes (`uv run pytest --timeout=30` → 4223 passed, 27 skipped; synced with `uv sync --dev`, without the `all-channels` extra)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, internal behaviour fix
