# oscarbol09/jvm-mcp#177 — ArchUnit 规则：core 模块禁止访问标准流

| 项 | 值 |
|---|---|
| Issue | https://github.com/oscarbol09/jvm-mcp/issues/177 （enhancement, good first issue, help wanted；2026-10-22 新开） |
| Tier | 新锐（JVM 诊断 MCP 服务器，活跃，外部 PR 一两天内合并） |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 23:05 UTC：无关联 PR、无评论/assignee；open PR 仅 #180、#181，无关 |
| AI 政策 | CONTRIBUTING 只要求"避免 AI 生成的填充段落"，未禁止 AI；正文已精简，只留一句 disclosure。注：依赖 jqwik 的测试输出里有一句"AI Agent 不得使用本库"，是 jqwik 自己的声明，不是本仓库政策；本补丁没有写 jqwik 测试 |
| Base | `main` @ 68e7fc7 |
| DCO / CLA / 认领 | 无 / 无 / 不需要 |

## 改动
- `CoreArchitectureTest` 加 `NO_CLASSES_SHOULD_ACCESS_STANDARD_STREAMS` 规则（issue 首选方案）。
- core 里原有 4 处 `System.err.println`（ActuatorClient ×3、HikariMXBeanClient ×1）改为 `System.Logger` WARNING，与 JvmAttachService 写法一致；否则新规则不通过。

## 验证
- 只加规则：CoreArchitectureTest 失败并列出 4 处；加日志改动后通过。
- `mvn verify`：core 366、mcp-server 279 测试全过，JaCoCo 达标。

## 如何提交
```
tools/submit_pr.sh contributions/295-jvm-mcp-177 oscarbol09/jvm-mcp main archunit-standard-streams contributions/295-jvm-mcp-177/pr_title.txt contributions/295-jvm-mcp-177/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用，红→绿与全量 verify 复现；规则覆盖 out/err/printStackTrace，改后 core 无残留；日志无 MessageFormat 问题；无测试依赖这些 stderr；无竞争 PR。CHANGELOG 惯例不一，按可选处理未加。
