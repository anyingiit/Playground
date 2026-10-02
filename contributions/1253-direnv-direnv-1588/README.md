# direnv/direnv#1588 — direnv reload silently fails when .envrc not allowed

| 项 | 内容 |
|---|---|
| Issue | https://github.com/direnv/direnv/issues/1588 |
| Tier | 高星（Go） |
| Labels | Feature |
| Status | ✅ ready — independently reviewed 2026-10-01: patch applies to master b00e451 (still HEAD), test red without fix / green with it, go test ./... + go vet + golangci-lint clean, author verified, issue still open with no competing PR (not submitted) |
| Base | `master` @ b00e451 (2026-03-31, master 的最新提交) |
| Duplicate-PR check | 2026-10-01 检查：issue 0 评论、无 assignee、无关联 PR/分支；`pulls?q=is:pr 1588` 0 结果；`is:pr reload` 只有已合并的 #1543（只处理 Denied，即本 bug 的前身）；2026-04 以后含 "allow" 的 open PR（#1611/#1594/#1592/#1591/#1586/#1579）都与此无关 |

## 问题理解

mightyiam 报告：`.envrc` 未被 allow 时执行 `direnv reload` 没有任何输出且 exit 0，用户以为 reload 成功了；希望返回非零退出码并说明 .envrc 未被允许。

代码（`internal/cmd/cmd_reload.go`）：#1543（2026-03 合并）只加了 `if foundRC.Allowed() == Denied` 的判断。`RC.Allowed()` 有三种状态 Allowed / NotAllowed / Denied；从未 allow 过、或 allow 后内容被修改（最常见）的 .envrc 都是 **NotAllowed**，于是落到 `foundRC.Touch()`，静默 exit 0。

## 合理性判断

- 行为明显是 #1543 修复的遗漏：#1543 的目标正是"reload 对被阻止的 .envrc 要报错"，只覆盖了 Denied。`RC.Load` 中 NotAllowed 也是用同一条 `notAllowed` 错误消息，所以 reload 复用它最一致。
- issue 打的是 Feature 标签，但改动极小、无兼容性风险（只把原本 exit 0 但什么都不会加载的情况改为报错）。
- AI 政策：仓库无 AGENTS.md/CLAUDE.md，CONTRIBUTING.md 只讲 release 流程，labels 无描述涉及 AI；而且 #1543 本身来自 `claude/…` 分支并被合并 → 无 AI 禁令。
- 注意：master 自 2026-03-31 后没有新提交，维护者近期合并不活跃，PR 可能需要较长时间才被处理。

## 改动

- `internal/cmd/cmd_reload.go`：`if foundRC.Allowed() == Denied` → `if foundRC.Allowed() != Allowed`（1 行）。
- 新增 `internal/cmd/cmd_reload_test.go`：用 `t.TempDir()` 构造 Config（WorkDir/DataDir），直接调用 `CmdReload.Action.Call`，测试 NotAllowed（报错且消息含路径和 `direnv allow`）、Denied（报错）、Allowed（成功）三种情况。

## 验证

环境：Go 1.24.7（与 CI 的 `go-version: '1.24'` 一致），`GOCACHE/GOMODCACHE` 设在工作目录。

| 命令 | 结果 |
|---|---|
| 仅加测试、未改代码：`go test ./internal/cmd/ -run TestReload -v` | **FAIL**：`TestReloadNotAllowed: expected direnv reload to fail for a .envrc that was never allowed`（Denied/Allowed PASS）→ red |
| 加修复后同命令 | 3 个全部 PASS → green |
| `go test ./...`（CI 的 Test 步骤） | internal/cmd、pkg/dotenv、pkg/sri 全部 ok |
| `go vet ./...` | 无输出 |
| `golangci-lint run --concurrency 2 ./internal/cmd/...`（仓库 .golangci.yml） | 0 issues |
| `gofmt -l .` | 只列出 `gzenv/gzenv.go`、`internal/cmd/cmd_fetchurl.go` — 基线上同样存在，与本改动无关；新文件已 gofmt |
| `go build` 后 `bash ./test/direnv-test.bash`（CI 的 make test-bash） | exit 0 |
| 手动端到端（XDG_DATA_HOME 指向临时目录） | 未 allow：`direnv: error …/.envrc is blocked. Run \`direnv allow\` to approve its content`，exit=1；allow 后：exit=0；deny 后：同样报错，exit=1 |

未运行：elvish/fish/tcsh/zsh/pwsh/murex shell 集成测试（本机无这些 shell，且改动不涉及 shell hook）、Windows/macOS 矩阵。

## 需要提交者注意

- 仓库无 DCO / Signed-off-by 要求，无 PR 模板（只有 ISSUE_TEMPLATE）；CHANGELOG 由 `make prepare-release` 生成，不需要手写。
- 无 AI 禁令；PR 描述中已含 Claude Code 披露段落。
- 提交信息风格参照 #1543（`Fix \`direnv reload\` doing nothing after \`direnv deny\``），正文 `Fixes #1588`。
- 维护者合并节奏较慢（master 最后一次提交 2026-03-31），提交后请耐心等待。

## 如何提交

```bash
git clone https://github.com/direnv/direnv && cd direnv
git checkout -b fix-reload-not-allowed origin/master
git am /path/to/0001-Fix-direnv-reload-silently-succeeding-when-.envrc-is.patch
go test ./internal/cmd/ -run TestReload -v
git push <your-fork> fix-reload-not-allowed   # PR 目标分支: master
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
