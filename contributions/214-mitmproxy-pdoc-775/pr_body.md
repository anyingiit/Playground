## Description

With `--docformat google`, the section regex in `docstrings.google()` also ran over fenced code blocks, so a line like `ABC:` followed by indented lines inside a ```` ``` ```` block was turned into a `###### ABC:` heading plus a block quote.

`google()` now applies the section conversion only to the text outside fenced code blocks. The fences are found with a simple line-by-line scan (no backtracking regex, so it stays linear on large docstrings). Only fences that start at the beginning of a line (```` ``` ```` or `~~~`) are skipped, and, as in CommonMark, a block is closed by a fence of the same character that is at least as long as the opening one (so a ```` ````md ```` block may contain ```` ``` ````). A fenced block that is indented as part of a section's contents (e.g. a code example under `Examples:`) stays part of that section, as before. An unterminated fence is treated as regular text, i.e. behaves as before.

I kept this to the Google flavour reported in the issue; the NumPy flavour splits on `Heading\n----` and could in principle be affected in a similar way, but I didn't want to widen the change without a report.

Tests: `test_google_fenced_code_block` in `test/test_docstrings.py` with the example from the issue (fails on `main`), a fence between two regular sections, a longer outer fence, and an unterminated fence. All snapshot tests are unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #775

## Checklist

- [x] Tests pass locally — `uv run pytest --cov=pdoc -m "not slow"`: 155 passed, `pdoc/docstrings.py` 100% covered; full `uv run pytest test/`: 360 passed; `ruff check .`, `ruff format --check .`, `mypy pdoc test` clean
- [x] `CHANGELOG.md` is updated
- [ ] Documentation is updated — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)
