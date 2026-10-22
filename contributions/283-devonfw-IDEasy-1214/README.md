# devonfw/IDEasy#1214 — preserve EOL style in upgrade-settings

| 项 | 值 |
|---|---|
| Issue | https://github.com/devonfw/IDEasy/issues/1214 |
| Tier | 新锐（IDEasy，devonfw 组织，活跃，~100★） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~21:20 UTC：无 assignee、无关联 PR；quando632 今天加了 good first issue 并把范围缩到 `updateRepositoryPropertiesFile`，本补丁正好按这个范围 |
| AI 政策 | AGENTS.md 欢迎 AI，但**严禁任何 AI 署名**（提交、PR 标题/正文、评论都不能有 "generated with"、Co-authored-by 等）。所以正文**没有** disclosure 段，提交时不要补，也不要加 `Assisted-by` |
| Base | `main` @ 616cffc |
| CLA | **需要**：首个 PR 时 cla-assistant 机器人会贴链接（SAP 的 CLA-assistant，GitHub 登录确认；文档提醒邮箱要和提交邮箱一致，字段未能免登录核实，预计姓名+邮箱）。若要求大量个人信息就放弃 |
| DCO / CHANGELOG | 无 DCO；CHANGELOG 已加在未发布的 2026.10.001 段末尾 |
| 需先认领 | 建议：PR 模板要求 issue 已分配/In Progress。可先在 issue 留言："I'd like to pick this up, following the narrowed scope from the last comment."（非强制） |

## 改动
`UpgradeSettingsCommandlet.updateRepositoryPropertiesFile` 改为 `readString` 读入、检测 CRLF/LF，用原换行符写回，保留"有无末尾换行"。新测试在运行时生成 CRLF 与 LF 两个旧版仓库 properties（因为 `.gitattributes` 会把提交的文件统一成 LF），精确比较升级后的内容。

## 验证
- JDK 25（pom 要求）：从 Adoptium 下载 Temurin 25.0.5。
- `mvn -Dtest=UpgradeSettingsCommandletTest test`：红（CRLF 被写成 LF）→ 绿 2/0。
- cli 全量 `mvn test`：1145 个，只有 4 个失败（NetworkProxyTest 3 + GlobalToolCommandletTest 1），已在 main 上复现，是本机代理环境导致。
- `spotless:check checkstyle:check` 通过。

## 如何提交
```
tools/submit_pr.sh contributions/283-devonfw-IDEasy-1214 devonfw/IDEasy main fix/1214-preserve-eol contributions/283-devonfw-IDEasy-1214/pr_title.txt contributions/283-devonfw-IDEasy-1214/pr_body.md
```
（不要加 `--trailer Assisted-by`。）

## 独立复核（2026-10-22，独立 agent）
- PASS：新克隆干净应用；红→绿、spotless/checkstyle 复现；`String.lines()` 与旧 `readAllLines` 行为一致（含空文件）；UTF-8 不变；测试在 Windows CI 也成立（运行时生成文件，不受 autocrlf 影响）；CHANGELOG 段未发布；无 AI 署名。
- 采纳：末尾只有 `\r` 的文件也保留结尾换行；正文写明"不再强制补末尾换行"；补回模板里的工具/GUI 两段清单（不勾选）；如实说明本地 4 个环境性失败。
- 未改（超出缩小后的范围）：`EnvironmentVariablesPropertiesFile.save()` 和各 merger 也不保留换行风格。
