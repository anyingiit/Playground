# Worker brief (parallel contribution sessions, 2026-10-01 round)

You are one of 8 parallel worker sessions in a volunteer open-source contribution effort run from the repo anyingiit/Playground (checked out here). Read docs/CONTRIBUTION_BRIEF.md and contributions/SUBMISSIONS.md fully first, and look at a finished example such as contributions/45-fsspec-projspec-69/.

YOUR SLICE: given in the session prompt (worker id, tier, ecosystems, target, folder-number range).
Tier definitions: 高星 = >5k stars and very active; 新锐 = young (<2 years) fast-growing project; 自由 = anything else that is actively maintained with a real test suite.

Use multi-agent Workflows (ultracode is on) to scout → precheck → implement → adversarially review, as many in parallel as your machine allows (4 cores; keep heavy builds limited).

Rules (owner decisions, override the brief where they differ):
- Follow every hard requirement in the brief: full issue understanding, legitimacy, AI-policy check (skip repos that ban AI contributions or require human-written PR descriptions/docs or videos), no duplicates (no open/merged PR, not claimed/assigned), malicious-code audit + AUDIT.md BEFORE running anything, red→green regression test, repo's own lint/format/typecheck/tests, repo conventions.
- Deliverables per folder: 0001-*.patch, README.md (Chinese notes; include 需要提交者注意 and submit steps), AUDIT.md, pr_title.txt, pr_body.md (English, chefs-pick-oss-starter format with the motivation/disclosure paragraph).
- Patch commit author: `git -c user.name=anyingiit -c user.email=49945850+anyingiit@users.noreply.github.com commit`. No AI model names in commits. DCO Signed-off-by with that same identity is allowed if the repo requires it; if the repo requires an AI trailer use `Assisted-by: Claude Code`.
- Do NOT use repos that already have a folder under contributions/ (check `ls contributions contributions/_skipped` and also `git fetch origin` + `git ls-tree -r --name-only origin/claude/serene-hamilton-br3vum contributions` periodically, since other workers add folders) and do not take repos clearly outside your ecosystem slice — other workers own those.
- Environment facts: GitHub API (gh api / mcp__github__*) does NOT work for upstream repos (proxy 403) and you must NOT open PRs, fork, comment or otherwise write to GitHub upstream. Read GitHub via WebFetch/WebSearch of github.com pages (issues?q=..., pulls?q=<issue-number>, labels page, raw.githubusercontent.com) and anonymous `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1`. Work in /home/user/work/<repo>; clean venvs/node_modules/target/caches after each task.
- Checkpoint: commit your new folders to your current branch and `git push -u origin <your branch>` at least every 30 minutes and after each finished contribution (commit author anyingiit <49945850+anyingiit@users.noreply.github.com>). Only push to your own designated branch. Do not edit other workers' folders, INDEX.md, SUBMISSIONS.md or submissions.json.
- Time box: stop starting new contributions at 2026-10-02 00:15 UTC; have everything finished, committed and pushed by 00:55 UTC. Unfinished work must be pushed with a clear Status line in its README.
- When done, write contributions/_workers/<worker-id>.md: a table of every folder you produced (NN, issue link, tier, status ready/skipped, one-line reason), commit and push it.
