# 395 — sinelaw/fresh#3074 退出的终端在重启编辑器后丢失自动标签名

| 项 | 值 |
|---|---|
| Issue | https://github.com/sinelaw/fresh/issues/3074 |
| Tier | 新锐（Rust 终端编辑器，2025 年起，增长很快，测试非常全） |
| Labels | actionable, triaged, tui-agent-auto-bug（维护者 9-02 标记 actionable） |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳其建议） |
| 重复 PR 检查 | 2026-10-22 21:00 UTC：issue 无评论、无 assignee、Development 空；无相关开放 PR |
| AI 政策 | CONTRIBUTING 无 AI 条款；维护者自己大量用 Claude（提交带 Co-authored-by: Claude） |
| Base | `master` @ 4caedcd |
| DCO / CLA | 无；PR 模板有一个 GPL-3.0-or-later 许可勾选框（pr_body 已勾） |
| 需先认领 | 否 |

## 问题理解
自动命名的终端（标签 `bash — <cwd>`）在退出后保存工作区，重开时变成 `*Terminal N* (exited)`。原因：只持久化显式标题；自动名靠活进程推导，恢复的死终端没有进程。

## 改动
- `ExitedTerminal` 新增 `auto_title`：退出时若非显式标题，记下当时的自动名（过滤掉 `*Terminal {id}*` 回退名）。
- `ExitedTerminalState`（工作区序列化）新增可选字段 `auto_title`（serde default/skip，旧文件兼容）；保存时写入，恢复死终端时放回标签（不标为显式），重启路径不变，新进程会重新命名。
- 新 e2e 测试 `test_exited_auto_named_terminal_keeps_its_name_across_an_editor_restart`（仅 Linux）。

## 验证
- 红：回退 src → 新测试失败，`Tab bar:  *Terminal 0* (exited)`；绿：通过，连跑 5 次稳定。
- `cargo test --test all_tests terminal`：203 passed；lib `workspace`/`exited_terminal`：82 passed；`restart_exited_terminal` 7 个全过。
- `cargo fmt`、`cargo check --all-targets -p fresh-editor` 通过；`cargo clippy --all-targets`（CI 用的普通模式）退出 0，警告均为既有代码。
- 独立复核 agent：VERDICT PASS；采纳：测试补“重启后重新自动命名”一步、用键盘输入 `exit`、PR 正文说明只测了本地单窗口；提交信息加 `Assisted-by: Claude Code`（上游提交惯例带 Claude 署名）。

## 如何提交
```
git clone https://github.com/sinelaw/fresh && cd fresh
git checkout -b keep-exited-terminal-auto-title origin/master
git am /path/to/0001-Keep-an-exited-terminal-s-auto-derived-tab-name-acro.patch
```
PR 正文按仓库模板（简短说明 + 许可勾选框），含披露段落。
