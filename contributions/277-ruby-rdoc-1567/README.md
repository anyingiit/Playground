# ruby/rdoc#1567 — `rdoc -C1` reports alias method arguments as uncovered

| 项 | 值 |
|---|---|
| Issue | https://github.com/ruby/rdoc/issues/1567 |
| Tier | 高星（ruby/rdoc，Ruby 官方） |
| Labels | 无 |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~20:45 UTC：issue 无评论/assignee；唯一相关 PR #1780 已被作者关闭（维护者 st0012 问"只查一层，是否应查到链尾"后作者没回）；open PR 中无引用 1567 的 |
| AI 政策 | 仓库有 AGENTS.md，欢迎 AI 辅助，但要求 **PR 正文 2–4 段、无 Test plan、不加任何 AI 署名或会话链接**。所以本 PR 正文**不含**我们惯用的 Motivation/disclosure 段，提交时不要补 |
| Base | `master` @ 0b82ffd |
| DCO / CLA / CHANGELOG | 无（History.rdoc 由发布时维护） |
| 需先认领 | 否 |

## 改动
`Stats#undoc_params` 改用 `documenting_comment(method)`：方法自身无注释时，沿 `is_alias_for || see` 链（与 `MethodAttr#documented?` 一致）找到第一个有注释的方法，有环保护。别名的别名、多层未注释 override 都覆盖了，正面回应了 #1780 里维护者"应查到链尾"的问题。

## 验证
- stats 测试 43/0；回退 lib/ 后 4 个新测试失败。
- 全量 `rake test` 2560 个，前后都只有两个环境性失败（root 运行导致 test_class_for_forbidden；US-ASCII locale 的 Aliki 测试），LANG=C.UTF-8 下 Aliki 通过。
- rubocop 无告警；issue 样例 `-C1` 从 6 个未文档化参数变为 0。

## 如何提交
```
tools/submit_pr.sh contributions/277-ruby-rdoc-1567 ruby/rdoc master alias-param-coverage contributions/277-ruby-rdoc-1567/pr_title.txt contributions/277-ruby-rdoc-1567/pr_body.md
```

## 独立复核（2026-10-22，独立 agent，两轮）
- 第一轮 FAIL：#1780 的评审"一层继承"指的是 `see`（父类方法），初版只跟了别名链；建议跟 `is_alias_for || see`，方法加 :nodoc:，RBS 返回类型加 Markup::Document → 全部已改，并加 C < B < A override 测试。
- 第二轮 PASS：新克隆 master 干净应用，红→绿、全量、rubocop、样例均复现；正文符合 AGENTS.md。建议正文补一句 override 行为 → 已补。
