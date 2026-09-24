# mloda-ai/mloda-registry#742 — Exclude .claude/worktrees from the bandit scan

| Item | Value |
|---|---|
| Issue | https://github.com/mloda-ai/mloda-registry/issues/742 |
| Tier | 新锐 |
| Labels | bug, good first issue, help wanted |
| Status | 🚧 in progress — implemented + committed, patch exported; running full tox |
| Duplicate-PR check | `742 repo:mloda-ai/mloda-registry` → 0 PRs; `bandit worktrees` → 0 PRs; issue has 0 comments, no assignee (2026-09-24) |

## 问题理解
bandit 不读 .gitignore；当 `.claude/worktrees/<wt>` 下有 git worktree 时，本地 `tox` 的 bandit 步骤会扫描 worktree 里的 `scripts/verify_builds.py` 副本并报 B404/B603/B607。
需在 tox.ini `-x` 列表与 pyproject `[tool.bandit] exclude_dirs` 加 `.claude/worktrees/*` 与 `*/.claude/worktrees/*`。PR 标题用 `chore:`。
