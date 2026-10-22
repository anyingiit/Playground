# vitruv-tools/methodologistUI-backend#372 — NotFoundException 文案重复 "not found not found!"

| 项 | 值 |
|---|---|
| Issue | https://github.com/vitruv-tools/methodologistUI-backend/issues/372 （bug, good first issue；2026-10-22 新开） |
| Tier | 自由（KIT Vitruv 项目的 Spring Boot 后端） |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 23:10 UTC：issue 无评论/assignee/关联 PR；open PR #371、#377 处理别的 issue（#377 与本补丁 import 块会有一行冲突，正文已说明） |
| AI 政策 | AGENTS.md 面向 AI 代理与人类，无禁令、无署名限制；正文含 disclosure |
| Base | **`develop`** @ 1d91739（AGENTS.md 要求 PR 指向 develop） |
| DCO / CLA / 认领 | 无 / 无 / 不需要 |

## 改动
- 新增 `RULE_SET_NOT_FOUND_ERROR = "RuleSet"`；ConstraintRuleSetService 的 RuleSet/VSUM 查找、FileStorageService#updateFile 改用常量（VSUM 复用 `VSUM_ID_NOT_FOUND_ERROR`）。
- `METAMODEL_IDS_NOT_FOUND_IN_THIS_VSUM_NOT_FOUND_ERROR` 值改为 "MetaModel Ids in this VSUM"。
- 测试：`hasMessageContaining` 改 `hasMessage` 精确断言，补两处消息断言；控制器测试桩同步。

## 验证
- 去掉主代码改动后 5 处断言失败（如 `File not found not found!`），加上后通过。
- `mvn verify -pl app -am`：Spotless + 487 个测试通过。CI 的 Checkstyle action 未在本地跑（app 模块的 checkstyle 配置在 develop 上本身缺 suppressions 文件）。

## 如何提交
```
tools/submit_pr.sh contributions/297-vitruv-methodologist-372 vitruv-tools/methodologistUI-backend develop not-found-messages contributions/297-vitruv-methodologist-372/pr_title.txt contributions/297-vitruv-methodologist-372/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆 develop 干净应用；所有 NotFoundException 调用都已用常量，无遗漏；常量选择一致；红→绿复现（63 中 5 失败→全过）；符合 AGENTS.md。指出与 #377 的 import 冲突 → 正文已加说明；"Four places" 措辞 → 已改。
