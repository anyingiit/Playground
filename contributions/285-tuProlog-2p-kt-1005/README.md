# tuProlog/2p-kt#1005 — `ceiling/1` saturates at Long.MAX_VALUE for large floats

| 项 | 值 |
|---|---|
| Issue | https://github.com/tuProlog/2p-kt/issues/1005 （confirmed, good first issue） |
| Tier | 自由（同 284） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~22:00 UTC：无 assignee、无关联 PR；9 个 open PR 都不涉及 ceiling |
| AI 政策 | 同 284（维护者自己用 Claude Code 做 triage）；保留 disclosure 段 |
| Base | `master` @ 4443ffd |
| DCO / CLA / CHANGELOG | 无（semantic-release 自动生成 CHANGELOG） |
| 需先认领 | 否 |
| 注意 | 这是本仓库第 3 个我们的 PR（#1044、284）。外部 PR 10/5 起仍未审，合并慢，**优先级最低**，可以隔天或等 #1044 有动静再提交 |

## 改动
`Ceiling.mathFunction(real)` 改为 `Numeric.of(real.value.setScale(0, RoundingMode.CEILING).toBigInteger())`，和 Floor/Round/Truncate 一致，也是 issue 里建议的写法。test-solve 的 `TestIs` 新增 `testIsCeilingOfLargeReal`（±1e30、2.1、-0.5），并接入 `TestPrologIs`、`TestProblogIs`。

## 验证
- 红：`X_1=9223372036854775807` → 绿：两套 solver 都通过。
- ktlintCheck（solve、test-solve、solve-prolog、solve-problog）、detekt（solve、test-solve）通过；jsTest 因 yarn 下载失败没跑，正文已说明。

## 如何提交
```
tools/submit_pr.sh contributions/285-tuProlog-2p-kt-1005 tuProlog/2p-kt master fix/1005-ceiling-bigint contributions/285-tuProlog-2p-kt-1005/pr_title.txt contributions/285-tuProlog-2p-kt-1005/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- PASS：新克隆干净应用，红→绿复现；`TestIs` 只有两个实现者且都已更新；依赖模块（solve-concurrent、oop-lib、io-lib 等）的 jvmTestClasses 和 JS 编译都通过。14 个边界值（负数、小数、±0、1e-300、最大 double）和 java.math.BigDecimal 结果一致。
- 采纳：加入 `ceiling(2.1)=3`、`ceiling(-0.5)=0` 两个小值用例。
- 未改：KDoc 里沿用的 "with and empty theory" 笔误，和现有 7 处保持一致。
