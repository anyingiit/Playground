Closes #3240

`Log.set_file` created the log directory with `os.mkdir`. That has two failure modes:

- If a **parent** of the log directory is also missing, `os.mkdir` raises `FileNotFoundError`. Every retry fails the same way, so after sleeping between attempts (5 s + 10 s by default) it raises `AutosubmitCritical`.
- For a **bare file name** (`Log.set_file("foo.log")`) the directory part is `''`, so `os.mkdir('')` always fails, with the same result.

About the FIXME in the issue: `logging.FileHandler(path, 'w')` creates the file itself, so the log file does not need to exist before the handler is attached. When only the last directory level is missing, the current code already works. The new `missing_dir` test cases cover that case, and they pass both before and after this change. The mkdir/handler logic itself is fine; only the way the directory was created was broken.

Changes:

- `os.makedirs(directory, exist_ok=True)`, with `os.curdir` when the path has no directory part. The FIXME is replaced with a comment explaining the above.
- New tests in `test/unit/log/test_log.py`:
  - `test_set_file_creates_missing_directories` covers the 4 handler types, for a missing directory and for missing parent directories. It checks that a handler is added, that there is no retry, and that the log file is created, with no log file existing beforehand.
  - `test_set_file_bare_file_name`.
- A CHANGELOG entry under 4.2.0 bug fixes.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

**Check List**

- [x] I have read `CONTRIBUTING.md`.
- [x] Contains logically grouped changes (else tidy your branch by rebase).
- [x] Does not contain off-topic changes (use other PRs for other changes).
- [x] Applied any dependency changes to `pyproject.toml`. (none)
- [x] Tests are included. Without the fix, 5 of the 9 new test cases fail (the missing-parent and bare-name cases); with it, `pytest test/unit/log` gives 82 passed. The full `pytest test/unit -n 4` run gives 2563 passed and 4 failed; the same 4 tests fail on `master` in my environment (no PostgreSQL driver, running as root, no `autosubmit` entry point on PATH). `ruff check` on the changed files is clean.
- [x] Changelog entry included in `CHANGELOG.md` if this is a change that can affect users.
- [ ] Documentation updated. (n/a)
- [x] If this is a bug fix, PR should include a link to the issue (e.g. `Closes #1234`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
