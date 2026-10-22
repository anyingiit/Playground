<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KMcyNnzD6JeAFXoMMWEfs3D)_

Closes #3104

`AutosubmitConfig.get_project_submodules_depth` documents a default of -1 (no limit). For an invalid value, it logs "Using default value -1" but then returns `[]`. While looking at that, I found that the function only handles **string** values, and the experiment YAML is not stringified on load:

| `GIT.PROJECT_SUBMODULES_DEPTH` | Before | After |
|---|---|---|
| not set / `"-1"` / `"3"` / `"[1, 2]"` | `[-1]` / `[-1]` / `[3]` / `[1, 2]` | unchanged |
| `3` (YAML int) | `TypeError: argument of type 'int' is not iterable` (not caught; it is raised before the `try`) | `[3]` |
| `[1, 2]` (YAML list) | `[]`: `int([1, 2])` raises `TypeError`, which is caught, so the setting is ignored (with the misleading "Using default value -1" warning) | `[1, 2]` |
| `"abc"`, `""` | `ValueError` (not caught: only `TypeError` is) | warning + `[-1]` |

I checked that `AutosubmitConfig.get_parser(...)` + `normalize_variables` keep `PROJECT_SUBMODULES_DEPTH: 3` as an `int`. So a user who writes the depth without quotes gets the `TypeError` when `autosubmit create`/`refresh` clones the project.

For invalid values the function now returns `[-1]`, as the docstring and the warning say. For the caller in `autosubmit/git/autosubmit_git.py` this behaves the same as `[]`: both lead to `max_depth = -1`, so submodules are cloned with `--recursive` as before.

Tests: `test_get_project_submodules_depth` (string, int and list forms) and `test_get_project_submodules_depth_invalid_uses_default` (warning + `-1`). Before the fix, 8 of the 13 new cases fail. With it, all 13 pass. `pytest test/unit/config test/unit/git` gives 282 passed, 2 skipped. `ruff check` on the changed files passes.

**Check List**

- [x] I have read `CONTRIBUTING.md`.
- [x] Contains logically grouped changes (else tidy your branch by rebase).
- [x] Does not contain off-topic changes (use other PRs for other changes).
- [ ] Applied any dependency changes to `pyproject.toml`. (n/a, no dependency changes)
- [x] Tests are included (or explain why tests are not needed).
- [x] Changelog entry included in `CHANGELOG.md` if this is a change that can affect users.
- [ ] Documentation updated. (n/a)
- [x] If this is a bug fix, PR should include a link to the issue (e.g. `Closes #1234`).

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
