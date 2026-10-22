# 398 — zerobrewhq/zerobrew#376 新增 `zb bundle check`

| 项 | 值 |
|---|---|
| Issue | https://github.com/zerobrewhq/zerobrew/issues/376 |
| Tier | 新锐（Rust 写的 Homebrew 替代，两年内创建，增长快，测试全） |
| Labels | type: feature, area: cli, area: install, priority: medium, status: accepted |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳其建议） |
| 重复 PR 检查 | 2026-10-22 22:10 UTC：issue 无评论、无认领、Development 空；搜索 `is:pr bundle` 仅我们的 #480 开放（无关） |
| AI 政策 | 无禁止 AI 规定 |
| Base | `main` @ c24141a |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
用户在 `.envrc` 里用 `brew bundle check`；zerobrew 没有对应命令，`zb bundle` 每次都会重新下载。issue 给出两个方案：支持 `zb bundle check`，或者再次 install 时不重新下载。本补丁实现前者（issue 标题的第一个选项），不改 `bundle install` 的行为（是否跳过已安装/过期包属维护者决策，PR 正文已说明）。

## 改动
- `cli.rs`：`BundleCommands::Check { file }`（`-f`，默认 `Brewfile`），加解析测试。
- `bundle.rs`：`check_file` 用 `load_manifest` 读 Brewfile，`missing_entries` 对每项走 `normalize_formula_name`（与 `zb install` 记录到 DB 的名字一致：`homebrew/core/x`→`x`，`homebrew/cask/x`→`cask:x`，tap 保留全名），用 `installer.is_installed` 查本地 DB。全部安装：打印 "The Brewfile's dependencies are satisfied." 退出 0；否则列出缺失项并返回 `ExecutionError`（退出 1）。不联网。
- README 命令示例一行；CHANGELOG `[Unreleased] / Added` 一条。
- `zb-brew` 已转发 `bundle`，因此 `brew bundle check` 经别名也可用。

## 验证
- 红：main 上 `zb bundle check` → `error: unrecognized subcommand 'check'`；变异（去掉名字规范化）→ `missing_entries_uses_installed_names` 失败。
- 绿：`cargo test -p zb_cli --lib bundle` 12 个全过（新增 3 个 + CLI 解析 1 个）。
- 手动：新建 `ZEROBREW_ROOT`，Brewfile 含 jq 和 cask firefox → 退出 1 并列出两项；DB 记录两者后 → 退出 0。
- `cargo test -p zb_cli --no-fail-fast`：仅 4 个失败，与 baseline 相同（root 运行）。clippy `-D warnings`、fmt 干净。

## 独立复核 PASS
VERDICT PASS。采纳：默认 Brewfile 时提示省略 `-f`；PR 正文说明别名/旧名会被报缺失、只查是否安装不查过期、`brew bundle check` 经 zb-brew 别名可用。未采纳（可选）：通过 opt/ 链接解析别名（范围扩大，正文已表示可追加）。

## 需要提交者注意
- 与 393、394（同仓库）改的文件不同，可任意顺序提交。
