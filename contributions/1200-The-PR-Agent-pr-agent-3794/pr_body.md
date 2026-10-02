## Description

Since #3746 raised the GitHub sub-issue query from 10 to 100, `extract_tickets` makes one `get_issue` REST call for every direct sub-issue of every linked ticket, with no cap. A PR linked to three large parent issues can trigger about 300 serial REST calls and a much larger ticket context. This PR makes two small changes in `pr_agent/tools/ticket_pr_compliance_check.py`, both proposed in #3794:

1. **Cap sub-issue lookups per ticket.** A new `MAX_GITHUB_SUB_ISSUES = 10` constant (10 was the old limit), next to `MAX_GITHUB_TICKETS` and `MAX_GITHUB_TICKET_LOOKUPS`, bounds the sub-issue loop with `itertools.islice`. When a ticket has more sub-issues, an info line is logged. The GraphQL query in `GithubProvider.fetch_sub_issues` is unchanged: it still asks for up to 100 children (#3746). It is a single request, so only the per-child REST lookups are capped.
2. **Store each ticket before its sub-issues.** `extract_and_cache_pr_tickets` used to append a ticket's sub-issues first and the ticket itself last. `fit_related_tickets_to_prompt_budget` keeps a *prefix* of `related_tickets` when the prompt is too large, so a linked ticket placed after its children was the first thing dropped. Now each ticket comes first and its sub-issues follow, so trimming drops sub-issues first.

Note for reviewers: `fetch_sub_issues` returns a `set`, so when a ticket has more than 10 children, which 10 are kept follows that set's iteration order. This matches the old `first: 10` behaviour, where the selection also depended on what GitHub returned. If you would prefer GitHub's order, `fetch_sub_issues` could return an ordered collection, but I left its return type alone to keep this change small.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #3794

## Checklist

- [x] Tests pass locally:
  - `PYTHONPATH=. uv run pytest tests/unittest/test_ticket_extraction_async.py -q` → 51 passed. Without the fix, the new `test_sub_issue_lookups_are_capped_per_ticket` (counts `get_issue` calls: 1 + 10 instead of 1 + 15) and the updated `test_stores_main_issue_before_its_sub_issues_in_related_tickets` both fail.
  - `PYTHONPATH=. uv run pytest tests/unittest -q` → 10289 passed, 33 skipped, 1 xfailed
  - `uv run ruff check <changed files>` → All checks passed; `pre-commit run --files <changed files>` → Passed
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, release notes are generated from merged PRs
- [ ] Documentation is updated (if applicable) — n/a, no user-facing option or docs page changes
