# Kotlin/dataframe #1866 — Inline some type aliases in public API, part 2

| 项 | 值 |
|---|---|
| Issue | https://github.com/Kotlin/dataframe/issues/1866 |
| Tier | 自由 |
| Labels | good first issue（Milestone: Backlog） |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=1866` 0 结果；关键词 "inline type aliases" 只有已合并的 part 1 #1863（Allex-Nik，2026-05-28）。issue 无 assignee、无评论。master 上这些别名仍出现在公开签名中（未修复）。 |
| Base | `master` @ 68c49eb5（2026-10-01） |

## 问题理解
#906 / #1863 已把 `AnyFrame`、`AnyRow`、`AnyBaseCol` 在公开 API 中内联。#1866 是第二部分：把 `AnyCol`、`AnyColumnReference`、`AnyColumnGroupAccessor`、`StringCol`、`ColumnGroupReference` 在**公开 API 签名**中替换为展开后的类型，让 IDE 补全显示真实类型。要求：不改内部使用，不删除别名声明。

## 合理性判断
- issue 由维护者开出，标了 good first issue，part 1 (#1863) 已按相同方式合并，做法明确，不需要设计讨论。
- 仓库对 AI 是友好的：有 AGENTS.md / CLAUDE.md 专门给编码代理看，CONTRIBUTING、.github、labels 里都没有禁止 AI 的规定，也没有 PR 模板。

## 改动
- 用脚本扫描 `core/src/main`、`dataframe-arrow/src/main`（其它模块的公开签名里没有这些别名）中所有 `public` / `override` 声明的签名部分（接收者、参数、返回类型、公开类的构造参数），只在签名范围内替换。函数体、KDoc、`impl/`、`internal`/`private` 声明都不改；`KotlinNotebookPluginUtils` 里 private 类的 override 已手动还原。
- 展开方式：`AnyCol` → `DataColumn<*>`；`AnyColumnReference` → `ColumnReference<*>`；`AnyColumnGroupAccessor` → `ColumnAccessor<DataRow<*>>`（`ColumnGroupAccessor` 本身也是别名，所以一直展开到底）；`StringCol` → `DataColumn<String?>`；`ColumnGroupReference` → `ColumnReference<DataRow<*>>`（与 part 1 把 `AnyRow` 写成 `DataRow<*>` 一致）。
- 补了需要的 import，删掉不再使用的别名 import，再用 `runKtlintFormatOverMainSourceSet` 统一格式（有几个超过 120 列的签名被自动换行）。
- 合计 45 个文件（core 44 个，arrow 1 个），约 200 处。`aliases.kt` 和 `generated-sources` 不动（后者由 CI bot 重新生成）。

## 验证（JDK 21，Gradle 9.8.0 wrapper）
这是纯重构，没有行为变化，所以 red→green 不适用。下面用编译、API 检查和现有测试来验证。
- `./gradlew --max-workers=2 -Pkotlin.dataframe.debug=true :core:compileTestKotlin :dataframe-arrow:compileTestKotlin :core:apiCheck :dataframe-arrow:apiCheck :core:runKtlintCheckOverMainSourceSet :dataframe-arrow:runKtlintCheckOverMainSourceSet`：BUILD SUCCESSFUL。`.api` 文件没有变化，因为别名在编译期展开，二进制兼容。
- `./gradlew --max-workers=2 -Pkotlin.dataframe.debug=true :core:test :dataframe-arrow:test`：BUILD SUCCESSFUL — core: 1861 tests, 0 failures, 17 skipped; dataframe-arrow: 68 tests, 0 failures, 1 skipped
- 本地环境说明：Maven Central 对本机 IP 返回 429，所以我在 `GRADLE_USER_HOME/init.d/mirror.gradle` 里加了 Google 的 Maven Central 镜像。这个改动只在本地生效，不在 patch 里。
- 独立复核（2026-10-01 19:36 UTC，全新 shallow clone @ 68c49eb）：`git am` 干净应用；脚本比对确认每个改动文件中删除行在把 5 个别名替换为展开类型后与新增行逐字一致（只差 import 和 ktlint 换行），没有任何行为改动；上面的编译/apiCheck/ktlint 命令 BUILD SUCCESSFUL，`git status` 干净（`.api` 未变）；`:core:test :dataframe-arrow:test` core 1861/0 失败/17 跳过，arrow 68/0/1。改动后 core 与 arrow 的 `src/main` 中这些别名只剩在 `internal`/`private` 声明、函数体和 KDoc 里。
- **没有运行**：完整的 `./gradlew build`（包含所有模块、samples 和 KDoc 预处理），因为机器资源有限。

## 需要提交者注意
- 仓库不需要 DCO，也没有 AI trailer 的要求。PR 正文里已经写了 disclosure 段落。
- 提交前最好本地跑一次 `./gradlew build -Pkotlin.dataframe.debug=true`（CONTRIBUTING 的要求）。
- 这类改动容易和 master 上的新提交冲突。如果 `git am` 失败，需要在新 master 上重新做替换（原替换脚本是临时文件，已随工作目录清理；可参照 patch 的 diff 手工或脚本重做，做完再执行 `runKtlintFormatOverMainSourceSet`）。
- 范围比 part 1 稍大：part 1 只改了 core 的 api 包。这次还改了 `DataColumn.kt`、`ColumnsContainer.kt` 等 core 根包文件，以及 `dataframe-arrow`。如果维护者只想改 api 包，可以按需删掉对应 hunk。

## 如何提交
```bash
git clone https://github.com/Kotlin/dataframe && cd dataframe
git checkout -b inline-type-aliases-part-2 origin/master
git am /home/user/Playground/contributions/099-Kotlin-dataframe-1866/0001-Inline-AnyCol-AnyColumnReference-AnyColumnGroupAcces.patch
./gradlew build -Pkotlin.dataframe.debug=true
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/099-Kotlin-dataframe-1866 Kotlin/dataframe master inline-type-aliases-part-2 contributions/099-Kotlin-dataframe-1866/pr_title.txt contributions/099-Kotlin-dataframe-1866/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
