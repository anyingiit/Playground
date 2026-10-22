# authorjapps/zerocode#800 — 允许只有 name 和 request 的极简 echo step

| 项 | 值 |
|---|---|
| Issue | https://github.com/authorjapps/zerocode/issues/800 （good first issue，2026-10-22 维护者新开） |
| Tier | 高星（zerocode ~900★，Java） |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 23:00 UTC：issue 无评论/assignee/关联分支；PR 搜 800 无结果 |
| AI 政策 | 无；正文含 Disclosure 段 |
| Base | `master` @ d6694c4 |
| DCO / CLA / 认领 | 无 / 无 / 不需要（CONTRIBUTING 建议先开 issue，本 issue 即维护者所开） |
| 提交信息 | 按 CONTRIBUTING：`ISSUE-800 # ...`（≤70 字符，无特殊字符） |
| PR 模板 | 有，正文按其结构填写 |

## 改动
`ZeroCodeMultiStepsScenarioRunnerImpl`：`executeApi` 把缺失的 url 当空串（原来 NPE）；`compareStepResults` 对不发调用（ApiType.NONE）且无 assertions/verify/validators 的步骤直接通过。新增 `ZeroCodeMultiStepsScenarioRunner_EchoStepTest` + `e2e/EchoStepShortForm` + 两个场景 JSON。

## 验证
- 新测试：无修复时红（store_ids 步 NPE），有修复时绿；Java 调用不写 assertions 仍失败。
- `mvn -pl core test` 457 个，只有 Postgres 场景（无数据库）和 `KafkaFileRecordHelperTest.test_dodgyFile` 失败，master 上同样失败。

## 如何提交
```
tools/submit_pr.sh contributions/294-zerocode-800 authorjapps/zerocode master issue-800-echo-step-short-form contributions/294-zerocode-800/pr_title.txt contributions/294-zerocode-800/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用，相关 11 个测试通过，红→绿复现且两处改动缺一不可；边界（显式 null、verify-only、validators、retry、占位符 url）均正确；风格、提交信息合规；无竞争 PR。建议：说明"有 url 无 operation 无 assertions 的步骤现在会通过" → 已补；恢复模板未勾选项 → 已恢复 2、5、7。
