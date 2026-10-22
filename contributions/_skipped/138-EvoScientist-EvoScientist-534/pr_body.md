## Description

Pressing Ctrl+C while `langgraph dev` is still starting (e.g. during `EvoSci deploy`) left the server running in the background.

**Root cause:** `start_langgraph_dev()` spawns the server with `start_new_session=True` (POSIX) / `CREATE_NEW_PROCESS_GROUP` (Windows), so the terminal's SIGINT only reaches the CLI. The callers register their cleanup (atexit / `finally`) only *after* `start_langgraph_dev()` returns. A `KeyboardInterrupt` raised anywhere between `Popen` and the ready `return proc` (writing the PID file / sidecar, or the up-to-60s health poll) therefore orphaned the server together with its PID file and workspace sidecar, and the next deploy hit a port conflict.

**Fix:** as suggested in the issue, everything after the spawn is wrapped in `try: ... except BaseException: stop_langgraph_dev(proc); raise`. `BaseException` is intentional so `KeyboardInterrupt` is covered. The two existing failure paths ("exited immediately" and "did not become healthy within 60 seconds") used to call `stop_langgraph_dev(proc)` themselves; they now just raise and the shared handler does the cleanup, so behaviour on those paths is unchanged. Most of the diff is the re-indentation of the existing block; the logic inside is unchanged.

**Tests:** new `TestStartLanggraphDevCleansUpOnInterrupt` in `tests/test_langgraph_manager.py` (reuses the existing `start_langgraph_dev_capture` fixture, with a fake `Popen` handle and a spy on `stop_langgraph_dev`):
- `KeyboardInterrupt` during the health poll → the server is stopped and the interrupt propagates (fails before the fix)
- an exception while writing the workspace sidecar → the server is stopped (fails before the fix)
- a successful start → `stop_langgraph_dev` is not called

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #534

## Type of change

- [x] Bug fix
- [ ] New feature
- [ ] Documentation / examples
- [ ] Test improvement
- [ ] Refactor (no behavior change)

## Checklist

- [x] I have read the [Contributing Guidelines](../CONTRIBUTING.md)
- [x] This targets **core functionality** used by the majority of users (`EvoSci deploy` / `EvoSci serve` startup)
- [x] I have added/updated tests where applicable (2 of the 3 new tests fail without the fix and pass with it)
- [x] `uv run ruff check .` passes (`uv run ruff format --check .` also passes)
- [x] `uv run pytest` passes (`uv run pytest --timeout=30`: 4224 passed, 27 skipped)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, internal behaviour only
