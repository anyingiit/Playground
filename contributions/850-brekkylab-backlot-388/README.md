# brekkylab/backlot#388 — hubspot `_flag`: only `true` selects the archived view

| 项 | 值 |
|---|---|
| Issue | https://github.com/brekkylab/backlot/issues/388 （拆自 #379 第 2 块） |
| Tier | 新锐 |
| Labels | fidelity, good first issue, hacktoberfest（**无 `agent`**） |
| Status | ✅ ready — patch + PR text done (not submitted); independently reviewed 2026-10-01 20:2x UTC |
| Base | `main` @ 0b08910 (2026-10-01 "Fix missing Gmail attachment error (400 instead of 404) (#394)") |
| Duplicate-PR check | 2026-10-01 18:1x UTC：`pulls?q=is:pr 388` 0 结果；`pulls?q=is:pr archived` 只有无关的 #327/#291/#275/#22；issue 0 评论、无 assignee、Development 无关联分支/PR；未打 `agent` 标签，所以仓库的 Claude Code routine 不会处理它 |

## 问题理解

HubSpot CRM v3 列表接口 `GET /crm/v3/objects/{type}?archived=...`。backlot 的 `_flag()` 把 `true`/`1`/`yes`（不区分大小写）都当成 true，返回 archived 视图。Issue 作者 2026-10-01 对真实 api.hubapi.com 实测：只有 `true`、`TRUE` 返回 archived；`1`、`yes`、`abc`、空串、不传都返回 active 记录。所以 `1`/`yes` 两种输入与真实 API 不一致。

## 合理性判断

- 项目宗旨就是"与真实 API 的差距最小"，CONTRIBUTING/AGENTS.md 明确"divergence from the real API is a bug"；issue 带 `fidelity` + `good first issue`，有实测数据，无需设计讨论。
- AI 政策：无禁令。仓库自己就用 Claude Code routine（只处理 `agent` 标签的 issue），本 issue 未打 `agent`，也无 bot PR。CLAUDE.md 仅 "Follow AGENTS.md"。
- AGENTS.md 规定：注释写"测量了什么"，不写修复历史；commit 标题为单句陈述新状态、**无 trailer**；PR/issue 正文段落不硬换行。均已遵守（commit 无 Signed-off-by、无 Co-authored-by）。

## 改动

- `backlot/routers/hubspot.py`：`_flag` 改为 `str(raw or "").strip().lower() == "true"`；docstring 改为记录 #388 的实测结果。
- `tests/test_hubspot.py`：新增参数化测试 `test_hubspot_archived_reads_only_true_as_true`（true/TRUE → 只返回 archived 公司 "Defunct Labs"；1/yes/abc/空串/不传 → 3 个 active 公司）。用 companies 而不是 contacts，因为样本库里唯一的 archived 记录是公司，且路由对所有 object type 共用。

## 验证

环境：`UV_CACHE_DIR=<work>/.uvcache uv sync --extra dev --locked`（Python 3.11.x，`.[dev]`；CI 用 `--all-extras`，太重未装）。pytest 默认 `-n auto`，这里用 `-n 2` 限制并行。

| 命令 | 结果 |
|---|---|
| 修复前（仅新测试）`pytest -n 2 tests/test_hubspot.py -k archived_reads_only` | **2 failed**（`[1-False]`、`[yes-False]`：返回了 `['Defunct Labs']`），5 passed → red |
| 提交后把 router 回退到 HEAD~1：`pytest -n 2 tests/test_hubspot.py` | 2 failed, 39 passed → red |
| 修复后 `pytest -n 2 tests/test_hubspot.py` | 41 passed → green |
| 修复后全量 `pytest -n 2` | 3771 passed, 38 skipped（skip 全是 extras 门控文件：official-sdk/llamaindex/mcp/mirage/fsspec，未安装） |
| `ruff check . && ruff format --check .` | All checks passed! / 143 files already formatted |

独立复核（2026-10-01 ~20:20 UTC）：重新 `uv sync --extra dev --locked`，回退 router 后 `tests/test_hubspot.py` 2 failed（`[1-False]`、`[yes-False]`），恢复后 41 passed；全量 `pytest -n 2` 3771 passed, 38 skipped；ruff check/format 通过。复查 issue 仍 open、无 assignee、无评论、无 `agent` 标签；`pulls?q=is:pr 388`/`hubspot`/open PR 列表均无重复 PR。

未运行：CI 的 `--all-extras` 测试矩阵和 Linear TS 示例（与此改动无关的可选面）。

## 如何提交

```bash
git clone https://github.com/brekkylab/backlot && cd backlot
git checkout -b hubspot-archived-true-only origin/main
git am /path/to/0001-hubspot-archived-reads-only-true-as-true-so-archived.patch
git push <your-fork> hubspot-archived-true-only   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`（已按仓库 PR 模板：What changed / Why this is what the real API does / Verification + 三个勾选项，并加入披露段落）。

## 需要提交者注意

- `hacktoberfest` 标签描述写着 "comment on the issue to be assigned"——建议提交前先在 issue 下评论认领（本环境不能写 GitHub）。
- 首次 PR 的 CI 需维护者批准才运行。
- AGENTS.md：PR 正文段落一行不换行（pr_body.md 已如此）；commit 无 trailer。
- 测量数据来自 issue 作者（2026-10-01），我们没有自己调用真实 HubSpot API；PR 正文已说明。`True`（混合大小写）、带空格的值未被测量，补丁保留原有 `lower()`/`strip()` 行为，若维护者要求可再调整。
