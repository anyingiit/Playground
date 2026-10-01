# openrewrite/rewrite-cucumber-jvm#63：Recipes for Cucumber-JVM 8.0.0（子项：TestNG `scenarios(ITestContext)`）

| 项 | 值 |
|---|---|
| Issue | https://github.com/openrewrite/rewrite-cucumber-jvm/issues/63 |
| Tier | 自由 |
| Labels | good first issue, recipe |
| Status | ✅ ready（补丁 + PR 文案已完成） |
| 重复 PR 检查 | 2026-10-01 查过：open PR 为 0。#66（Akhil-1527，DropStrictAware，已合并）只做了 StrictAware 子项，也写明 "Part of #63"。issue 无评论、无 assignee，没有人认领 TestNG 子项 |
| AI 政策 | 仓库没有 CONTRIBUTING / AGENTS 文件，也找不到 AI 相关规则（`.claude/settings.json` 说明维护者自己就在用 Claude Code）。PR 正文里已写披露 |
| Base | `main` @ 41933f4 |

## 问题理解
#63 是 maintainer（timtebeek）开的 Cucumber-JVM 8.0.0 迁移伞形 issue，列了多项 recipe。这次只做其中界限清楚的一项：
8.0.0 把 `AbstractTestNGCucumberTests` 的 `@DataProvider` 从 `scenarios()` 改成了 `scenarios(ITestContext)`（已对照 cucumber-jvm main 源码确认）。
用户 runner 里常见的 `@Override @DataProvider(parallel = true) public Object[][] scenarios() { return super.scenarios(); }` 在 8.x 下不再是 override，所以需要加上参数，再传给 super。

## 合理性判断
这一项在 issue 正文 "Needed, by priority" 列表里，是 maintainer 本人提出的；#66 已经按"一个子项一个 PR"的方式被合并，维护者回复 "Good to see support for 8.0.0 brought closer"。所以拆小 PR 的做法可以接受。

## 改动
- 新增 `src/main/java/org/openrewrite/cucumber/jvm/AddTestContextToScenarios.java`：
  - 前置条件 `DeclaresMethod` 或 `UsesMethod`（复审时补上 `DeclaresMethod`：原来只有 `UsesMethod`，不调用 `super.scenarios()` 的 override 会被漏掉）；用 `MethodMatcher(... scenarios(), matchOverrides=true)` 匹配 override 声明，经中间基类继承的也算；
  - 用 JavaTemplate 生成 `ITestContext context` 参数（类型来自 `dependsOn` stub）。方法体里已有 `context` 变量时改名为 `testContext`；
  - 把方法体内的 `super.scenarios()` 改成 `super.scenarios(context)`，并同步更新 method type。
- 新增测试 `AddTestContextToScenariosTest`，共 6 个用例：DocumentExample、中间基类、变量名冲突、不调用 super 的 override、无关 `scenarios()`、未 override 的 runner。
- `build.gradle.kts`：加 `testParserClasspath("org.testng:testng:7.+")`；重新生成 `src/test/resources/META-INF/rewrite/classpath.tsv.gz`（二进制）。
- `recipes.csv`：新增一行。这一行由 `recipeCsvGenerate` 生成；生成时另外两行的引号格式也变了，那两行已手动还原，不带进补丁。
- 没有加进任何 composite：`UpgradeCucumber8x` 还不存在，放进 7x 又不对。PR 里已说明。

## 验证
本地有个限制：`settings.gradle.kts` 只从 Code Genome（需要凭据）拿 `org.openrewrite` 构建插件依赖，所以本地临时做了两处改动，都**不在补丁里**：
1. settings 去掉 codegenome 仓库，换成 `mavenCentral()`；
2. build.gradle.kts 顶部临时加 `buildscript { configurations.classpath { resolutionStrategy.eachDependency { org.openrewrite:rewrite-* -> latest.release } } }`。

这样拿到的是 Maven Central 上的 rewrite 8.90.4。命令和结果：
- `./gradlew createTestTypeTable` → 生成的测试 type table 带 `org.testng:testng:7.12.0`
- 红（recipe 改成 no-op）：`./gradlew test --tests '*AddTestContextToScenariosTest'` → 6 个用例中 4 个失败，"Recipe was expected to make a change but made no changes"
- 绿：同一命令 → 6/6 通过（RewriteTest 默认开启类型校验）
- `./gradlew check` → 137 个测试，6 个失败，全部是 `CucumberJava8ToCucumberJavaTest$StepMigration`；`license`、`recipeCsvValidate` 通过
- 在基线上（stash 掉本改动）跑 `./gradlew test --tests '*CucumberJava8ToCucumberJavaTest'` → 同样是这 6 个失败。这是旧 rewrite 版本的环境问题，和本改动无关
- 在干净的 `main` 上 `git apply --check` 补丁 → OK

## 复审（独立）
- 2026-10-01 复审：open PR 仍为 0；补丁在新 clone 上 `git am` 成功；红/绿复现（no-op 时 4/6 失败，修复后 6/6 通过）。
- 发现并修复：仅 `UsesMethod` 前置条件会漏掉不调用 `super.scenarios()` 的 override，改为 `Preconditions.or(DeclaresMethod, UsesMethod)` 并加用例 `overrideWithoutSuperCall`，补丁已重新导出。

## 需要提交者注意
- 补丁含二进制文件（test `classpath.tsv.gz`），用 `git am` 应用即可（导出时用了 `--binary`）。也可以应用后自己跑一次 `./gradlew createTestTypeTable` 重新生成。
- 如果你有 Code Genome 凭据或 CI，建议用最新 rewrite 再跑一次 `./gradlew check`，确认那 6 个失败在 CI 上不会出现。
- 仓库不要求 DCO / Signed-off-by，无需 sign-off。commit 作者是 anyingiit noreply 邮箱。
- PR 正文里写的是 "Part of #63"，不是 "Closes"，因为 issue 是伞形的，不能被这个 PR 关闭。
- 如果维护者希望顺手建 `UpgradeCucumber8x`，或改用 `parserClasspath` 的 TestNG type table，可以在后续评论里跟进。

## 如何提交
```bash
git clone https://github.com/anyingiit/rewrite-cucumber-jvm && cd rewrite-cucumber-jvm   # 先在 GitHub 上 fork
git remote add upstream https://github.com/openrewrite/rewrite-cucumber-jvm && git fetch upstream
git checkout -b cucumber-8-testng-scenarios-context upstream/main
git am /path/to/0001-Pass-ITestContext-to-AbstractTestNGCucumberTests.sce.patch
git push -u origin cucumber-8-testng-scenarios-context
gh pr create --repo openrewrite/rewrite-cucumber-jvm --head anyingiit:cucumber-8-testng-scenarios-context \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`

## PR body
见 `pr_body.md`
