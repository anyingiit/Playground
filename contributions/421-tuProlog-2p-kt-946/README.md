# 421 — tuProlog/2p-kt#946: withTheories() 保留接收者的 unificator

| 项 | 内容 |
|---|---|
| Issue | https://github.com/tuProlog/2p-kt/issues/946 |
| 层级 | 自由（博洛尼亚大学 tuProlog 的 Kotlin 多平台 Prolog，持续发版（10 月已发 3.0.4、3.0.5）） |
| Labels | bug, confirmed, module::dsl-theory（维护者 gciatto 本人开的，10-04 确认并给出一行修复方案） |
| Base 分支 | `master`（补丁基于 4443ffd） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：无评论认领、无指派、无关联 PR；8 个开着的 PR 均与 withTheories/unificator 无关 |
| AI 政策 | 仓库有 AGENTS.md（给 agent 的构建说明），维护者自己的 triage 也写着用 Claude Code，无限制 |
| CLA/DCO | 无 |

## 问题理解
`UnifyLogicProgrammingScope.withTheories()` 的 `unificator` 默认值是全局默认 unificator，而不是接收者自己的，导致 `lp(custom) { withTheories() }` 静默换回默认严格 unificator。issue 里给了修复：默认改成 `this.unificator` 并更新 KDoc、在 `:dsl-theory` 加测试。

## 改动
- `DSL.kt`：默认值 `this.unificator`，KDoc 改写。`theoryFactory` 默认 `IndexedTheoryFactory(unificator)` 自然跟着变。
- 新增 `TestWithTheories.kt`（commonTest，3 个测试）。

## 验证
- 红：不带修复 `:dsl-theory:jvmTest --tests '*TestWithTheories*'` 3 个测试中 2 个失败（显式传参的那个本来就过）。
- 绿：`:dsl-theory:jvmTest :dsl-theory:ktlintCheck :dsl-theory:detektAll --continue` BUILD SUCCESSFUL；dsl-theory JVM 测试 7/7 通过。
- 未跑 jsTest（需下载 Node/Kotlin JS 工具链）；改动是 commonMain 纯 Kotlin，平台无关。
- 环境：Maven Central 经代理返回 429，用本地 init 脚本把 Central 指向 Google 镜像（不在仓库内）。

## 需要提交者注意
- 提交信息为 Conventional Commits（仓库 commit-msg 钩子校验，已手动验证通过）；CHANGELOG 由 semantic-release 生成，不手改。
- `fix` 会触发补丁版本发布；行为变化在 PR 正文已说明（issue 作者自己也提到）。

## 如何提交
```
git clone https://github.com/tuProlog/2p-kt && cd 2p-kt && git checkout -b fix-with-theories-unificator origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 全新 `git clone --depth 20`（origin/master = 4443ffd，与补丁基点一致），`git am` 干净应用。
- 代码：`UnifyLogicProgrammingScope.withTheories(unificator = this.unificator, theoryFactory = IndexedTheoryFactory(unificator))`。Kotlin 扩展函数的默认参数在调用时求值，`this` 指接收者，`unificator` 是 `UnificationAware` 的属性（`LogicProgrammingScopeImpl` 的 `override val unificator`），后面的 `theoryFactory` 默认值引用的是前一个参数，所以工厂也跟着用接收者的 unificator。KDoc 改写准确；`CoreLogicProgrammingScope` 重载不变是对的（它没有 unificator）。
- 测试：`Unificator.naive()` 每次调用都返回新的匿名对象，默认值是 `Unificator.default`（lazy strict），所以 `assertSame` 能区分开；3 个测试有意义。
- 其他引用：全仓库（含 `documentation/` 站点源、其他模块）只有 `dsl-theory` 的 `DSL.kt`、`LogicProgrammingScope.kt` 提到 `withTheories`，后者只是链接，没有描述默认值；没有别的代码依赖旧默认值。
- 构建（Google 镜像 init 脚本，`--no-scan`）：
  - 红：只把 DSL.kt 回退到 HEAD~1，`:dsl-theory:jvmTest --tests '*TestWithTheories*'` 3 个测试中 2 个失败（Preserves…、BuildsTheories…），BUILD FAILED。
  - 绿：`:dsl-theory:jvmTest :dsl-theory:ktlintCheck :dsl-theory:detektAll --continue` BUILD SUCCESSFUL；测试结果 XML 2+2+3=7 个，0 失败；ktlintCommonMain/CommonTest 检查跑过。
  - 注：本仓库 dsl-theory 的 detekt 子任务全部是 NO-SOURCE（只配置了 jvm/js 源集，没有 commonMain），所以 `detektAll` 实际没检查什么；这和上游配置一致，不影响结论，PR 正文里的说法也没错。
- 竞争 PR：/pulls 共 8 个开着的 PR，没有一个和 withTheories/unificator/dsl-theory 有关；`?q=946` 只搜到 3 个无关的 renovate 旧 PR。issue 仍只有 gciatto 10-04 一条确认评论，没有指派，没有关联分支或 PR。
- pr_body.md：前两行是归属块；全英文；内容与补丁和 issue 一致；有 Motivation / disclosure 段；结尾有 Claude Code 署名。pr_title 与提交标题一致，符合 Conventional Commits。没有需要修改的地方。
- 已删除临时克隆 /home/user/work/review421。

结论：PASS
