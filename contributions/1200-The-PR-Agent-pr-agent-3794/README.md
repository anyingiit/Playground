# The-PR-Agent/pr-agent#3794 — Linked GitHub issues fetch every sub-issue with one REST call each, with no cap

| 项 | 值 |
|---|---|
| Issue | https://github.com/The-PR-Agent/pr-agent/issues/3794 |
| Tier | 高星 |
| Labels | good first issue, help wanted, Low Effort Issue, performance |
| Status | ✅ ready — patch + PR 文本已完成（未提交） |
| Base | `main` @ 2b73b36（2026-10-01，`fix(tools): re-raise any provider incomplete-files error ... (#3800)`） |
| Duplicate-PR check | 2026-10-01 23:00 和 23:09 UTC 各查一次：`pulls?q=3794` 0 结果；`pulls?q=is:pr sub-issue` 只有已合并的 #3746（就是引入回归的 PR），没有新 PR；issue 无 assignee，Development 为空，页面上没有可见评论（侦察时看到的 “1 comment” 实际是 issue 正文），不存在认领 |

## 问题理解

- #3746（2026-09-29 合并）把 `GithubProvider.fetch_sub_issues` 的 GraphQL `subIssues(first: 10)` 改成了 `first: 100`。
- `extract_tickets`（`ticket_pr_compliance_check.py` 约 930-936 行）会对每个子 issue 调一次 `repo.get_issue()`，而且没有上限。所以一个 PR 关联 3 个大 ticket 时，最多要串行发 ~300 次 REST 请求，prompt 里的 ticket 上下文也会大很多。
- `extract_and_cache_pr_tickets`（约 1092-1096 行）原来先 append 子 issue，最后才 append ticket 本身。`fit_related_tickets_to_prompt_budget` 超预算时保留的是 `related_tickets[:prefix]`（我核对了二分查找的代码），所以最后一个关联 ticket 排在它的子 issue 后面，会最先被截掉。
- Issue 给出的修法：每个 ticket 的子 issue 设上限（10，也就是旧值），并且把 ticket 放在它的子 issue 前面。

## 合理性判断

- Issue 指出的问题和具体代码行都能对上，修法也是 issue 自己给的，打了 `good first issue` / `Low Effort Issue`，没有争议。
- AI 政策：仓库有 `AGENTS.md`（给 coding agent 的仓库指南），`CONTRIBUTING.md` 没有禁止 AI。49 个 label 的描述里都没有 “human only” 之类的说法。结论：没有 AI 禁令。
- 设计取舍：**GraphQL 的 `first: 100` 保留不动**（#3746 刚合并，它只是一次请求，成本不高），只在 REST 循环里用 `itertools.islice` 限制次数。这样既符合 issue 说的 “cap fetched sub-issues per ticket”，也不会把 #3746 回退掉。

## 改动

- `pr_agent/tools/ticket_pr_compliance_check.py`
  - 新增常量 `MAX_GITHUB_SUB_ISSUES = 10`（放在 `MAX_GITHUB_TICKETS` / `MAX_GITHUB_TICKET_LOOKUPS` 旁边，带注释），`import itertools`。
  - 子 issue 循环改成 `for sub_issue_url in itertools.islice(sub_issues, MAX_GITHUB_SUB_ISSUES)`；超过上限时打一条 info 日志（写法参考同文件里的 `Too many GitHub tickets`）。上限按“尝试查询次数”计，查询失败的子 issue 也算一次，因为要限制的就是 REST 调用数。
  - `extract_and_cache_pr_tickets` 改成先 append ticket，再 append 它的子 issue。
- `tests/unittest/test_ticket_extraction_async.py`
  - 新增 `TestSubIssues::test_sub_issue_lookups_are_capped_per_ticket`：用 `MagicMock` 做 repo，15 个子 issue，断言只保留前 10 个，并且 `get_issue.call_count == 1 + 10`。
  - 原来的 `test_stores_sub_issues_before_main_issue_in_related_tickets` 断言的是旧顺序，改名为 `test_stores_main_issue_before_its_sub_issues_in_related_tickets`，期望值改成 `[main, sub_a, sub_b]`。

## 验证

环境：本机 uv 是 0.8.17，项目要求 `uv==0.12.10`，所以用 `uvx --from uv==0.12.10 uv sync --frozen`（与 CI 相同），venv 和 cache 都在工作目录里。

| 命令 | 结果 |
|---|---|
| 只回退 `pr_agent/`、保留新测试：`PYTHONPATH=. .venv/bin/python -m pytest tests/unittest/test_ticket_extraction_async.py -q` | **2 failed**, 49 passed → red（ordering 测试的断言失败；cap 测试因为常量不存在报 AttributeError） |
| 保留常量、只去掉 `islice`：`... -k capped` | **1 failed**（实际得到 15 个子 issue）→ red（证明是行为上的失败） |
| 打补丁后 `... tests/unittest/test_ticket_extraction_async.py -q` | 51 passed → green |
| 打补丁后跑全部单测 `PYTHONPATH=. .venv/bin/python -m pytest tests/unittest -q` | 10289 passed, 33 skipped, 1 xfailed（4 分 33 秒） |
| `.venv/bin/ruff check <2 changed files>` | All checks passed |
| `pre-commit run --files <2 changed files>`（SKIP=ruff-check,actionlint：ruff 已单独跑过；actionlint 只检查 workflow，这次没改） | 全部 Passed |
| 在新的 shallow clone 上 `git am 0001-*.patch` | 能干净应用 |

## 需要提交者注意

- Commit 用 Conventional Commits（`fix(tickets): ...`），作者是 anyingiit noreply 邮箱，没有 Signed-off-by（仓库不要求 DCO），也没有 AI trailer。
- 仓库没有 PR 模板。`CHANGELOG.md` 已经停止维护（release notes 从 PR 自动生成），所以不用改。
- PR 描述里已有 Claude Code 披露段落。
- 可能会被讨论的点：`fetch_sub_issues` 返回的是 `set`，子 issue 超过 10 个时保留哪 10 个取决于 set 的迭代顺序。PR 描述里已经说明，并提出可以改成有序容器，由维护者决定。
- 如果维护者更想直接把 GraphQL 改回 `first: 10`，也是一行的改动（`test_sub_issues_are_returned_when_present` 要跟着改）。

## 如何提交

```bash
git clone https://github.com/The-PR-Agent/pr-agent && cd pr-agent
git checkout -b fix/cap-github-sub-issues origin/main
git am /path/to/0001-fix-tickets-cap-GitHub-sub-issue-lookups-and-list-ti.patch
git push <your-fork> fix/cap-github-sub-issues   # PR 目标分支: main
# PR 标题见 pr_title.txt，正文见 pr_body.md
```

已验证的工作副本：`/home/user/work/pr-agent-3794`（分支 `fix/cap-github-sub-issues`）。

## 独立复核

复核时间：2026-10-01 23:30–23:40 UTC

- Issue 状态：WebFetch issue 页面，确认仍是 Open，没有 assignee，Development 为空，没有评论认领。PR 列表搜 `sub-issue`，只有已合并的 #3746，没有与本 issue 竞争的 PR。
- 补丁与 issue 对照：两个要求都做到了，一是每个 ticket 最多查 10 个子 issue（用 `islice`，`len()` 对 `fetch_sub_issues` 返回的 set 可用），二是 ticket 排在它的子 issue 前面。`sub_issues` 只在这两处使用，没有其他调用方会受顺序变化影响。GraphQL 的 `first: 100` 保持不变，这是合理取舍。
- Red/green：把 `pr_agent/` 回退到 HEAD~1，保留新测试，结果 2 failed / 49 passed；恢复补丁后 51 passed。再跑和 ticket/sub_issue 相关的单测，340 passed，1 xfailed。`ruff check` 两个改动文件都通过。
- 交付物：`0001-*.patch` 与 `git format-patch -1 HEAD` 的输出逐字一致。作者是 anyingiit noreply 邮箱，patch 里没有 AI 模型名。commit 符合 Conventional Commits。pr_body.md 是英文，有 Motivation/disclosure 段落和 `Closes #3794`。AUDIT.md 存在。
- 没有发现需要修改的问题，未改动 commit。

Status: ✅ ready（独立复核通过，可按“如何提交”提交）
