# privateerproj/privateer-sdk#311: NeedsReview-only run reported as "Unexpected exit"

| 项 | 值 |
|---|---|
| Issue | https://github.com/privateerproj/privateer-sdk/issues/311 |
| Tier | 自由 |
| Labels | good first issue |
| Status | ✅ ready（patch + PR 文本已完成，未提交；已经过独立复审） |
| Base | `main` @ 66b9dce（`ci(release-drafter): ... (#315)`） |
| Duplicate-PR check | 2026-10-01 检查：issue open、0 comments、无 assignee；`pulls?q=311` 只有 #310（已合并，是 issue 提到的相关重构）和 #210（依赖升级）；关键词 `NeedsReview` 命中 #298/#252（已合并）和 #287（open，AI 配置，与本 issue 无关）；`"unexpected exit"` 命中 #310、#191（closed）。都不是修这个 issue 的 PR |

## 问题理解

如果一次 `pvtr run` 只有 `NeedsReview`（warning），没有 `Failed`：
- `pluginkit.ExitCodeFor` 把 Failed、NeedsReview、Unknown 都映射成 `shared.TestFail`(1)；
- `command.runOne` 只设置 `Successful = (code == TestPass)`，`Error` 留空；
- `PluginPkg.closeClient` 只有 Successful 和 Error 两个分支，其余情况一律记为 `[WARN] Unexpected exit from X with no error or success`；
- 另外，`EvaluationSuite.Evaluate` 的汇总行只要结果不是 Passed/NotRun 就记 `ERROR`，所以 NeedsReview 也记成了 ERROR。

Issue 提出的建议有三条：(1) closeClient 把“没有 error、但不是 pass”的退出当作正常结果，用 Info/Warn 记录；(2) 讨论 NeedsReview 是否要单独一个退出码；(3) 让 `debug` 子命令返回 `ExitCodeFor(...)`。

## 合理性判断

- 报告者已经把根因定位清楚，打了 good first issue 标签，属于 bug。现在的日志确实有误导性（把正常的“有 warning”结果说成插件异常退出）。
- AI 政策：仓库没有 CONTRIBUTING、AGENTS.md 或 PR 模板，label 描述里也没有 AI 相关规定（`.gitignore` 里甚至忽略了 `.claude/*.local.*`），所以没有禁令。
- 设计问题按协调者给的最小方案处理：NeedsReview 仍然算普通失败（退出码保持 `TestFail`），只把日志改成 Warn。理由写在 PR 里：单独加退出码会改动 `shared/exitcodes.go` 和 `exitSeverity`，并影响下游 CI 的行为，这应该由维护者决定。第 (3) 条 `debug` 退出码也没有改，同样会改变可观察的行为，在 PR 里说明可以作为后续。所以 PR 写的是 `Refs #311`，没有写 Closes。

## 改动（5 个文件，+115/−10）

- `command/types.go`：`PluginPkg` 新增 `ExitCode int` 字段。`closeClient` 的日志逻辑抽到 `logResult`，改用 switch：Successful 记 Info；有 Error 记 Error；`ExitCode == TestFail` 记 **Warn** `Plugin for X completed with non-passing results`；其他情况仍记 “Unexpected exit ...”，并附上 `(exit code N)`。
- `command/run.go`：`runOne` 在正常结束时记录 `ExitCode`；两个 RPC 初始化失败的分支记录 `InternalError`。
- `pluginkit/evaluation_suite.go`：汇总行的级别选择抽成 `logSuiteSummary`，NeedsReview 记 **Warn**，Failed/Unknown 仍记 Error。新增 `hclog` import（模块已经直接依赖 go-hclog）。
- 测试：`command/types_test.go` 新增 `TestLogResult`（4 个用例），`pluginkit/evaluation_suite_test.go` 新增 `TestLogSuiteSummary`（5 种 result）。

## 验证

环境：本机 Go 1.24.7，`go.mod` 要求 `go 1.26.2`，用 `GOTOOLCHAIN=auto` 自动下载了 go1.26.2。GOPATH/GOCACHE 放在 `/home/user/work/privateer-sdk-cache`，`GOFLAGS=-p=2`。

| 命令 | 结果 |
|---|---|
| 基线 `go vet ./... && go test ./...` | 全部 ok |
| **Red**：保留新测试和辅助函数，只去掉新增的 `ExitCode == TestFail` 分支、`(exit code %d)` 和 `case gemara.NeedsReview` → `go test ./command/ ./pluginkit/ -run 'TestLogResult\|TestLogSuiteSummary'` | FAIL：`clean TestFail` 得到 `[WARN] Unexpected exit from svc with no error or success`；`host-level` 用例缺少 exit code；`Needs_Review` 得到 `[ERROR] summary` |
| **Green**：恢复修复后同一命令 | PASS（4 + 5 个子测试） |
| `go vet ./...` | 无输出 |
| `go test -race ./... -coverprofile coverage.out -covermode atomic`（与 CI 相同） | 所有包 ok；total coverage 68.7%（CI 门槛 45%）。`shared` 包（没有测试文件）打印了 `go: no such tool "covdata"`，原因是自动下载的 toolchain 不带 covdata 工具，属于本机环境问题，与本改动无关 |
| `go build ./...` | ok |
| `golangci-lint run ./...`（v2.11.4，与 lint.yml 相同版本，`go install` 安装） | 0 issues |
| `gofmt -l .` | 无输出 |
| `git apply --check` 到 66b9dce 的干净 worktree | OK |

没有做：用真实插件跑一次 `pvtr run`（需要安装插件和 grc.store catalog），只做了单元测试层面的验证。

## 如何提交

```bash
git clone https://github.com/privateerproj/privateer-sdk && cd privateer-sdk
git checkout -b fix/needs-review-exit-log origin/main
git am /path/to/0001-fix-command-do-not-report-NeedsReview-only-runs-as-a.patch
# 如需 DCO：git commit --amend -s --no-edit
git push <your-fork> fix/needs-review-exit-log   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

### 独立复审（2026-10-01 20:2x UTC）
- 重新读了 issue #311（仍 open、无评论、无 assignee）；`pulls?q=311` 仍只有 #310、#210，没有重复 PR。
- 用 go1.26.2 重新跑：去掉三个新分支后 `go test ./command/ ./pluginkit/ -run 'TestLogResult|TestLogSuiteSummary'` 3 个子测试 FAIL（`Unexpected exit`、缺 exit code、NeedsReview 记为 `[ERROR]`）；恢复后 PASS。`go vet ./...`、`gofmt -l .` 无输出，`go test -race ./...` 全部 ok。
- 检查了 `shared/plugin.go`：干净的 TestFail 经 RPC 返回时 `Err` 为空，所以确实走到新的 Warn 分支；带 error 的情况仍走 Error 分支。commit 作者为 anyingiit，无 AI 模型名。
- 保留 `Refs #311`（不是 Closes）：issue 第 (3) 条 `debug` 子命令退出码没有处理，写 Closes 会让 issue 被关掉而遗漏这一点。复审未改动 patch。

### 需要提交者注意
- PR 标题会被 `pr-title.yml` 检查是否符合 Conventional Commits，`pr_title.txt` 已经是 `fix(command): ...` 格式。
- 维护者的 commit 大多带 `Signed-off-by`，但仓库没有 DCO 文档或 DCO 检查，也有不带 sign-off 的 commit，所以 patch 里没加。如果 PR 上出现 DCO 检查，用 `git commit --amend -s` 补上（身份用 anyingiit）。
- PR 用的是 `Refs #311`，不是 Closes：单独的 NeedsReview 退出码和 `debug` 子命令退出码这两点留给维护者决定，PR 正文里已经说明。如果维护者希望一并处理，可以追加 commit。
- `PluginPkg` 新增了导出字段 `ExitCode`（这是向后兼容的新增）。
- 仓库没有 CHANGELOG（用 release-drafter 生成），也没有 PR 模板。
