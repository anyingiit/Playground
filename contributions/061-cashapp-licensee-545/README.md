# cashapp/licensee#545 — Artifact coordinates not printed out when build is ran in quiet mode

| 项 | 值 |
|---|---|
| Issue | https://github.com/cashapp/licensee/issues/545 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — patch + 测试 red→green + check 通过 (2026-10-01) |
| 重复 PR 检查 | 2026-10-01 `github.com/cashapp/licensee/pulls?q=545` 0 结果；issue 无 assignee、无评论 |
| Base | `trunk` @ 117a759 |

## 问题理解
`gw -q app:licensee` 时只输出 ` - ERROR: ...`，看不出属于哪个 artifact。作者（维护者 Egorand）期望 quiet 模式要么输出完整信息、要么什么都不输出。

## 合理性判断
Issue 由维护团队成员提出，代码中确实把坐标头固定用 `LIFECYCLE` 级别打印（`-q` 会屏蔽），而错误/警告用 `ERROR`/`WARN`（`-q` 仍显示）。合理且范围小。仓库无 CONTRIBUTING/AGENTS/AI 政策，无 DCO 要求，无 PR 模板。

## 改动
- `src/main/kotlin/app/cash/licensee/task.kt`：坐标头日志级别改为其结果中最严重的级别（有 Error → violationErrorLevel，有 Warning → violationWarningLevel，否则 INFO）。IGNORE 时这些级别都是 INFO，行为不变；非 quiet 模式下 WARN/ERROR 与 LIFECYCLE 显示效果一致。
- 新 fixture `src/test/fixtures/spdx-not-allowed-log-quiet/`（复制 `spdx-not-allowed-log`；`allFixturesCovered` 要求每个 fixture 只被一个测试使用，故需单独目录），含 22 字节空 zip jar（与其他 fixture 一致，`checkFixtureJars` 校验）。
- `LicenseePluginFixtureTest.violationsLoggedQuiet`：以 `--quiet` 运行并断言坐标行出现在错误行之上。
- `CHANGELOG.md` Unreleased → Fixed 加一条。

## 验证（`GRADLE_USER_HOME` 指向工作目录；Maven Central 偶发 429，重试即可）
- Red（未改 task.kt）：`./gradlew test --tests '*.violationsLoggedQuiet*' --tests '*.allFixturesCovered*'` → 4 tests, 2 failed；输出只有 ` - ERROR: SPDX identifier 'Apache-2.0' is NOT allowed`，与 issue 现象一致。
- Green：`./gradlew spotlessCheck test --tests '*.LicenseePluginFixtureTest.violations*' --tests '*.LicenseePluginFixtureTest.unused*' --tests '*.LicenseePluginFixtureTest.failure*' --tests '*.LicenseePluginFixtureTest.allFixturesCovered*' --tests '*.SpdxLicensesTest'` → 43 tests, 0 failures（latest 与 9.0 两个 Gradle 版本）。
- `./gradlew check -x test`（lint、spotlessCheck、checkKotlinAbi/checkLegacyAbi、checkFixtureJars）→ 通过。
- 未运行：完整 `success` 系列 fixture（大量 Android/KMP fixture，资源受限）；改动只影响有 Error/Warning 结果时坐标头的日志级别，不影响 success fixture 的产物。

## 需要提交者注意
- 补丁包含一个二进制 fixture jar（22 字节空 zip），用 `git am` 应用（format-patch 已含 binary patch），不要用 `patch`。
- 仓库不要求 DCO、不要求 AI trailer；PR 描述已含披露段落。
- commit 作者：anyingiit <49945850+anyingiit@users.noreply.github.com>。

## 如何提交
```bash
git clone https://github.com/cashapp/licensee && cd licensee
git checkout -b quiet-mode-coordinates origin/trunk
git am /path/to/contributions/061-cashapp-licensee-545/0001-*.patch
git push <fork> quiet-mode-coordinates
# 或在 Playground 中：
tools/submit_pr.sh contributions/061-cashapp-licensee-545 cashapp/licensee trunk quiet-mode-coordinates contributions/061-cashapp-licensee-545/pr_title.txt contributions/061-cashapp-licensee-545/pr_body.md
```

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。
