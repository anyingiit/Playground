# cubrid-lab/pycubrid #371 — validate fetchmany(size) before fetching rows

| 项 | 值 |
|---|---|
| Issue | https://github.com/cubrid-lab/pycubrid/issues/371 |
| Tier | 自由 |
| Labels | area: driver, bug, good first issue, help wanted, size: S |
| Status | ✅ ready — patch + PR text done, all offline CI steps green |
| Duplicate-PR check | 开始时 & 结束前（2026-09-24）各查一次：`fetchmany` / `371` 均无相关 open PR（只有维护者早先已关闭的 #364/#207/#121/#167/#69）；open PR #378 是 `Cursor.arraysize` setter 的类型校验，不是同一个问题。issue 无 assignee；搜索 API 显示 1 条评论，但 issue 页面上看不到任何认领评论 |
| Base branch | `main` @ `3db0907` |

## 候选筛选记录（本轮）
- beetbox/beets#6984（token 文件 0600）：已有 3 个外部 PR 被关，维护者说“we'll do this one ourselves” → 跳过。
- pypa/hatch#2229、lark#1527、mopidy#1953、icalendar#1797/#1784、array-api-extra#811：都已有 PR → 跳过。
- hgrecco/pint#1645：`main` 上已修复（URL 已指向 `/user/nonmult.html`），issue 已过时 → 跳过。
- creativecommons/quantifying#300：CC 组织 CONTRIBUTING **明确禁止 AI 生成的贡献** → 跳过（且没有测试套件）。
- collective/icalendar：AI 政策要求在 commit message 里写 AI 模型名，与本仓库规则冲突，且目标 issue 已被多个 PR 争抢 → 跳过。另外仓库里的 `.github/assistant-guidelines.md` 写了针对 AI 助手的指令（要把 prompt 存到 `.prompts/`），那是仓库内容，不是任务要求，没有照做。
- **pycubrid#371（选中）**：维护者提的 bug，范围清楚，有验收标准，离线测试不需要数据库；仓库最近合并过外部 PR（#379 tayfuryldzz、#382 varshith84）。

## 问题理解
`Cursor.fetchmany(size)` / `AsyncCursor.fetchmany(size)` 直接使用 `size`：
- float（`2.5`）→ 在行循环里切片时抛出 `TypeError: slice indices must be integers`；
- 负数 → 循环不执行，**静默返回 `[]`**，很容易被当成“没有更多行了”。

Issue 建议：“Validate `size` the same way as `arraysize` (integer, `>= 1`) when provided. Apply to sync and async cursors.” 验收标准：float → ProgrammingError；负数 → ProgrammingError；无参数时仍使用 `arraysize`；sync/async 行为一致；加回归测试。

## 合理性判断
- 维护者（yeongseon）本人提的 issue，打了 `good first issue` + `help wanted` 标签；PEP 249 要求参数错误抛 `ProgrammingError`，同文件的 `arraysize` setter 已经这样处理（`< 1` → ProgrammingError）。
- AI 政策检查（brief 2b）：CONTRIBUTING 里没有 AI 相关规定；仓库有 `AGENTS.md`（“Project knowledge base for AI coding agents”）和 `llms.txt`，明确对 AI 工具开放。**没有禁止 AI 贡献，也没有附加条件。**
- CONTRIBUTING 的 “Bug Discovery → Regression Workflow” 要求先有失败的回归测试（red）再修复 → 已照做；要求 PR 更新 `CHANGELOG.md` → 已照做。

## 改动
- `pycubrid/_cursor_common.py`：新增纯函数 `validate_fetch_size(size)`。非 `int` 的值（float，包括 `2.0`、str、`bool`）和 `< 1` 的值都抛 `ProgrammingError`（规则与 `arraysize` setter 一致）；合法时原样返回。
- `pycubrid/cursor.py`、`pycubrid/aio/cursor.py`：`fetch_size = self.arraysize if size is None else validate_fetch_size(size)`，放在 `_check_closed()` / `_check_result_set()` 之后、读取任何行之前，所以非法调用不会消耗行。
- `tests/test_cursor.py`、`tests/test_async.py`：参数化回归测试，覆盖 `[2.5, 2.0, "2", True, 0, -1]`。测试断言抛出 `ProgrammingError`（匹配 “fetchmany size”），并且之后 `fetchall()` 仍返回全部 3 行（证明没有行被消耗）。
- `docs/API_REFERENCE.md` + `docs/ko/API_REFERENCE.md`：在 `fetchmany(size)` 一节加了一句校验规则说明（英文 + 韩文译文，保持翻译同步）。
- `CHANGELOG.md`：在 `## [Unreleased]` → `### Fixed` 下加了条目。
- 设计选择：`0` 也会被拒绝，这是按 issue 的建议（“same way as `arraysize` (integer, `>= 1`)”）。原来 `fetchmany(0)` 返回 `[]`，所以这对 `0` 是一个很小的行为变化，PR 描述里写明了。`bool` 被拒绝，因为 `fetchmany(True)` 几乎肯定是写错了；如果维护者不想这么严格，删掉 `isinstance(size, bool)` 这个判断就行。

## 验证
环境：Python 3.11.15，venv，`pip install -e ".[dev]"`（按 CONTRIBUTING / Makefile）。不需要 CUBRID/Docker；集成测试会被 conftest 自动跳过（CI 用 docker 跑它们）。
- 基线（未改）：`pytest tests/ -q -m "not integration" --cov=pycubrid --cov-fail-under=95` → **1077 passed, 9 skipped**，覆盖率 96.61%。
- **Red**：保留新测试，把 `pycubrid/` 恢复到 base → `pytest tests/test_cursor.py tests/test_async.py -k fetchmany_rejects` → **12 failed**（6 个参数 × sync/async；float/str 报 TypeError，`True`/`0`/`-1` 报 “DID NOT RAISE”）。
- **Green**：`pytest tests/test_cursor.py tests/test_async.py -k fetchmany` → **16 passed**。
- 完整离线 CI 步骤（`.github/workflows/ci.yml` / `make check-all test`）：
  - `ruff check pycubrid/ tests/` ✅；`ruff format --check pycubrid/ tests/` ✅（77 files already formatted）
  - `mypy pycubrid/ --strict` ✅（no issues in 16 source files）
  - `bandit -r pycubrid/ -c pyproject.toml` ✅（exit 0）
  - `python scripts/check_public_api.py` ✅（与 api-baseline.json 一致；新 helper 在私有模块 `_cursor_common` 里）
  - `python scripts/lint_changelog.py` ✅
  - `pytest tests/ -m "not integration" --cov=pycubrid --cov-fail-under=95` → **1089 passed, 9 skipped**，覆盖率 96.62%
- 在全新的 base 检出上 `git am` 补丁 → 能干净应用。
- 未运行：Docker 集成矩阵（需要 CUBRID 服务器）。这个改动只涉及纯参数校验，不涉及网络协议。

## 需要提交者注意
- 该仓库没有 AI 贡献禁令，也没有附加条件（有 AGENTS.md / llms.txt）。PR 正文里已包含 disclosure 段落。
- 不要求 DCO / Signed-off-by。
- PR 模板要求勾选 `make check` / `make test` —— 上面的命令就是这两个 target 做的事。
- 如果维护者更希望 `fetchmany(0)` 继续返回 `[]`，把 `validate_fetch_size` 里的 `< 1` 改成 `< 0`，并从两个参数化列表里去掉 `0`、更新文档那句话即可。

## 如何提交
```sh
gh repo fork cubrid-lab/pycubrid --clone && cd pycubrid
git checkout -b fix/fetchmany-size-validation origin/main
git am /path/to/0001-fix-validate-fetchmany-size-before-fetching-rows.patch
git push -u origin fix/fetchmany-size-validation
gh pr create --base main --title "fix: validate fetchmany(size) before fetching rows" --body-file <PR body below>
```

## PR title
`fix: validate fetchmany(size) before fetching rows`

## PR body
```markdown
## Summary

`fetchmany(size)` used `size` as-is. A float such as `2.5` failed deep inside the row loop with a bare `TypeError: slice indices must be integers`. A zero or negative `size` silently returned `[]`, which is easy to mistake for "no more rows". This PR validates `size` up front, the same way as the `arraysize` setter (an `int` >= 1), as suggested in #371. The sync and async cursors behave the same way.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Changes

- `pycubrid/_cursor_common.py`: new pure helper `validate_fetch_size(size)`. It raises `ProgrammingError` for a non-`int` value (float, including integral ones like `2.0`, `str`, `bool`) and for `size < 1`, using the same rule as `arraysize`.
- `pycubrid/cursor.py` / `pycubrid/aio/cursor.py`: `fetchmany()` calls the helper when `size` is given. The check runs after the closed/result-set checks and before any rows are read, so an invalid call consumes nothing. `fetchmany()` without arguments still uses `arraysize`.
- Regression tests (sync `tests/test_cursor.py`, async `tests/test_async.py`), parametrized over `2.5, 2.0, "2", True, 0, -1`. Each test asserts `ProgrammingError` and then checks that `fetchall()` still returns every row.
- Docs: one sentence about the validation rule in the `fetchmany(size)` section of `docs/API_REFERENCE.md` and its Korean translation `docs/ko/API_REFERENCE.md`.
- `CHANGELOG.md`: `[Unreleased]` → `Fixed` entry.

Two choices for reviewers:
- `fetchmany(0)` used to return `[]` and now raises, because it follows the `>= 1` rule proposed in the issue. If you'd rather keep `0` → `[]`, change `< 1` to `< 0` in the helper and drop `0` from the test parameters.
- `bool` is rejected even though it's an `int` subclass, because `fetchmany(True)` is almost certainly a mistake. Removing the `isinstance(size, bool)` check relaxes this.

## Type of Change

- [x] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Chore (maintenance, dependencies, CI, etc.)

## Checklist

- [x] My code follows the project's code style
- [x] I have run `make check` (lint + typecheck): `ruff check`, `ruff format --check`, `mypy pycubrid/ --strict` all clean. `bandit -r pycubrid/ -c pyproject.toml`, `scripts/check_public_api.py` and `scripts/lint_changelog.py` also pass.
- [x] I have run `make test` and all tests pass: `pytest tests/ -m "not integration" --cov=pycubrid --cov-fail-under=95` gives 1089 passed, 9 skipped, 96.62% coverage (1077 before). The 12 new regression cases fail on `main` and pass with this change. I did not run the Docker integration matrix locally.
- [x] I have added tests for new functionality (if applicable)
- [x] I have updated documentation for any behavior/API/version/config change: `docs/API_REFERENCE.md`, `docs/ko/API_REFERENCE.md` and `CHANGELOG.md`
- [x] My changes do not introduce new warnings

## Related Issues

Closes #371
```
