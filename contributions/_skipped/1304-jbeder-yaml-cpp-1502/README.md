# jbeder/yaml-cpp#1502 — Wrong LF count at the end（literal 块标量尾部换行丢失）

| 项 | 值 |
|---|---|
| Issue | https://github.com/jbeder/yaml-cpp/issues/1502 |
| Tier | 高星 |
| Labels | 无 |
| Status | ⏭️ skipped — 已有开放 PR #1504（Closes #1502）；且仓库 AI 政策不鼓励此类“把 issue 丢给 AI 修”的 PR |
| Duplicate-PR check | 2026-10-01 ~23:01 UTC 复核：`pulls?q=1502` 命中 **#1504 "Preserve trailing newline in block chomping keep indicator (+)"**（Tyagiquamar，2026-10-01 开，Open，正文写明 Closes #1502，改 `src/emitterutils.cpp` + `test/integration/emitter_test.cpp`） |

## 跳过原因

1. **重复**：scout 之后（2026-10-01 当天）已有人提交 PR #1504，修的正是本 issue（同一文件、同一思路，并带回归测试）。按 brief 硬性要求 3 跳过。
2. **AI 政策（附带）**：`CONTRIBUTING.md` 的 “AI Usage” 一节：允许用 AI 写代码，但 AI 不能署名为 co-author、不能用 AI 写文档，并明确 “No 'low effort' AI PRs. Don't just paste an issue into Claude and ask it to fix it …”。即便没有重复 PR，这种志愿式 AI 修 issue 也属于该条款所担心的情形，需提交者本人深度理解/参与；加上 PR 描述可能被视为 AI 生成文本（规则 3），风险较高。

## 复核记录
- Issue：Open，无 assignee、无 label、无评论；作者希望发布含修复的版本。
- 基线：master @ 1e0876c（2026-09-17）。仅做了浅克隆用于读取 CONTRIBUTING，未构建/运行任何代码（故无 AUDIT.md）。
- 排除列表中无 yaml-cpp。
