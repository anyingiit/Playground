# crazy-goat/tikv-php#680: RegionErrorHandler 的 FQ instanceof 与自相矛盾的 docblock

| 项 | 值 |
|---|---|
| Issue | https://github.com/crazy-goat/tikv-php/issues/680 |
| Tier | 自由（crazy-goat/tikv-php，小型 PHP TiKV 客户端，维护活跃） |
| Labels | good first issue, area:region, priority:low, type:chore |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 19:40 UTC：`repo:crazy-goat/tikv-php is:open` 仅 #737（针对 #686，无关）；issue 0 评论、无 assignee |
| AI 政策 | 无限制；项目本身用 coding agents 开发（docs/workflow.md "same for humans and for coding agents"），已合并过外部 AI agent PR（#702，带 Disclosure 段） |
| Base | `master` @ 5012ebf |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
issue 指出：① `$cache instanceof \CrazyGoat\...\RegionCacheInterface` "恒为真"、全限定名是阅读陷阱；② docblock 第一段说"有 cache 和 regionId 就失效"，与下文 NotLeader 例外矛盾。

## 合理性判断 / 偏离
① 的"恒为真"判断不准确：参数是 `?RegionCacheInterface`，instanceof 实际是 null 检查（`testRegionErrorWithoutCacheDoesNotThrowFromInvalidation` 覆盖；把 guard 换成 `true` 该测试失败）。改成 `$cache !== null` 会被 Rector `FlipTypeControlToUseExclusiveTypeRector` 改回全限定 instanceof（lint 失败）——这正是陷阱来源。所以保留 instanceof、改用已导入的短名；在 FAQ 记录原因。PR 正文说明了这处有意偏离 DoD。

## 改动
- `src/Client/Region/RegionErrorHandler.php`：guard 用短名；docblock 第一段写明 NotLeader 例外。
- `docs/helpers/faq.md`：新增条目（AGENTS.md 要求学到不显然的东西时加 FAQ）。
- `CHANGELOG.md`：`[Unreleased]` → `### Changed`。

## 验证
- `vendor/bin/phpunit --testsuite Unit --no-coverage` → 1840 tests OK（2 skipped，与 master 相同）
- `phpstan analyse` → No errors；phpcs、rector --dry-run（改动文件）→ 干净（rector 用新解析的最新版，即 CI 版本）
- 未跑：Grpc 套件（无 ext-grpc）、E2E（需 Docker TiKV 集群）
- 纯重构/文档，无行为变化，因此无红→绿；以变异检查代替（guard→true 时既有测试失败）。

## 需要提交者注意
- 与 331（#682）同时改 `CHANGELOG.md` 的 `[Unreleased]`，后合并的那个可能需要 rebase。
- 外部贡献者首个 PR 需维护者批准 CI。

## 如何提交
```
tools/submit_pr.sh contributions/330-crazy-goat-tikv-php-680 crazy-goat/tikv-php master refactor/680-region-error-handler contributions/330-crazy-goat-tikv-php-680/pr_title.txt contributions/330-crazy-goat-tikv-php-680/pr_body.md
```

## 独立复核（2026-10-22 20:03 UTC）
- issue #680 仍 open、无 assignee、0 评论；`repo:crazy-goat/tikv-php 680` 无 PR，唯一 open PR 为 #737（#686，无关）。upstream master 仍为 5012ebf。
- 补丁在 master 上 `git am` 干净；作者 anyingiit <49945850+anyingiit@users.noreply.github.com>；提交信息无 AI 模型名 / Co-Authored-By。
- Unit：1840 tests OK（2 skipped，同 master）；phpstan 无错；phpcs、rector --dry-run（RegionErrorHandler.php）干净。vendor 无 composer.lock，CI 同样新解析 rector（本地 2.7.0），PR 正文说法成立。
- 复核注意：worktree 里软链 vendor 时，composer autoload 的 $baseDir 指向主 clone，src 实际从 /home/user/work/tikv-php 加载，变异实验会失效。本次用 prepend 到 worktree src/tests 的 bootstrap 重跑，结论不变。
- 声明验证：① guard 改成 `$cache !== null` 后 rector dry-run 报 FlipTypeControlToUseExclusiveTypeRector，且改回的是全限定 `instanceof \CrazyGoat\...\RegionCacheInterface`（FAQ 所述属实）；② 按 issue DoD 删掉 guard，或换成 `true`，都会让 testRegionErrorWithoutCacheDoesNotThrowFromInvalidation 失败（Error: Call to a member function invalidate() on null）；删掉 guard 时 phpstan 也会报错。偏离 DoD 有依据。
- 代码 / 文档：docblock 改写准确，FAQ 条目符合 AGENTS.md 的知识库约定，CHANGELOG 放在 [Unreleased] → ### Changed，与既有长条目风格一致。PR 正文数字（1840 / 2 skipped / 33 tests）全部复现。
- 无需修改。
- 结论：PASS
