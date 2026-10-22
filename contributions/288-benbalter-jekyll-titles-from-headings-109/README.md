# benbalter/jekyll-titles-from-headings#109 — explicit titles overwritten with `collections: true`

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/jekyll-titles-from-headings/issues/109 （good first issue，维护者 10/4 开，写明了修法和要的测试） |
| Tier | 高星（GitHub Pages 默认插件之一，~100★；benbalter 合并外部 PR 快） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~22:30 UTC：无评论、无 assignee、无关联 PR；`refs/pull` 最大 #110（已合并，无关） |
| AI 政策 | CLAUDE.md 只限制 agent 发版；无 AI 禁令；保留 disclosure 段 |
| Base | `main` @ 457264d |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 改动
`inferred_title?`：只有当文档标题等于"文件名 slug 的 titleize"时才视为推断标题（按 Jekyll `populate_title` 的方式取 slug，兼容 Jekyll 3/4 对末尾句点的差异，忽略 front matter 的 `slug:`）。新增两个 fixture post 和 3 个 spec，CHANGELOG 加 `## Unreleased / ### Fixed`。

## 验证
- rspec 48/0（Jekyll 4.4.1 和 3.10.0 都跑过）；回退 lib/ 后 2 个显式标题用例失败（custom slug 用例防止误用 `data["slug"]`）。
- rubocop 无告警（新 spec 内联取文档，避免 `RSpec/MultipleMemoizedHelpers` 超限）。

## 如何提交
```
tools/submit_pr.sh contributions/288-benbalter-jekyll-titles-from-headings-109 benbalter/jekyll-titles-from-headings main keep-explicit-document-titles contributions/288-benbalter-jekyll-titles-from-headings-109/pr_title.txt contributions/288-benbalter-jekyll-titles-from-headings-109/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- PASS：干净应用，红→绿复现，Jekyll 3/4 都通过；草稿、嵌套目录、带点文件名等边界在临时站点验证正常；fixture 不影响其他用例；issue 要求的三项测试齐全。
- 采纳：Jekyll 3 不去末尾句点，现在两种 slug 形式都接受；正文说明"front matter defaults 设置的 title 现在算显式"。
