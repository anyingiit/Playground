## Description

The README's Usage section says "For detailed examples, see [EXAMPLES.md](EXAMPLES.md)", but there is no `EXAMPLES.md` in the repo, so the link 404s (#11).

The examples for each kind of test (action, request, feature, part, database cleaning, operations) are already right below in the same Usage section, so this removes the dangling sentence rather than adding a new file. I changed `README.repo.md` (the source that repo-sync renders from) and `README.md` the same way so they stay in sync.

If you'd rather keep the link and have a separate `EXAMPLES.md`, I'm happy to rework this, e.g. by moving the "Writing Tests" examples there.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and checked as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #11

## Checklist

- [x] Docs-only change; `grep -rn EXAMPLES .` finds no other references
- [ ] Tests — n/a (documentation)
- [ ] `CHANGELOG.md` — n/a (documentation only)
