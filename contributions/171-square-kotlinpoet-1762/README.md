# square/kotlinpoet#1762 — Chained constructor call is not formatted correctly

| 项 | 值 |
|---|---|
| Issue | https://github.com/square/kotlinpoet/issues/1762 |
| Tier | 自由 |
| Labels | bug, PR welcome |
| Status | ✅ ready — patch + PR 文本已完成（未提交）；独立复审 23:09 UTC 通过（red→green、jvmTest 1009/0 失败、spotlessCheck 均已复跑） |
| Base | `main` @ d438267（2026-09-26，"Update plugin spotless to v8.10.3 (#2394)"） |
| Duplicate-PR check | 2026-10-01 23:01 UTC（独立复审 23:09 UTC 复查结果相同）：`pulls?q=1762` 只有 #2332、#2354，均已 closed 且未合并，关闭原因都是作者没签 CLA（维护者 Egorand 在 #2354 写了 "Please feel free to re-open the PR, but make sure to sign the CLA"）。关键词查询（constructor delegate）也没有 open PR；open PR 列表里唯一相关的 #2391 改的是 `trimTrailingNewLine` 对 %S 的处理，跟本问题无关。issue 没有评论、没有 assignee、没人认领 |

## 问题理解

`FunSpec.constructorBuilder().callThisConstructor(...)` / `callSuperConstructor(...)` 的实参原来是用 `joinToCode(prefix = " : this(", suffix = ")")` 直接内联输出的。只要某个实参本身跨多行（比如 `beginControlFlow` 生成的 lambda），输出就会乱：
- 自动换行后的续行跟 `: this(` 对齐，没有相对缩进；
- lambda 体和 `}` 按外层缩进输出，看上去比调用本身还靠左；
- 实参末尾的 `\n` 会让 `)` 单独占一行。

issue 给了复现代码和实际输出。它对"期望输出"只有文字描述（续行应缩进、lambda 体应再缩进一层），没有给代码块。

## 合理性判断

- 维护者给 issue 打了 `bug` 和 `PR welcome` 标签。#2332 拿到过 Egorand 的认可（"Looks good and the test coverage is pretty solid"），JakeWharton 当时提醒要处理位置参数和嵌套 CodeBlock。两个 PR 都只是因为没签 CLA 才被关掉，说明需求本身被接受。
- 本实现是独立写的，没有参考 #2332/#2354 的 diff（只读了 PR 讨论）。
- AI 政策：仓库里没有 CONTRIBUTING.md、AGENTS.md、CLAUDE.md；`docs/contributing.md` 和 `.github/` 里都没有 AI/LLM 相关条款；labels 页也没有 "human only" 之类的说明。所以没有 AI 禁令。

## 改动

- `kotlinpoet/src/jvmMain/kotlin/com/squareup/kotlinpoet/FunSpec.kt`：新增私有函数 `emitDelegateConstructorCall`。
  - 先对每个实参调用 `trimTrailingNewLine()`（和 PropertySpec initializer 用的是同一个 helper）。
  - 用 `CodeBlock.toString()` 渲染后判断里面有没有 `\n`。因为是先渲染再判断，`%L`、`%1L` 这类位置参数里嵌套的多行 CodeBlock 也能识别出来，对应 JakeWharton 在 #2332 提的点。
  - 没有多行实参时，输出和原来完全一样（已有测试 `constructorDelegation` 不受影响）。
  - 有多行实参时，用 `·:·this(\n⇥` + `,\n` 分隔 + `,\n⇤)` 输出：每个实参单独一行、缩进一级、带 trailing comma，风格和多行参数列表（ParameterSpec.emit）一致。`: this(` 用不可断空格紧跟在签名后面。
- `kotlinpoet/src/jvmTest/.../TypeSpecTest.kt`：新增两个测试。`constructorDelegationWithMultilineArgument` 是 issue 的原始复现；`superConstructorDelegationWithNestedMultilineArgument` 覆盖 super 调用，以及通过 `%1L` 位置参数传入的嵌套多行块。
- `docs/changelog.md`：在 Unreleased 下加了一条 Fix。

已知局限：嵌套 CodeBlock 自身以 `\n` 结尾时（例如 `CodeBlock.of("%L", buildCodeBlock { beginControlFlow…endControlFlow })`），逗号前还会多一个空行。原因是共享的 `trimTrailingNewLine` 不会递归进嵌套块，property initializer 也有同样的问题。这个 helper 本 PR 没动（open PR #2391 正在改它），PR 描述里已经写明。

## 验证

环境：JDK（系统）+ 仓库自带的 Gradle wrapper 9.8.0（jar 已校验，见 AUDIT.md）。

| 命令 | 结果 |
|---|---|
| 只回退 FunSpec.kt、保留新测试：`./gradlew :kotlinpoet:jvmTest --tests 'com.squareup.kotlinpoet.TypeSpecTest.*onstructorDelegation*'` | 3 个测试，**2 个失败**（两个新测试），即 red |
| 加上修复后再跑同一条命令 | 3 个测试，0 个失败，即 green |
| `./gradlew :kotlinpoet:jvmTest :kotlinpoet:spotlessCheck`（CI 跑的是 `./gradlew build` / `:kotlinpoet:check`） | BUILD SUCCESSFUL：jvmTest 1009 tests / 0 failures / 40 skipped；spotless（ktfmt googleStyle + license header）通过 |

没在本地跑的：JS/Wasm 测试（需要下载 Node）、多 JDK toolchain 测试（只在 CI 环境开启）、apiCheck。这次只改了 private 函数，不影响公开 API。

## 如何提交

```bash
git clone https://github.com/square/kotlinpoet && cd kotlinpoet
git checkout -b fix-delegated-constructor-call-formatting origin/main
git am /path/to/0001-Fix-formatting-of-delegated-constructor-calls-with-m.patch
./gradlew :kotlinpoet:jvmTest :kotlinpoet:spotlessCheck
git push <your-fork> fix-delegated-constructor-call-formatting   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

### 需要提交者注意
- **必须先签 Square 的 Individual CLA**（https://spreadsheets.google.com/spreadsheet/viewform?formkey=dDViT2xzUHAwRkI3X3k5Z0lQM091OGc6MQ&ndplr=1），然后在 PR 里勾上 CLA 那一项。前两个 PR 都是因为没签 CLA 被关的。
- 不要删 PR 模板的默认内容（docs/contributing.md 写明缺 checklist 的 PR 会被关）。pr_body.md 已经原样保留了模板里的两项。
- changelog 条目目前写的是 `(#1762)`（issue 号），仓库惯例写 PR 号。开 PR 后请改成实际 PR 号，例如 `git commit --amend`。
- 仓库没有 AI 政策、不要求 DCO、没有 AI trailer 要求。PR 正文已经包含 Claude Code 的披露段落。
- 可能的 review 点：维护者 Egorand 在 #2332 建议过把同样的处理推广到 property initializer 和默认参数值。本 PR 只修 issue 范围内的问题，如果维护者要求可以再跟进。
- 本地 clone（含 commit）：`/home/user/work/square-kotlinpoet`，分支 `fix-delegated-constructor-call-formatting`。
