# infection/infection#2582 — colored diffs in GitHub Action logs

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/infection/infection/issues/2582 |
| Tier | 自由 |
| Labels | Component / Reporter, Enhancement, Feature, Help Wanted, Integration / GitHub |
| Status | ✅ ready — patch + PR text written |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论、无关联 PR；PR 搜索 `2582` 0 结果；复核 2026-10-01：open PR 列表与 `GitHubActionsLog`/`color diff` 搜索均无相关 open PR。#2292（staabm，"colored diffs in GitHub Actions *annotations*"）已关闭——annotations 不支持 ANSI，与本 issue（*日志*里的 diff）不同 |
| Base | `master` @ 8fc651d |

## 问题理解

PR #2552 新增了 `GitHubActionsLogTextFileReporter`：在 GitHub Actions 上 `--logger-text=php://stdout` 时用 `::group::` 折叠各段。
review 时 theofidry 提议 diff 也加颜色，staabm 指出 GitHub Actions 日志支持 ANSI 颜色并开了本 issue。

## 合理性判断

维护者（staabm）自己开的 issue，标 Help Wanted / Feature；只影响 GitHub Actions 的 stdout 日志，写文件的 text log 不变，无 BC 风险。
仓库有 `AGENTS.md`（专门给 AI agent 的贡献指南），无禁止 AI 贡献条款。

## 改动

- `BaseTextFileReporter`：新增 `protected formatDiff()` 钩子，默认原样返回（`TextFileReporter` 输出不变）。
- `GitHubActionsLogTextFileReporter`：覆写 `formatDiff()`，`@@` 青色、`-` 红色、`+` 绿色；第一个 `@@` 之前的 `--- Original`/`+++ New` 头不着色。
- 测试：更新原有期望（nowdoc→heredoc 以写 `\e`），新增 `test_it_colors_the_mutant_diffs`（头部/上下文行/看起来像头部的改动行）。

## 验证（PHP 8.3.6，本机）

依赖安装：GitHub API 被代理拦截，用 `composer install --prefer-source`；`phpstan/phpstan` 只有 dist，临时把 lock 里的 URL 换成本地 git archive 的 zip（装完已 `git checkout composer.lock`，补丁不含 lock 变更）。

| 命令 | 结果 |
|---|---|
| `vendor/bin/phpunit tests/phpunit/Reporter/GitHubActionsLogTextFileReporterTest.php`（还原 src，仅新测试） | 🔴 2 failures（新测试 + 带 mutation 的用例） |
| 同上（含修复） | 🟢 OK (7 tests, 7 assertions) |
| `make cs` | Fixed 0 of 1492 files；无尾随空格 |
| `make phpstan` | [OK] No errors |
| `make validate` / `rector-check` / `detect-collisions` / `check-agents-adr-list` | 全部通过 |
| `make test-autoreview` | OK (1761 tests) |
| `php -d memory_limit=-1 vendor/bin/phpunit --exclude-group e2e` | OK (6813 tests, 20 skipped, 2 incomplete，均为环境限制) |
| `make mago` | 8 issues 全在 `tests/phpunit/AutoReview/Makefile/MakefileTest.php`，master 上完全相同（推测因 --prefer-source 安装依赖导致），与本改动无关 |
| zizmor / e2e / test-infection（自变异 MSI 门槛） | 未运行（无 Docker、无 xdebug/pcov） |

## 需要提交者注意

- PR 标题即 squash 后的 commit 标题，格式 `type(scope): Sentence-case`（已按此写）。
- 仓库**不要求 DCO**，commit 无 Signed-off-by。
- CI 有自变异 MSI 门槛：Infection 的 `Continue_` 变异把 `continue` 换成 `break`，三处均被新测试杀死（复核时纠正了原先"等价变异"的说法并从 PR 正文删除）；若 CI 报其他 escaped mutant 需补测试。
- CI 会跑 `make mago`；本机 mago 的 8 个问题 master 同样存在，CI（dist 安装）应不会出现，如出现请对比 master。
- PR 模板要求文档 PR 链接；本改动仅日志样式，写了 n/a，维护者若要求再去 infection/site 补。
- 建议标签：Feature/DX、Component / Reporter、Integration / GitHub（维护者打）。
- PR 正文含 AI 辅助披露段。

## 如何提交

```bash
git clone https://github.com/anyingiit/infection.git && cd infection   # 先在 GitHub 上 fork infection/infection
git remote add upstream https://github.com/infection/infection.git && git fetch upstream
git checkout -b gh-actions-colored-diffs upstream/master
git am /path/to/0001-feat-reporter-Color-the-mutant-diffs-in-the-GitHub-A.patch
git push -u origin gh-actions-colored-diffs
gh pr create --repo infection/infection --head anyingiit:gh-actions-colored-diffs \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title

`feat(reporter): Color the mutant diffs in the GitHub Actions log`

## PR body

见 `pr_body.md`。

## 独立复核（2026-10-01）

- 新鲜 clone（master @ 8fc651d）`git am` 成功；`GitHubActionsLogTextFileReporterTest` 去掉 src 修复 → 2 failures，含修复 → OK (7 tests)；`tests/phpunit/Reporter/` 133 tests OK。
- `phpstan --configuration devTools/phpstan.neon` [OK]；php-cs-fixer v3.92.5 check 0 files；`git diff --check` 干净；`mago analyze` 仅 MakefileTest.php 的 8 个既有问题。
- 修正：PR 正文删掉不准确的"等价变异"说明；`## Related issue` → `## Related issues`（对齐仓库模板）。补丁本身未改。
