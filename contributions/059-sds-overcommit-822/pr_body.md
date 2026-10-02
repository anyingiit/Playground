## Description

`CommitMsg::TextWidth` warns on every body line longer than `max_body_width`, including lines that contain nothing but a URL. A URL can't be wrapped without breaking it (in the terminal and on GitHub), so these warnings can't be fixed without making the message worse.

This PR exempts body lines that consist solely of a URL (`scheme://...`, surrounding whitespace ignored), optionally written as a Markdown-style link reference such as `[1]: https://...`. Lines that mix a URL with other text are still checked as before, and the subject line checks are unchanged. No new configuration option is added; the exemption is always on, since an over-long URL-only line is never actionable.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #822

## Checklist

- [x] Tests pass locally (`bundle exec rspec spec/overcommit/hook/commit_msg/text_width_spec.rb`: 19 examples, 0 failures; the 2 new URL-only specs fail without the fix. Full `bundle exec rspec`: 1647 examples, 5 failures, all in `author_email_spec`/`author_name_spec`/`committing_spec`, which fail identically on `main` in my environment due to its git config. `bundle exec overcommit --run`: all pre-commit hooks passed)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, entries appear to be added when a version is cut; happy to add one if you prefer
- [ ] Documentation is updated (if applicable) — n/a, the behavior is described in the hook's source comment
