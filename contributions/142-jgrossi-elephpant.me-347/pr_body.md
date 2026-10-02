## Description

Adds the account creation date to a user's herd (profile) page, as proposed in #347.

The existing calendar line from #328/#339 now reads:

> Joined March 2021 • Herd updated 2 days ago

- `x-user-profile` gets a new `showJoined` prop (default `false`). When set and the user has a `created_at`, it renders `Joined {Month} {Year}` (`F Y`).
- The joined date and the herd update date are joined with ` • ` on the same line, under the existing calendar icon. Either part is omitted if it's not available (e.g. a user with no elePHPants only shows "Joined …").
- As the issue suggests, the label "Herd last updated" was shortened to "Herd updated" for consistency (I kept sentence case; happy to switch to "Herd Updated" if you prefer the exact wording from the issue).
- Only `herd/show.blade.php` opts in, so the compact trade list and the conversation header are unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #347

## Checklist

- [x] Tests pass locally — `./vendor/bin/pest -p`: 215 passed (504 assertions). New tests in `tests/Feature/ExampleTest.php` fail without the view change (3 failed) and pass with it.
- [x] `./vendor/bin/pint --test` passed, `./vendor/bin/phpstan analyse` no errors, `./vendor/bin/rector process --dry-run` clean
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (no changelog in the repo)
- [ ] Documentation is updated (if applicable) — n/a
