# Enter-tainer/typstyle #478 — wrapped list items indented by tab-width

| 项 | 值 |
|---|---|
| Issue | https://github.com/Enter-tainer/typstyle/issues/478 |
| Tier | 自由 |
| Labels | bug |
| Status | ✅ ready — patch + PR text done（独立复核 2026-10-01：git am 干净应用于 master@57a34b7，red 4 失败 → green 30 passed） |
| 重复 PR 检查 | /pulls?q=478 无相关 PR；issue open、无 assignee、无评论（2026-10-01） |
| AI 政策 | 仓库自带 CLAUDE.md（面向 Claude Code 的开发指南），CONTRIBUTING / PR 模板 / labels 无 AI 限制 |

## 问题理解
设置 `--tab-width=4`（`tab_spaces`）后，列表项折行的悬挂缩进变成 4 空格；期望无论 tab-width 为多少都缩进 2 空格（与 `- ` 对齐）。
根因：`crates/typstyle-core/src/pretty/markup.rs` 中 `convert_list_item_like`（list/enum）和 `convert_term_item` 用 `self.indent(body)`，即 `nest(tab_spaces)`。

## 合理性判断
Bug label，作者给了期望输出；默认 tab=2 时行为一致，修复只影响非默认 tab-width。合理。

## 改动
- 新增 `indent_item()`：item body 固定 `nest(2)`，替换两处 `self.indent(body)`。
- 新 fixture `tests/fixtures/unit/markup/list-indent-tab4.typ`（`tab_spaces=4 wrap_text`）+ 4 个 snapshot（0/40/80/120）。
- CHANGELOG.md 新增 `## Unreleased` 条目（PR 模板要求更新 CHANGELOG）。

## 验证
- Red：去掉修复跑 `cargo test -p typstyle-tests --test tests -- list-indent-tab4` → 4 个 snapshot 失败（折行缩进 4 空格）；Green：10 passed。
- `cargo test -p typstyle-tests --test tests -- --skip e2e` → 2675 passed（e2e 需拉取外部仓库，未跑）
- `cargo test -p typstyle-core` → 25 passed；`cargo test -p typstyle --test test_style_args` → 6 passed
- `cargo clippy -p typstyle-core -p typstyle-tests --all-targets --all-features` 无警告；`cargo fmt --check --all` 通过
- 现有快照零变化（默认 tab=2 输出不变）。

## 需要提交者注意
- 设计取舍：非默认 tab-width 下，**嵌套列表项**也改为 2 空格缩进（不再跟随 tab_spaces）。PR 正文已说明并表示可调整，维护者可能有不同偏好。
- 无 DCO / AI trailer 要求；commit 作者为 anyingiit noreply 邮箱。
- PR 使用仓库模板（Summary/Changes/Checklist/Testing）并加入 motivation/disclosure 段落。
- 上游默认分支为 `master`；仓库已迁移到 `typstyle-rs/typstyle`（旧 URL 重定向），提交时用 `typstyle-rs/typstyle` 作为 upstream。

## 如何提交
```bash
git clone https://github.com/typstyle-rs/typstyle && cd typstyle
git checkout -b fix/list-item-indent-tab-width
git am /path/to/0001-fix-do-not-use-tab-width-for-list-item-indentation.patch
tools/submit_pr.sh <folder> typstyle-rs/typstyle master fix/list-item-indent-tab-width <folder>/pr_title.txt <folder>/pr_body.md
```
