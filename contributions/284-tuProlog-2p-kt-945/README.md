# tuProlog/2p-kt#945 — Normalize malformed TheoryDeobjectifier input errors

| 项 | 值 |
|---|---|
| Issue | https://github.com/tuProlog/2p-kt/issues/945 |
| Tier | 自由（2p-kt，博洛尼亚大学的 Kotlin 多平台 Prolog，~100★，维护者 gciatto 活跃，今天刚发 3.0.5） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~21:45 UTC：无 assignee、无关联 PR；9 个 open PR 都与 serialize-theory 无关 |
| AI 政策 | AGENTS.md 是写给 AI agent 的；维护者自己的 triage 评论注明由 Claude Code 完成。保留 disclosure 段 |
| Base | `master` @ 4443ffd |
| DCO / CLA / CHANGELOG | 无（semantic-release 根据 Conventional Commit 生成） |
| 需先认领 | 否 |
| 同仓库 | 285（#1005 ceiling）也是这个仓库，可以同时提交 |

## 改动
JVM/JS 两个 `TheoryDeobjectifier` 用 `it as? Clause ?: throw DeobjectificationException(it)` 替换无检查的强转，和 issue 建议一致。commonTest 加了 JSON/YAML 各一个测试，分别用数字、变量、`foo(X)` 三种非子句元素断言 `DeobjectificationException`。

## 验证
- `:serialize-theory:jvmTest`：红（ClassCastException）→ 绿 6/0。
- `ktlintCheck`、`detekt`、`jsMainClasses`、`jsTestClasses` 通过；`jsTest` 因 yarn 下载失败没跑，正文已说明。

## 如何提交
```
tools/submit_pr.sh contributions/284-tuProlog-2p-kt-945 tuProlog/2p-kt master fix/945-theory-deobjectifier-errors contributions/284-tuProlog-2p-kt-945/pr_title.txt contributions/284-tuProlog-2p-kt-945/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- PASS：新克隆干净应用，红→绿复现；不会误拒合法输入（事实是 `{"head":…}`，规则是 `:-`/2）；`Theory.of` 立即消费序列，惰性不影响；JS 端 `as?` 行为一致；Conventional Commit 正确。
- 采纳：正文里的示例消息改为准确的 `Error while deobjectifying 1`，并说明为什么传 Term 而不是原始输入。
- 未改（另一个 bug，不扩大本 PR）：JVM 的 `deobjectifyClause` 要求有 `head`，指令 `{"body":…}` 读不回来，而 JS 能读。可以以后单独提 issue。
