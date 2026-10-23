- [x] Closes #2502
- [x] Executed `pre-commit run --all-files` or `pixi run lint --all-files` with no errors — ran `taplo fmt --check pyproject.toml` (the only hook relevant to the touched files); passes
- [x] The change is fully covered by automated unit tests — the existing tests using the `subtests` fixture exercise it
- [ ] Documented in docs/ as appropriate — n/a
- [x] Added an entry to the CHANGES file

## Description

pytest 9.0 integrated `pytest-subtests` into pytest itself and the plugin repository has been archived. This drops `pytest-subtests` from the `test` extra and pins `pytest>=9` instead, so the built-in `subtests` fixture is always available (without the pin, a resolver could pick pytest 8 and every test that takes `subtests` would error with `fixture 'subtests' not found`).

Verification (Python 3.13, fresh venv, `uv pip install -e ".[test]"` → pytest 9.1.1, no pytest-subtests installed):

- `pytest --benchmark-skip` → `1926 passed, 1171 skipped, 8 xfailed, 288 subtests passed`
- Same venv downgraded to pytest 8 (still without the plugin): tests using `subtests` fail with `fixture 'subtests' not found`, which is why the `>=9` lower bound is needed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

🤖 Generated with [Claude Code](https://claude.com/claude-code)
