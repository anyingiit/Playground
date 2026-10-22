# helix-editor/helix#11198 — SQL 接入 sqls 语言服务器

| 项 | 值 |
|---|---|
| Issue | https://github.com/helix-editor/helix/issues/11198 |
| Tier | 高星（helix ~45k★） |
| Labels | A-language-support, C-enhancement |
| Status | ✅ ready（独立复核 PASS，已按意见修改） |
| 重复 PR 检查 | 2026-10-22 21:00 UTC：`is:pr sqls` 0 条；`sql language server` 只有无关 #8675；issue 无 assignee、无关联 PR |
| AI 政策 | 无（同 360），正文含披露 |
| Base | `master` @ ba40e54 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
请求把 sqls 作为 SQL 的 LSP。2025-03 有人指出被 sqls#175 阻塞（sqls 关键字补全带 `documentation.kind = ""`，不是合法 MarkupKind，helix 反序列化失败）；2026-01 有人说上游已关；2026-03 有人求配置示例。sqls#176（2025-12-28）修复，现最新 v0.2.48（2026-07）。

## 改动
- `languages.toml`：在顶部按字母排序的 `[language-server]` 内联表加 `sqls = { command = "sqls" }`（spade-language-server 与 starpls 之间）；sql 加 `language-servers = [ "sqls" ]`。
- `book/src/generated/lang-support.md`：docgen 生成，只变 sql 行。

## 验证（红→绿以上游版本对照）
- sqls v0.2.27 vs v0.2.48，同一 `SEL` 补全请求（脚本 scratchpad/sqlprobe.py，HOME 指向空目录、无配置）：
  - 0.2.27：`"documentation":{"kind":"","value":""}` → 用 helix-lsp-types 反序列化 `CompletionItem` 报 "data did not match any variant of untagged enum Documentation"（红）
  - 0.2.48：无 documentation 字段 → 反序列化成功（绿）
- `cargo xtask docgen` 只改 sql 行；`hx --health sql` → `✓ sqls`。
- 注意：本机 helix 的增量构建一度没有感知 languages.toml 变化（xtask/hx 用了旧二进制），已 touch 后重建再生成，diff 确认只有 sql 行。

## 需要提交者注意
- 与 360 同仓库（helix），两个 PR 各自独立、改动行不重叠（都会改 lang-support.md 但不同行，languages.toml 中插入位置也不同（360 在 csharp-ls 后，361 在 spade-language-server 后），已验证两个补丁按顺序 `git am` 无冲突，可按任意顺序提交）。

## 如何提交
```
D=$PWD/contributions/361-helix-editor-helix-11198
tools/submit_pr.sh $D helix-editor/helix master sql-sqls-lsp $D/pr_title.txt $D/pr_body.md
```

## 独立复核（2026-10-22 21:15 UTC，独立 agent）
- issue open、无关联 PR；`sqls`/`11198`/`sql lsp` 搜 PR 无相关；sqls#176（2025-12-28）已合并，v0.2.48 为最新版。
- 新克隆 `git am` 干净；docgen 无差异。
- 实测：v0.2.27 补全带 `documentation:{kind:"",value:""}`，helix-lsp-types 反序列化失败；v0.2.48 无该键、反序列化成功。无配置时不崩溃、格式化可用，启动时发一条 Info 级 `no database connection` showMessage。
- 意见：①样式——简单 LSP 应写在顶部字母序 `[language-server]` 内联表 → 已改；②配置路径应写 `$XDG_CONFIG_HOME/sqls/config.yml`，并提及启动提示 → 已改正文。
- 结论：PASS（修正后）。修改后重验：docgen 无差异、`hx --health sql` ✓。
