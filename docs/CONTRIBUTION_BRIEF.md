# Contribution brief (applies to every contribution in this repo)

Goal: use spare quota to help open-source maintainers by fixing `good first issue` /
`help wanted` issues. PRs cannot be opened from this environment (no fork/push rights
outside `anyingiit/playground`), so every contribution is saved here as a ready-to-apply
patch + a ready-to-paste PR description. The owner (anyingiit) submits them later.

## Hard requirements (all mandatory)

1. **Understand the issue completely.** Read the full issue body and every comment
   (use WebFetch on the issue URL, or `mcp__github__search_issues` with owner/repo and
   `fields: ["number","title","body"]` to get the verbatim body).
2. **Judge whether the request is legitimate/reasonable** using the repo's ROADMAP,
   docs, CONTRIBUTING, AGENTS/CLAUDE.md, recent commits/PRs and other clues. If it is not
   reasonable, already fixed, or out of scope, stop and record why.
3. **No duplicates.** Before implementing, search open PRs for the issue
   (`mcp__github__search_pull_requests` with query `<issue-number> repo:owner/name`, and a
   keyword query). Also check the issue is not assigned/claimed in comments. If someone is
   already on it, skip (or at most offer a missing test as a comment draft).
4. **Tests/CI must pass.** Run the repo's own test/lint/format/typecheck commands as CI
   and CONTRIBUTING describe. Add a regression test for bug fixes and prove it fails
   without the fix (red → green). If a full suite cannot run here, run the largest
   relevant subset and say exactly what was and wasn't run, and show that any remaining
   failures also fail on the base branch.
5. **Follow the repo's conventions**: commit message format (Conventional Commits,
   DCO, principle citations, etc.), changelog/changeset fragments, docs updates, code
   style, PR template requirements. Commit with
   `git -c user.name=anyingiit -c user.email=winshyon@gmail.com commit ...`.
   Do NOT add `Signed-off-by` yourself (DCO must be the owner's own sign-off) — note in
   the README if the repo needs it. Never put AI model names in commits.
6. **Malicious-code audit before running anything** from a new repo:
   `python3 /home/user/Playground/tools/audit_repo.py <clone-dir>` and manually review
   every hit, with extra care for code that runs on install/build/test (setup.py,
   conftest.py, build.rs, package.json lifecycle hooks, test setup files, Makefiles,
   CMake downloads, CI scripts invoked by tests). Save the reviewed verdict as
   `AUDIT.md` in the contribution folder (summary table: hit → reviewed → benign/why).
   If anything looks malicious, STOP, do not run it, and report.
7. **PR text in the chefs-pick-oss-starter format** (see below), including the
   motivation/disclosure paragraph.

## Checkpointing (quota may run out at any moment)

Work so that an interruption leaves something usable, not nothing:
1. As soon as the issue is chosen, create the deliverables folder with a `README.md` stub:
   issue link, tier, `Status: 🚧 in progress — <current step>`, and the notes gathered so far.
2. Update the `Status:` line and notes after each milestone (audit done → implemented →
   tests red/green → full checks → PR text written).
3. As soon as a working commit exists, export `0001-*.patch` immediately; re-export after changes.
4. Write `AUDIT.md` right after the audit, before building/testing.
The coordinator commits the folder periodically, so partial progress survives.

## Deliverables — folder `contributions/NN-<owner>-<repo>-<issue>/`

- `0001-*.patch` — from `git format-patch -1` (single commit on a branch off the default branch).
- `README.md` (Chinese is fine for the notes, PR text in English):
  - table: Issue link · Tier (高活跃高Star / 新锐 / 自由) · labels · status · duplicate-PR check result
  - 问题理解 / 合理性判断 / 改动 / 验证 (exact commands + results, red→green) / 如何提交 (git am steps, base branch)
  - PR title + PR body in the format below
- `AUDIT.md` — malicious-code audit verdict.

Do NOT `git commit`/`push` in `/home/user/Playground` — the coordinator does that.

## PR body format (chefs-pick-oss-starter `.github/PULL_REQUEST_TEMPLATE.md`)

```markdown
## Description

<What changes and why. Root cause, approach, anything reviewers should know.>

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #<n>

## Checklist

- [x] Tests pass locally (<exact commands + results>)
- [ ] `CHANGELOG.md` is updated (if applicable) — <how / n/a>
- [ ] Documentation is updated (if applicable) — <how / n/a>
```

If the target repo's own template demands extra items (e.g. a changeset checkbox or a
"Constitution principle" line), add them inside the Description or Checklist.

## Environment notes

- Work in `/home/user/work/<repo>`; shallow clones (`git clone --depth 1`), sparse checkout for huge repos.
- Disk is limited (~15 GB free shared by everyone). Check `df -h /home/user` before big
  installs/builds; delete `node_modules`, `target/`, venvs, caches (`~/.cache/pip`) when done.
- The machine has 4 cores shared by several agents; prefer targeted builds/tests.
- Global GitHub search via curl is blocked; use the `mcp__github__*` tools (load via ToolSearch)
  and WebFetch. The GitHub search API has secondary rate limits — back off ~60 s on 403.
