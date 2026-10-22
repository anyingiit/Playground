# benbalter/jekyll-optional-front-matter#67 — crash on non-hash config

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/jekyll-optional-front-matter/issues/67 （good first issue，10/4 维护者开） |
| Tier | 高星（GitHub Pages 默认启用的插件，~200★；benbalter 合并外部 PR 快） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~22:40 UTC：无评论、无 assignee、无关联 PR；`refs/pull` 最大 #68（已合并，无关） |
| AI 政策 | CLAUDE.md 只限制 agent 发版；无 AI 禁令；保留 disclosure 段 |
| Base | `main` @ 4b086ed |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 改动
`Generator#option` 加 `is_a?(Hash)` 守卫（与 jekyll-default-layout 一致），非 hash 配置视为未配置；specs 覆盖 `true` 和数组；CHANGELOG 加 `## Unreleased` 条目。

## 验证
- rspec 40/0；回退 lib/ 后 2 个新用例失败（NoMethodError / TypeError）。
- rubocop 无告警；`gem build` 成功（产物已删）。

## 如何提交
```
tools/submit_pr.sh contributions/287-benbalter-jekyll-optional-front-matter-67 benbalter/jekyll-optional-front-matter main non-hash-config contributions/287-benbalter-jekyll-optional-front-matter-67/pr_title.txt contributions/287-benbalter-jekyll-optional-front-matter-67/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- PASS：干净应用，红→绿复现；`option` 是唯一读这个配置的地方；与 default-layout 的守卫说法属实；标题风格与兄弟仓库一致。
- 采纳：之前贡献者 PR 自己加过 Unreleased 条目，所以补了 CHANGELOG；正文说明 `false` 仍被忽略，禁用要用 `enabled: false`。
