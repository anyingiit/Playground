<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KPKpHzfAxy5KoBhHBfd3QVb)_

## Description

When source is piped in with `--stdin-filename` (as editor integrations such as ALE do), Reek ignored `exclude_paths`, even with `--force-exclusion`. `Application#source_from_pipe` built the source directly and never went through the exclusion check that `SourceLocator` applies to files given on the command line.

Following the approach suggested in the issue, this extracts that check into a public `SourceLocator#excluded_file?(path)` (formerly the private `ignore_file?`, logic unchanged) and uses it in `source_from_pipe`: if the stdin filename is excluded, no sources are reported. The semantics match those for a file passed on the command line:

- a file listed directly in `exclude_paths` is skipped;
- a file inside an excluded directory is skipped only with `--force-exclusion`.

As with command-line files, `exclude_paths` entries are globbed against the filesystem, so the exclusion applies when the stdin filename refers to an existing file (the editor-integration case).

Tests:

- `features/command_line_interface/stdin.feature`: two new scenarios (file excluded directly; file in an excluded directory, with and without `--force-exclusion`). Both fail on `master` and pass with the change.
- `spec/reek/source/source_locator_spec.rb`: specs for `#excluded_file?`, including a path that does not exist on disk.

No CHANGELOG entry since the changelog appears to be written at release time with PR numbers; happy to add one if you prefer.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #1429

## Checklist

- [x] Tests pass locally — `bundle exec rake ci` (Ruby 3.3.6): spec 1120 examples / 0 failures, features 127 scenarios passed, rubocop no offenses, quality 134 examples / 0 failures
- [ ] `CHANGELOG.md` is updated — left for release time (see above)
- [ ] Documentation is updated — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)
