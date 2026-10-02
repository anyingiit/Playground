## Description

`backend/compilers/download.py` did not treat failed downloads as failures:

- When `get_compiler_raw` raised (e.g. `('Connection aborted.', RemoteDisconnected(...))`), `DownloadThread.run` logged the exception but put nothing on the results queue. The failed compiler therefore vanished from both the numerator and the denominator, so the run still logged `Updated 213 / 213 compiler(s)`.
- `main()` always returned normally, so the script exited 0 and CI/deploy steps that run it (`uv run compilers/download.py ... && ...`) carried on.

Changes:

- Results are now `(item, result)` pairs. An exception is recorded as `False` for that compiler.
- The two `return None` paths after a failed image index / manifest request (the image exists in the registry but fetching it failed) now log an error and return `False`, matching the existing `False` for a failed extraction. `None` still means "nothing to do" (already up to date).
- The summary only counts real downloads (`result is True`). If anything failed, the script logs `N compiler(s) failed to download: platform/compiler, ...` and exits with status 1 (`sys.exit(main())`).

I left the "`<image>` not found in registry!" case unchanged (it still returns `None` and does not fail the run). That lookup also returns `None` for any non-200 answer, so it can hide transient errors as well. I wasn't sure whether failing the run for a missing image is what you want (it could break setups that list compilers that aren't published yet), so I kept this PR small. I'm happy to change that here if you'd like.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2118

## Checklist

- [x] Tests pass locally
  - New `coreapp/tests/test_compiler_download.py` (mocks `get_compiler_raw`, no network): a run with one download, one exception and one failed result now returns 1 and logs `Updated 1 / 3`; a clean run returns 0. Both tests fail without the change (`main()` returned `None`).
  - `uv run python manage.py test coreapp.tests.test_compiler_download`: OK (2 tests)
  - `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`: clean
  - Full `uv run python manage.py test` run outside Docker without downloaded compilers/binutils: 20 failures in `test_platform` / `test_compiler_endpoint`. The same 20 fail on `main` in the same environment, and the new tests pass.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (no changelog in the repo)
- [ ] Documentation is updated (if applicable) — n/a
