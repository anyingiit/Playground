# 433 — tuProlog/2p-kt#1005: ceiling/1 用大整数计算，不再在 Long.MAX_VALUE 饱和

| 项 | 内容 |
|---|---|
| Issue | https://github.com/tuProlog/2p-kt/issues/1005 |
| 层级 | 自由（博洛尼亚大学 tuProlog，Kotlin 多平台 Prolog，持续发版） |
| Labels | bug, confirmed, good first issue, module::solve（维护者 gciatto 10-04 开并确认，给出修复方案：照 Floor.kt 用 setScale(0, CEILING).toBigInteger()，并在 test-solve 加回归测试） |
| Base 分支 | `master`（补丁基于 4443ffd） |
| 状态 | ✅ 可提交（复核 PASS） |
| 重复检查 | 2026-10-22：issue 无评论认领、无指派、无关联分支/PR；`is:pr ceiling` 0 结果 |
| AI 政策 | 无限制（AGENTS.md 是构建说明；维护者 triage 本身用 Claude Code） |
| CLA/DCO | 无 |
| 同仓库 | 第 2 个（另一个是 421 #946），可一起提交 |

## 改动
- `Ceiling.kt`：Real 分支改为 `Numeric.of(real.value.setScale(0, RoundingMode.CEILING).toBigInteger())`，去掉 `kotlin.math.ceil` import。Integer 分支不变。
- `TestIs` / `TestIsImpl`：新增 `testIsCeilingOfLargeReal`（`ceiling(1.0e30)` → 10^30；`ceiling(-12345678901234567890.5)` → -12345678901234567890，验证超出 Long 范围后仍向上取整）。
- `TestPrologIs`、`TestProblogIs` 接上新测试（这两个是 TestIs 的全部实现者）。

## 验证
- 红：只回退 Ceiling.kt，`:solve-prolog:jvmTest --tests '*TestPrologIs*'` 7 个中 1 个失败，实际值 `9223372036854775807`，和 issue 描述一致。
- 绿：`:solve-prolog:jvmTest :solve-problog:jvmTest :solve:jvmTest` + 四个模块 `ktlintCheck` + `:solve:detektAll :test-solve:detektAll`，BUILD SUCCESSFUL；solve-prolog 441、solve-problog 412（54 skipped）、solve 20，0 失败。
- 注意：测试输入用 `realOf("1.0e30")`（字符串解析，与 Prolog 解析器一致）；用 `realOf(1.0e30)`（Double）会得到二进制精确值 1000000000000000019884624838656。
- 未跑 jsTest。

## 如何提交
```
git clone https://github.com/tuProlog/2p-kt && cd 2p-kt && git checkout -b fix-ceiling-big-integer origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 用全新 clone 检查，origin/master 仍为 4443ffd，`git am` 干净应用（5 个文件，+43/-2）。
- 修法与维护者 gciatto 的建议一致。
- 已核对的取值：负小数 -2.9→-2、-0.5→0，实数形式的整数 2.0→2，超出 Long 范围时不饱和。写法与 Floor/Round/Truncate 一致。
- TestIs 只有 TestPrologIs、TestProblogIs 两个实现者，补丁都已接上。
- 绿：指定的 9 个任务 BUILD SUCCESSFUL。solve-prolog 441、solve-problog 412（54 skipped）、solve 20，全部 0 失败。ktlint/detekt 通过。
- 红：只回退 Ceiling.kt 后，testIsCeilingOfLargeReal 失败，实际值 9223372036854775807。
- PR 标题、正文、作者和提交信息均符合要求。
- 无竞争 PR，issue 无人认领。同作者另有开放的 PR #1044（即 421）。
- 小瑕疵："with and empty theory" 笔误照抄自既有 KDoc，不改。

结论：PASS
