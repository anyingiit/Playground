# ruby/rdoc#1857 — meta description excerpts include link URL fragments

| 项 | 值 |
|---|---|
| Issue | https://github.com/ruby/rdoc/issues/1857 |
| Tier | 高星（ruby/rdoc，Ruby 官方） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~20:50 UTC：issue 无评论/assignee/关联 PR；open PR 无覆盖。草稿 PR #1787（st0012，comment markup source）和 #1617（移除 Darkfish）在相近区域，可能需 rebase |
| AI 政策 | AGENTS.md 允许 AI，但 PR 正文须 2–4 段、无 Test plan、**不加 AI 署名**，所以本正文没有 disclosure 段，提交时不要补 |
| Base | `master` @ 0b82ffd |
| DCO / CLA / CHANGELOG | 无 |
| 需先认领 | 否 |
| 优先级 | 低于其他：这是本轮第 3 个 rdoc PR（#1860、278 之后），可最后提交或隔天提交 |

## 改动
`Darkfish#excerpt`（Aliki 也用）在匹配前调用新的 `strip_links`：Markdown 注释把 `[text](url)` 换成文字、去掉图片；RDoc 注释把 `{text}[url]`、`text[url]` 换成文字；最后去掉裸 URL（保留句末标点，含 `<https://…>` autolink）。

## 验证
- darkfish 测试 39/0；回退 lib/ 后 3 个新测试失败（markdown 链接、rdoc 链接、裸 URL）。
- 全量 2557 个（复核时、采纳建议前），只剩已知环境失败 test_class_for_forbidden（root）；rubocop 无告警。
- issue 样例 `og:description` 从 "Foo. example." 变为 "Foo."。对 rdoc 自身文档，只有 CONTRIBUTING、doc/configuration、RDoc::TomDoc 三页描述变化。

## 如何提交
```
tools/submit_pr.sh contributions/281-ruby-rdoc-1857 ruby/rdoc master excerpt-links contributions/281-ruby-rdoc-1857/pr_title.txt contributions/281-ruby-rdoc-1857/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- PASS：新克隆 master 干净应用，红→绿、全量、rubocop、issue 样例、正文中"三页变化"说法均复现，符合 AGENTS.md。
- 采纳的建议：裸 URL 正则保留句末标点并处理 `<…>` autolink（原来会吞掉句号）；Markdown 链接正则加 `(?<![\w`])` 避免误伤 `a[0](x)` 这类代码；`strip_links` 标 `# :nodoc:`；正文如实描述 TomDoc 结果。改后加了裸 URL 测试并重跑 darkfish 测试和 rubocop。
- 未改（低优先）：`{text}[x]` 匹配任意目标，与 RDoc 渲染 tidy link 的行为一致。
