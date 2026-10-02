# spec-kitty/spec-kitty#4292: mypy strict no-any-return errors in agent_profiles/repository.py

| 项 | 值 |
|---|---|
| Issue | https://github.com/spec-kitty/spec-kitty/issues/4292 |
| Tier | 新锐 |
| Labels | domain:charter, good first issue, priority:P3, status:ready, tech-debt |
| Status | ✅ ready（patch 和 PR 文本已完成，独立复审通过，尚未提交） |
| Base | `main` @ `d78aa2345e61`（2026-10-01） |
| Duplicate-PR check | 2026-10-01 18:30 和 18:47 UTC 各查一次 `pulls?q=4292`，以及关键词 `repository.py no-any-return agent_profiles`。只找到 #4293，它是提出本 issue 的那个已合并 PR（#2715 follow-up），并没有修这三处。issue 没有评论、没有 assignee、没有 `status:claimed` 或 `taken-by-human` 标签 |

## 独立复审（2026-10-01 20:30 UTC）

- 复查 issue：仍 open、无 assignee、无评论；`pulls?q=4292` 只有已合并的 #4293，`is:open no-any-return` 无结果，没有重复 PR。
- 重建 venv 后亲自复跑：改动前 `mypy --strict` 3 errors（164/270/956），改动后 Success；gate 测试去掉 src 改动 1 failed，带上 1 passed；`tests/doctrine/agent_profiles` 等相关测试 187 passed（未含 lineage_accessor 文件）；ruff check / format 通过。
- 核对三个注解类型与被调方真实声明一致（`profile.py` 中 `routing_priority: int`，`built_in_dir -> Path`，`profile_channel_reachable -> frozenset[str]`）；PR 正文符合仓库 5 段模板；patch 与 commit 一致、作者正确、无 AI 模型名。未发现需要修改的问题。

## 问题理解

单独对 `src/charter/offering/agent_profiles/repository.py` 跑 `mypy --strict` 时，会报 3 个 `no-any-return`。issue 写的是 163/268/922 行，当前 main 上实际是 164/270/956 行。

原因是 `pyproject.toml` 里有一条 `charter.*` 的 `follow_imports = "skip"` override。它让单文件检查时，其他 charter 模块导入的符号（`AgentProfile`、`built_in_dir`、`profile_channel_reachable`）都被当成 `Any`。下面三个函数直接 return 了这些值：

- `_score_profile() -> float`，返回 `profile.routing_priority` 参与的表达式
- `_default_built_in_dir() -> Path`
- `profile_channel_reached() -> frozenset[str]`

issue 的建议是在每个 return 前加带注解的局部变量或做类型收窄，不要用 suppress。

## 合理性判断

- 维护者把 issue 标成了 `good first issue` + `status:ready` + `tech-debt`。charter 的质量门要求 `mypy --strict` 通过，所以需求明确，也在范围内。
- AI 政策：CONTRIBUTING.md 欢迎 AI 辅助贡献，但要求在 PR 里披露 AI 用了多少（PR 正文已写明）。仓库本身由 agent fleet 维护，没有 AI 禁令。
- 不需要设计讨论：改动不改变任何运行时行为。

## 改动

- `src/charter/offering/agent_profiles/repository.py`：三处 return 前各加一个带注解的局部变量，类型就是被调函数真实声明的类型：`routing_priority: int`、`profiles_dir: Path`、`reached: frozenset[str]`。没有用 `type: ignore` 或 `cast`，也没有改 pyproject 的 mypy override。
- 新增 `tests/doctrine/agent_profiles/test_repository_mypy_strict.py`：用 `sys.executable -m mypy --strict` 检查该文件，断言 exit 0 且输出里没有 `no-any-return`。写法照搬仓库里已有的 `tests/cross_cutting/test_mypy_strict_mission_step_contracts.py` 和 `tests/specify_cli/missions/test_read_path_resolver_redundant_cast_gate.py`，marker 也一样用 `integration` + `slow`。

## 验证

环境：在 `/home/user/work/spec-kitty` 里执行 `uv sync --frozen --extra test --extra lint`，Python venv 放在仓库内 `.venv`。

| 命令 | 结果 |
|---|---|
| `.venv/bin/python -m mypy --strict src/charter/offering/agent_profiles/repository.py`（改动前） | **3 errors**（164/270/956 行，no-any-return）→ red |
| 同上（改动后） | `Success: no issues found in 1 source file` → green |
| 同上，不带 `--strict`（pyproject 本身就设了 `strict = true`） | Success |
| `pytest -q tests/doctrine/agent_profiles/test_repository_mypy_strict.py -n0`，`git stash` 掉 src 改动只保留测试 | **1 failed**（输出列出 3 个 no-any-return）→ red |
| 同上，带上 src 改动 | 1 passed → green |
| `pytest -q -n2 tests/doctrine/agent_profiles tests/charter/test_profile_channel_delivery.py tests/charter/test_context_profile.py tests/charter/test_doctrine_service_lineage_accessor.py tests/architectural/test_charter_sole_door_agent_profile_repository.py` | 192 passed |
| `pytest -q -n2` 跑 6 个 marker/shard 架构 gate（fast_tier_marker_completeness、marker_job_completeness、module_shard_registry、interpreter_shard_coverage、quarantine_marker、performance_marker_guard） | 73 passed |
| `ruff check <两个文件>` | All checks passed |
| `ruff format --check .`（CI `ci-quality.yml` 用的就是这条命令） | 2953 files already formatted。注意 repository.py 在 ruff format 的 exclude 列表里，所以单独 `ruff format --check <path>` 会提示要改格式，加 `--force-exclude` 后就不报了。这个情况改动前就存在，与本 patch 无关 |
| `mypy --strict tests/doctrine/agent_profiles/test_repository_mypy_strict.py` | Success |

没跑的：全量测试套件和整个 `tests/architectural/`。charter 明确禁止在 mission 工作里跑全量重型套件（`NO_FULL_HEAVY_SUITES_IN_MISSION`），而且这次改动只涉及类型注解。

## 如何提交

```bash
git clone https://github.com/spec-kitty/spec-kitty && cd spec-kitty
git checkout -b issue-4292-repository-no-any-return origin/main   # 仓库约定的分支名格式是 issue-<n>-<slug>
git am /path/to/0001-fix-charter-narrow-three-no-any-return-returns-in-ag.patch
git push <your-fork> issue-4292-repository-no-any-return
# 开 PR，目标分支 main，先开成 draft；标题用 pr_title.txt，正文用 pr_body.md
```

### 需要提交者注意

- **先 claim**：仓库用 label 驱动的 agent fleet，`status:ready` 正是 fleet 的领取队列，可能有 fleet VM 正在或即将处理这个 issue。按 CONTRIBUTING 的说法，人类贡献者开始做时应该加 `status:claimed` + `taken-by-human`，并评论 `claimed by <harness>/<model> on <machine>`。外部贡献者多半没有加 label 的权限，可以在 issue 里留言说明。提交前请再查一次有没有 fleet PR。
- PR 正文用的是仓库模板要求的 5 个固定小节（Issue / Change / Tests run / Blast radius / Deferred），模板注释说正文不按格式写会被 squad 判 MAJOR。所以 chefs-pick 的 motivation/disclosure 段落放进了 `## Change`，测试清单放在 `## Tests run`。标题格式 `[#<n>] ...` 也是模板要求的。
- AI 披露是 CONTRIBUTING 的硬性要求，pr_body.md 里已经写了。仓库还要求贡献者自己理解并测试过改动，请提交前过一遍 diff。PR 里如果有评论是 AI 生成的回复，也需要披露。
- 提交信息用 Conventional Commits（commitlint 的 type-enum 包含 `fix`）。不需要 DCO 和 changelog：模板只要求面向用户的改动写 changelog，这次不是。
- charter 的 ATDD 条款要求"测试作为单独 commit 先提交"，但那是针对 mission/WP 流程的。这里按我们的规则做成了单个 commit，red→green 过程已在上面记录。如果维护者要求，可以拆成两个 commit：先提交测试，再提交修复。
- 新测试带 `integration` + `slow` marker，和已有的同类 mypy gate 测试一致。所以它可能只在 nightly 或 full 跑道里执行，而不是每个 PR 都跑。
- charter 里"开始工作时把 issue 分配给 HiC""遇到既有失败要开 issue"这类规则是针对内部 agent 的。本次没有碰到既有失败。
