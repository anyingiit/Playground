# astropy/astropy#15557 — SlicedLowLevelWCS does not handle negative indexing correctly

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/astropy/astropy/issues/15557 |
| Tier | 高星（>5k stars, very active） |
| Labels | Bug, wcs.wcsapi |
| Status | ✅ ready — patch + PR text done |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论认领；无 open/merged PR。#20320/#20323（IMGillusion）已于 2026-09-12 被 @pllim 以违反 AI policy（自治 agent 提交）为由关闭，标 `invalid` |
| Base | `main` @ bab4b9c4 |

## 问题理解
`SlicedLowLevelWCS(wcs, slice(-3, None))` 把 -3 当作像素坐标 -3（第一个像素左边），而不是 NumPy 语义的"倒数第 3 个"，导致世界坐标静默算错。issue 建议：要么报错，要么在已知轴长时转换为正索引。

## 合理性判断
Bug 标签、维护者 @astrofrog 在 #20320 的技术评审里明确倾向："WCS 有 shape 时正确支持负索引，shape 未知时才报错"，并建议在 `__init__` 里归一化。本补丁按此方向独立实现。

## 改动
- `astropy/wcs/wcsapi/wrappers/sliced_wcs.py`：新增 `_resolve_negative_indices(slices, array_shape)`，在 `sanitize_slices` 之后、与已有切片合并之前，用被切 WCS 的 `array_shape` 把负的整数索引、负的 slice start/stop 转成非负（slice 越界下限截到 0，整数 < -size 报 `IndexError`）；`array_shape` 为 None 时遇到负值抛 `IndexError`。非负值完全不变。类 docstring 补一句说明。
- 测试：`test_sliced_wcs.py` 新增 `test_negative_indices`（含 issue 例子、负 stop、越界负 start、负整数）、`test_negative_indices_nested`（`[2:8]` 再 `[1:-1]`）、`test_negative_indices_no_shape`、`test_negative_integer_index_out_of_range`。
- 变更日志：`docs/changes/wcs/15557.bugfix.rst`。

## 验证（Python 3.12 venv，`uv pip install -e ".[test]"` + matplotlib）
- 红：撤回源码改动，`pytest astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py` → 9 failed, 42 passed
- 绿：同命令 → 51 passed
- issue 原例子输出 `[100.6 100.8 101. ]`
- `pytest -n 2 astropy/wcs/wcsapi astropy/nddata` → 1406 passed, 69 skipped
- `pytest -n 3 astropy/wcs` → 611 passed, 23 skipped, 1 xfailed
- `pytest -n 3 astropy/visualization/wcsaxes` → 261 passed, 63 skipped（无 pytest-mpl，图像比对跳过）
- `ruff check` / `ruff format --check`（与 pre-commit 同版本 0.15.20）→ clean

## 需要提交者注意
- ⚠️ **AI policy 风险较高**：astropy AI policy（astropy-project/policies/ai-policy.md）允许 AI 辅助但要求：披露、能自己解释全部改动、**亲自**回应评审（不能转贴 AI 回复）、"Autonomous workflows (agents) are not human contributors"。同一 issue 的上一个 AI PR（#20320）就是因为作者自称自治 agent 被关并警告封禁。请务必自己读懂补丁、亲自回复评审；若不打算亲自跟进，请不要提交。
- PR 模板 **必填 AI Disclosure 且要求写出具体模型与版本**：请把 pr_body.md 中的 `MODEL_AND_VERSION_TO_FILL` 替换为实际模型/版本（我们的约定是 commit 里不写模型名，PR 模板这里要求写）。
- 模板里的 "I certify that I am human..." 复选框需提交者本人确认后勾选。
- PR 开出后把 `docs/changes/wcs/15557.bugfix.rst` 重命名为 `<PR号>.bugfix.rst`（astropy changelog 检查要求用 PR 号），追加一个 commit 即可。
- 不需要 DCO / Signed-off-by；无 AI trailer 要求。
- 与 #20320 实现思路相似（维护者建议的方向），本补丁为独立实现。

## 如何提交
```bash
tools/submit_pr.sh contributions/608-astropy-astropy-15557 astropy/astropy main fix-sliced-wcs-negative-indices contributions/608-astropy-astropy-15557/pr_title.txt contributions/608-astropy-astropy-15557/pr_body.md
```
手动方式：fork 后 `git checkout -b fix-sliced-wcs-negative-indices origin/main && git am 0001-*.patch && git push`，再用 pr_title.txt / pr_body.md 开 PR。
