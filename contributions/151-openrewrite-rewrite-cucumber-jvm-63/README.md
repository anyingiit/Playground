# openrewrite/rewrite-cucumber-jvm#63：Recipes for Cucumber-JVM 8.0.0（子项：Removed modules）

| 项 | 值 |
|---|---|
| Issue | https://github.com/openrewrite/rewrite-cucumber-jvm/issues/63 |
| Tier | 自由 |
| Labels | good first issue, recipe |
| Status | ✅ ready（补丁和 PR 文案已完成） |
| 重复 PR 检查 | 2026-10-01：open PR 为 0；issue 没有评论，也没有 assignee。#66（Akhil-1527，StrictAware，已合并）只做了 StrictAware 子项。本仓库另有 `907-…-63`（TestNG `scenarios(ITestContext)` 子项），和本补丁不重叠 |
| AI 政策 | 仓库里没有 CONTRIBUTING / AGENTS 文件，也没有 AI 相关规则（`.claude/settings.json` 说明维护者自己在用 Claude Code）。PR 正文已写披露 |
| Base | `main` @ 41933f4 |
| Patch | `0001-Replace-the-modules-removed-in-Cucumber-JVM-8.0.0.patch` |

## 问题理解
#63 是维护者 timtebeek 开的伞形 issue，列出了 Cucumber-JVM 8.0.0 需要的各项迁移 recipe。本补丁只做其中 "Removed modules" 这一项：
- `cucumber-openejb` → `cucumber-jakarta-openejb`
- `cucumber-cdi2` → `cucumber-jakarta-cdi`
- `cucumber-deltaspike` 没有替代模块，issue 原文是 "at most flag it"

## 合理性判断
这是维护者本人列出的子项。#66 已经按"一个子项一个 PR"的方式合并（PR 写的是 "Part of #63"），所以拆成小 PR 可以接受。
在 Maven Central 上核对过：`cucumber-jakarta-cdi` 从 6.1.0 开始发布，`cucumber-jakarta-openejb` 从 7.5.0 开始发布，最新版都是 8.0.3；`cucumber-cdi2`、`cucumber-deltaspike`、`cucumber-openejb` 的最后版本都是 7.34.9。
object factory 的类名是从 jar 里的 `META-INF/services` 读出来的：`io.cucumber.jakarta.cdi.CdiJakartaFactory`、`io.cucumber.jakarta.openejb.OpenEJBObjectFactory`。

## 改动
- `cucumber.yml`：新增声明式 recipe `org.openrewrite.cucumber.jvm.ReplaceRemovedCucumber8Modules`，包含：
  - 两个 `ChangeDependency`，不设置 `newVersion`，版本保持不变，与其它 cucumber 模块对齐；
  - 两个 `properties.ChangePropertyValue`，作用于 `cucumber.object-factory`；
  - 一个 `DependencyInsight`，用来标记 `cucumber-deltaspike`。
- `recipes.csv`：手动加了一行。`recipeCsvGenerate` 会把整份文件的引号都改掉，还会多加一列 dataTables，所以只取新行的前 10 列，按字母顺序插入。
- 新增测试 `ReplaceRemovedCucumber8ModulesTest`，共 4 个用例：pom 替换（DocumentExample）、两个 properties 改值、其它 factory 不受影响、deltaspike 被标记。
- 没有把新 recipe 加进任何 composite，因为 `UpgradeCucumber8x` 还不存在。PR 正文里已说明。

## 验证
本地限制：`settings.gradle.kts` 只从 Code Genome 拉 `org.openrewrite` 构建插件依赖，而这个仓库需要凭据。所以本地临时做了两处改动，它们**不在补丁里**：settings 里换成 `mavenCentral()`；`build.gradle.kts` 加了 buildscript 的 `resolutionStrategy`，把 rewrite-* 解析为 Maven Central 的 latest.release。这个做法和 907 相同。
- 红：先把 cucumber.yml 的改动 stash 掉，再跑 `./gradlew test --tests '*ReplaceRemovedCucumber8ModulesTest'` → 4/4 FAILED（recipe 不存在）。
- 绿：同一条命令 → 4/4 通过。
- `./gradlew check --continue` → `license`、`recipeCsvValidate` 通过；共 135 个测试，6 个失败，全部在 `CucumberJava8ToCucumberJavaTest$StepMigration`。
- 基线：把 src 改动 stash 掉，跑 `./gradlew test --tests '*CucumberJava8ToCucumberJavaTest'` → 同样是 6 个失败。这是本地 rewrite 版本较旧导致的环境问题，907 也遇到了同样的问题。
- 补丁在干净的 `main` 上，以及在先 `git am` 了 907 补丁之后，`git apply --check` 都通过，两份补丁互不冲突。

## 需要提交者注意
- 建议提交前在有 Code Genome 凭据的环境或 CI 上，用最新 rewrite 再跑一次 `./gradlew check`，确认那 6 个失败在 CI 上不出现。
- 仓库不要求 DCO / Signed-off-by。commit 作者用的是 anyingiit 的 noreply 邮箱。
- PR 写的是 "Part of #63"，不是 Closes，因为这是伞形 issue。
- 有一个设计取舍可能被维护者问到：版本保持不变，而没有设成 `newVersion: 8.x`。注意 7.5.0 以前的 `cucumber-openejb` 换名之后，坐标在 Maven Central 上不存在，要等后续的 `UpgradeCucumber8x` 升级版本后才正确。PR 正文里已经说明，并表示愿意改。
- 如果 907（TestNG）也要提交，两个 PR 互相独立，可以并行提交。

## 如何提交
```bash
# 先在 GitHub 上 fork openrewrite/rewrite-cucumber-jvm
git clone https://github.com/anyingiit/rewrite-cucumber-jvm && cd rewrite-cucumber-jvm
git remote add upstream https://github.com/openrewrite/rewrite-cucumber-jvm && git fetch upstream
git checkout -b cucumber-8-removed-modules upstream/main
git am /path/to/0001-Replace-the-modules-removed-in-Cucumber-JVM-8.0.0.patch
git push -u origin cucumber-8-removed-modules
gh pr create --repo openrewrite/rewrite-cucumber-jvm --head anyingiit:cucumber-8-removed-modules \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title / body
见 `pr_title.txt`、`pr_body.md`
