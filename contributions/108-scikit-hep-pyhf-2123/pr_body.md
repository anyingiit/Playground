# Description

Resolves #2123 by moving the tbump configuration from `tbump.toml` into the `[tool.tbump]` table of `pyproject.toml` and removing `tbump.toml`. tbump reads `[tool.tbump]` from `pyproject.toml` on its own, so `uvx tbump` in the release-prepare workflow needs no change.

The configuration was copied over as is: `github_url`, `[tool.tbump.version]` (the `current` version and the regex), `[tool.tbump.git]`, the `[[tool.tbump.file]]` entries and the `candidate` `[[tool.tbump.field]]`. The self-referencing `src = "tbump.toml"` entry now points at `pyproject.toml`. It keeps the `search = "Bump version: {current_version} → "` restriction, so in `pyproject.toml` only the `message_template` line gets bumped (plus `tool.tbump.version.current`, which tbump always bumps). Other strings that happen to contain the version are left alone.

Since the release process from #2743 reads the version straight from `tbump.toml`, I also updated every place that does:

* `ci/validate-version.py` now reads `["tool"]["tbump"]["version"]` from `pyproject.toml`. The error message now says "tbump release version format".
* `.github/workflows/release-tag.yml`: the "Read version from pyproject.toml" step reads the same key with `tomllib`. The header comment is updated to match.
* `.github/workflows/release-prepare.yml`: the text of the generated PR body.
* `docs/development.rst` (release procedure and patch release notes) and the patch-release forward-port item in `.github/ISSUE_TEMPLATE/~release-checklist.md`.

After this PR, `git grep tbump.toml` returns nothing.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2123

# Checklist Before Requesting Reviewer

- [x] Tests are passing (config-only change; verified with tbump 6.11.0 and Python 3.12)
  - `tbump current-version` gives `0.7.6` both before and after the change.
  - `tbump --only-patch --non-interactive 0.7.7`, run on `main` and on this branch: both bump the same 7 files with an identical 19+/19− diff. The only difference is that the two self-bumped lines (`current` and `message_template`) are now in `pyproject.toml` instead of `tbump.toml`. Nothing else in `pyproject.toml` changes, and `0.8.0rc1` works the same way.
  - `uv run ci/validate-version.py 0.7.7` gives `Bumping version: 0.7.6 -> 0.7.7`. `0.8.0rc1` is accepted. `v0.7.7`, `0.7.6` and `0.7.07` are rejected with the expected errors.
  - On this branch, the old `validate-version.py` and the old release-tag one-liner both fail with `FileNotFoundError: 'tbump.toml'`. The updated script works as shown above, and the updated one-liner prints `0.7.6`. On `main`, tbump with no `tbump.toml` fails with `Key "tbump" does not exist`.
  - `prek run --files <changed files>`: every hook passes. zizmor's online audit couldn't reach the GitHub API from my environment, so I ran it with `zizmor --offline` on both workflows. It reports no findings, the same as on `main`.
- [x] "WIP" removed from the title of the pull request
- [ ] Selected an Assignee for the PR to be responsible for the log summary
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (pyhf writes release notes per release under `docs/release-notes`)
- [x] Documentation is updated (if applicable) — `docs/development.rst` and the release checklist issue template

# Before Merging

For the PR Assignees:

- [ ] Summarize commit messages into a comprehensive review of the PR
