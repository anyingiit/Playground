# crazy-goat/tikv-php#682: 删掉 fail-closed 契约的探测死分支

| 项 | 值 |
|---|---|
| Issue | https://github.com/crazy-goat/tikv-php/issues/682 |
| Tier | 自由（crazy-goat/tikv-php） |
| Labels | good first issue, priority:low, type:chore |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 19:40 UTC：open PR 仅 #737（#686，无关）；issue 0 评论、无 assignee |
| AI 政策 | 无限制（见 330） |
| Base | `master` @ 5012ebf |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
两个测试先探测 `batchResolveRegions(['z'])` 是否抛异常，不抛就 `expectNotToPerformAssertions()` + 警告后提前返回。#244 已合并，分支是死的；而且契约一旦回归，测试会静默通过。

## 改动
- 两个文件各加 `testResolverFailsClosedForAKeyOutsideTheReturnedRegions()`（expectException(TiKvException)）。
- 删除 `requireFailClosedContract()` 及两处调用、commit 测试里的 inline 探测；更新类 docblock；CHANGELOG `[Unreleased]` → `### Tests`。

## 验证
- 全量 `phpunit --testsuite Unit` → 1842 OK（2 skipped 同 master）；phpstan 无错；phpcs / rector 干净。
- 红→绿（变异法）：把 `RegionResolver` 的 fail-closed throw 关掉 → master 两个文件都以 exit 0 结束（仅 "OK, but there were issues!" + 1 个 E_USER_WARNING，CI 不带 --fail-on-warning；问题所在）；本补丁各 1 个失败。恢复后全绿。
- 未跑：Grpc 套件、E2E。

## 需要提交者注意
- 与 330（#680）都改 `CHANGELOG.md` `[Unreleased]`，后合并的可能需要 rebase。

## 如何提交
```
tools/submit_pr.sh contributions/331-crazy-goat-tikv-php-682 crazy-goat/tikv-php master test/682-fail-closed-probes contributions/331-crazy-goat-tikv-php-682/pr_title.txt contributions/331-crazy-goat-tikv-php-682/pr_body.md
```

## 独立复核（2026-10-22 20:03 UTC）
- issue #682 仍 open、无 assignee、0 评论；`repo:crazy-goat/tikv-php 682` 无 PR，无竞争 PR。
- 补丁在 master 上 `git am` 干净；作者正确；提交信息无 AI 模型名。
- Unit：1842 tests OK（2 skipped，同 master）；phpstan 无错；两个测试文件的 phpcs、rector dry-run 干净；文件中已无 probe / "not merged" 残留。
- 变异复核：用 worktree 本地 autoload 重跑（软链 vendor 会从主 clone 加载 src，导致变异不生效）。在 RegionResolver::batchResolveRegions 的 fail-closed throw 前插 `continue` 后，master 两个文件都 exit 0，但输出是 "OK, but there were issues!" + 1 个 warning（RawKv：2 tests / 0 assertions；Txn：2 tests / 5 assertions）；本补丁每个文件 1 个失败（testResolverFailsClosedForAKeyOutsideTheReturnedRegions）。未变异时两个文件各为 OK (3 tests, 7 assertions)。
- 已修正：pr_body.md 原写 master 变异后是 `OK (2 tests, 5 assertions)` / `OK (2 tests, 6 assertions)`，这其实是未变异 master 的数字（原作者的变异很可能因软链 autoload 未生效）。已改为实测结果，并注明 CI 不带 --fail-on-warning，所以回归确实会被放过。README 验证段的措辞同步更新。补丁本身未改。
- 与 330 都改 CHANGELOG [Unreleased]，后合并的需要 rebase（已知）。
- 结论：PASS（PR 正文数字已修正）
