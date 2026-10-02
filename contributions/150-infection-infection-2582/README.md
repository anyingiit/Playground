# infection/infection#2582 — colored diffs in github action logs

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/infection/infection/issues/2582 |
| Tier | 自由 |
| Labels | Component / Reporter, Enhancement, Feature, Help Wanted, Integration / GitHub |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01：无 open PR 引用 #2582；无 assignee、无评论认领。#2292（给 annotations 上色）已关闭，原因是 annotations 不支持 ANSI——与本 issue（日志输出）不同 |
| Base | `master` @ 8fc651d |

## 问题理解
PR #2552 新增了 `GitHubActionsLogTextFileReporter`（在 GitHub Actions 中、text log 输出到 `php://stdout` 时用 `::group::` 折叠各类 mutant）。theofidry 提出 diff 能否着色，staabm 指出 GitHub Actions 日志支持 ANSI 颜色，于是开了本 issue。

## 合理性判断
维护者自己提出、标 Help Wanted；#2292 证明 annotations 不行，但日志（log viewer）确实渲染 ANSI。改动仅影响 GitHub 日志 reporter，普通文本文件输出不变。

## 改动
- `BaseTextFileReporter`：新增 `protected function formatDiff(string $diff): string`（默认原样返回），diff 经此钩子输出。
- `GitHubActionsLogTextFileReporter`：覆写 `formatDiff()`，以 `-` 开头的行包红色 `\033[31m`，`+` 开头包绿色 `\033[32m`，以 `\033[0m` 复位（常量化，符合仓库“常量不被变异”的约定）。只处理 diff，命令行/进程输出不受影响。
- 测试：更新 `GitHubActionsLogTextFileReporterTest` 中 completeMetricsProvider 的期望输出（heredoc 内带 `\e[31m` 等）。

## 验证
环境：PHP 8.3.6 CLI（无 Xdebug/pcov），`composer install --prefer-source`（GitHub API 被屏蔽，phpstan/phpstan 的 dist 手动从 git 取）。
- red：`git stash push -- src` 后 `vendor/bin/phpunit tests/phpunit/Reporter/GitHubActionsLogTextFileReporterTest.php` → `Tests: 6, Failures: 1`
- green：恢复后 → `OK (6 tests, 6 assertions)`；`vendor/bin/phpunit tests/phpunit/Reporter` → `OK (132 tests, 200 assertions)`
- `make cs`：Fixed 0 of 1492 files；`make phpstan`：[OK] No errors；`make validate`：valid；`make test-autoreview`：OK (1761 tests)；`make rector-check`：OK；`make detect-collisions`、`make check-agents-adr-list`：通过。
- `make mago`：报 8 个问题，全部在 `tests/phpunit/AutoReview/Makefile/MakefileTest.php`，在未改动的 master 上同样出现（本地 source 安装环境问题），与本改动无关。第一版用 `Safe\preg_replace` 时 mago 报了返回类型错误，已改为 explode/str_starts_with 实现并消除。
- 全量单测 `phpunit --exclude-group=e2e,autoreview`：6840 tests，22 errors 全部是 `Console\E2ETest`（在 fixture 目录里跑 `composer install` 失败——本环境无 Xdebug/网络受限/磁盘），与 reporter 无关。注意：该测试会在 `tests/e2e/*/vendor` 下装依赖，占用了约 11 GB，已删除。

## 需要提交者注意
- 仓库有 `AGENTS.md`（专门写给 AI 贡献者的指南），允许 AI 辅助贡献；定义完成为 `make autoreview` 绿。PR 描述里已写明 Claude Code 辅助。
- squash-merge，**PR 标题即提交标题**，格式 `type(scope): Sentence-case summary`，已按此写。
- 不需要 DCO / Signed-off-by。CHANGELOG 由维护者发布时维护，无需改动。
- 仓库要求用户可见改动配 infection/site 文档 PR；本改动只是给已有输出上色，PR 里写了 n/a，若维护者要求再补。
- CI 会对改动文件跑 Infection 自测（MSI gate）；若有逃逸 mutant（例如颜色常量相关），在 PR 讨论里说明即可。
- 可在 PR 中附一张 GitHub Actions 日志截图更直观（需要真实跑一次 workflow，本环境无法做）。

## 如何提交
```bash
git clone https://github.com/anyingiit/infection.git && cd infection   # 先 fork
git remote add upstream https://github.com/infection/infection.git && git fetch upstream
git checkout -b feat/github-actions-log-colored-diffs upstream/master
git am /path/to/0001-feat-reporter-Color-mutant-diffs-in-the-GitHub-Actio.patch
git push origin feat/github-actions-log-colored-diffs
gh pr create --repo infection/infection --head anyingiit:feat/github-actions-log-colored-diffs \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`

## PR body
见 `pr_body.md`

## 独立复核（2026-10-02）
- 重复检查：issue 仍 open、无 assignee、无关联 PR；`is:pr 2582`、`is:pr is:open color` 均 0 结果。
- 新鲜浅克隆 master @ fb87644 上 `git am` 干净应用。
- red/green：去掉 `src/` 改动 → `Tests: 6, Failures: 1`；恢复 → `OK (6 tests)`；`tests/phpunit/Reporter` → `OK (132 tests, 200 assertions)`。
- PHPStan（devTools/phpstan.neon，改动的 3 个文件）：No errors；PHP-CS-Fixer v3.92.5 check：0 of 3 files；mago lint 仅 1 条既有 help（未改动行）。
- PR 正文与仓库 `.github/PULL_REQUEST_TEMPLATE.md` 结构一致；关于 `DiffColorizer` 多行回退也给 `---`/`+++` 上色的描述属实。
