# crazy-goat/tikv-php#662: guard 测试的注释剥离器不认双引号内的转义引号

| 项 | 值 |
|---|---|
| Issue | https://github.com/crazy-goat/tikv-php/issues/662 |
| Tier | 自由（crazy-goat/tikv-php） |
| Labels | good first issue, priority:low, type:chore |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 19:58 UTC：`repo:crazy-goat/tikv-php stripComment OR 662` → 0；issue 0 评论、无 assignee |
| AI 政策 | 无限制（见 330） |
| Base | `master` @ 5012ebf |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
`stripComment()` 跟踪引号，但把双引号字符串内的 `\"` 当成闭合引号，之后空白后的 `#` 被当注释截断，后面的 `<(` 进程替换就逃过 #461 的 guard。

## 改动
- `tests/Unit/Bin/PickIssueScriptGuardTest.php`：单引号外的反斜杠转义下一个字符；新增数据驱动测试 `testStripCommentFollowsTheShellQuotingRules`（10 个用例，含 issue 场景 + `<(cat)` 保留）；更新类 docblock 与方法 docblock。
- `CHANGELOG.md`：`[Unreleased]` → `### Tests`。

## 验证
- 红：只加测试不改剥离器 → 2 个用例失败（双引号内转义引号、引号外转义引号）。
- 绿：该文件 15 tests OK；全量 Unit 1850 OK（2 skipped 同 master）；phpstan 无错；phpcs/rector 干净。
- 未跑：Grpc 套件、E2E、shellcheck（未改 shell）。

## 需要提交者注意
- 与 330/331 都改 `CHANGELOG.md` `[Unreleased]`，后合并的可能需要 rebase（三个 PR 依次提交即可）。

## 如何提交
```
tools/submit_pr.sh contributions/332-crazy-goat-tikv-php-662 crazy-goat/tikv-php master test/662-strip-comment-escaped-quote contributions/332-crazy-goat-tikv-php-662/pr_title.txt contributions/332-crazy-goat-tikv-php-662/pr_body.md
```

## 独立复核（2026-10-22 20:03 UTC）
- Issue #662：WebFetch 确认仍 open、无 assignee、0 评论、无关联 PR；MCP 搜索 `repo:crazy-goat/tikv-php 662` / `stripComment` → 0；仓库唯一 open PR 为 #737（#686，无关）。
- Patch 在 master@5012ebf 上 `git am` 干净；作者 anyingiit <49945850+anyingiit@users.noreply.github.com>；commit message 无 AI 模型名；标题符合 `type: subject (#N)`。
- 复跑：该测试文件 15 tests / 31 assertions OK；Unit 套件 1850 tests、2 skipped OK；phpstan 无错；phpcs 退出码 0；rector dry-run 无改动。PR 正文所有数字均核对一致（10 个数据集、15 tests、1850/2 skipped、2 个失败用例）。
- 红→绿：仅删除 stripComment() 中新增的 4 行反斜杠分支 → 恰好 "escaped quote inside double quotes" 与 "escaped quote outside quotes" 2 个失败；恢复后全绿。
- 与真实 bash 对比（`declare -f` 输出判断注释起点）13 个用例：issue 场景、`\\"`、单引号内 `\`、引号外 `\"`、`\#`、`${#a[@]}`、行尾 `\` 续行等全部与 bash 一致；行尾反斜杠时 `$i++` 越界只会结束循环，无副作用。
- 已知残余差异（均为旧实现已有、非本 PR 引入、bin/pick-issue.sh 中不存在，不阻塞）：`a\ #x`（转义空格后的 `#` 在 bash 中不是注释，剥离器会截断）、`$'a\' # b'`（ANSI-C 字符串里 `\'`）、反引号内的 `"\`"`。脚本中唯一的 `$'…'` 是 `$'\x1f'`/`$'\x1e'`，无问题。
- 对真实 bin/pick-issue.sh：新旧剥离器逐行输出完全相同；在脚本副本末尾追加 `done < <(echo "a \" # b")` 后 guard 能检出 `<(`。
- CHANGELOG 放在 `[Unreleased]` → `### Tests`，与仓库既有写法一致；PR 正文结构对应 `.github/pull_request_template.md`。
- 复核过程中我的 worktree 在 master 分支上执行了 git am，导致本地 clone 的 `master` 被推进到补丁提交；已 `git branch -f master 5012ebf` 恢复，worktree 已删除。包内文件除本节外未改动。
- 结论：PASS
