# higher-kinded-j/higher-kinded-j#1221 — 速查表 LazyPath/GenericPath 写了不存在的 run()

| 项 | 值 |
|---|---|
| Issue | https://github.com/higher-kinded-j/higher-kinded-j/issues/1221 （documentation, good first issue；2026-10-22 新开） |
| Tier | 新锐（Java 函数式库，活跃，外部 PR 合并快） |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 22:55 UTC：仓库 0 个 open PR，搜 1221 无 PR；issue 无评论/assignee |
| AI 政策 | 无禁令（仓库自带 .claude/skills，合并过 Cursor Agent 提交）；正文 Additional Comments 含 disclosure |
| Base | `main` @ ac42282 |
| DCO / CLA / 认领 | 无 / 无 / issue 欢迎评论认领，可选：提交时顺手评论 "I'd like to take this" |
| PR 模板 | 有，正文已按其结构填写 |

## 改动
- `hkj-book/src/cheatsheet.md`：LazyPath `.get()`，GenericPath `.runKind()`，WithStatePath `.run(initial)` → `StateTuple<S, A>`（issue 可选项）。
- `release-history/unreleased.md` Documentation 末尾加一行（PR 模板与 STYLE-GUIDE 要求用户可见改动写；先例 #1155）。注意：外部速查表 PR #1158/#1186 没写，维护者若要求删就删。

## 验证
`hkj-book/check.sh` exit 0（锚点、mermaid、页脚、可读性 baseline、英式拼写）。未跑 Gradle bookVerify（无 Java 片段改动，正文已说明且该框未勾）。

## 如何提交
```
tools/submit_pr.sh contributions/293-higher-kinded-j-1221 higher-kinded-j/higher-kinded-j main cheatsheet-extract-methods contributions/293-higher-kinded-j-1221/pr_title.txt contributions/293-higher-kinded-j-1221/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用；三个单元格与源码一致；书里其他页没有同样的错；check.sh 通过；无竞争 PR。建议：release note 措辞更顺 → 已改并重跑 check；bookVerify 合并框不要勾 → 已取消勾选；可评论认领 → 记在上表。
