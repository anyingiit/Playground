# restic/restic#22078 — sftp: ssh's error line not printed when session fails on loaded host

| 项 | 值 |
|---|---|
| Issue | https://github.com/restic/restic/issues/22078 |
| Tier | 高星 |
| Labels | 无（issue 未打标签） |
| Status | ✅ ready — 独立复审通过（2026-10-01 23:45 UTC）：全新 clone 上 git am 成功，新测试去掉修复时 FAIL、加上修复时 PASS（含 -race），sftp 包全部测试、gofmt、go vet、golangci-lint 均通过；issue 仍无竞争 PR |
| Base | `master` @ 5127c4a (2026-09-25) |
| Duplicate-PR check | 2026-10-01 23:20、23:30 和 23:45 UTC（复审）各查一次：`pulls?q=22078` 无结果；`is:pr sftp` 和 `sftp stderr` 关键词搜索没有涉及 stderr、NewClientPipe 或 #22078 的 PR。issue 0 条评论，无人认领，无 assignee，没有关联分支或 PR |

## 问题理解

`internal/backend/sftp/sftp.go` 的 `startClient` 用 `cmd.StderrPipe()` 加一个 goroutine 把 ssh 的 stderr 转发到 restic 的 errorLog。`sftp.NewClientPipe` 失败时（比如 ssh 连不上端口），函数立刻返回错误，restic 随即退出，这时 goroutine 可能还没打印 ssh 的 "Connection refused"。另外，`cmd.Wait()` 在进程退出后会关闭 StderrPipe 的读端，没读完的数据会丢失。reporter 的 Build A/B 实验对应这两点：只修第二点是 213/300，两点都修是 300/300。

## 合理性判断

- 这是一个可复现的真实 bug（用户看不到 ssh 的诊断信息），根因分析清楚，修复范围小，属于 sftp 后端的正常 bugfix。
- issue 正文写明 "AI-drafted, verified by me before filing"，维护者没有反对。
- AI 政策：仓库没有 AGENTS.md 或 CLAUDE.md；CONTRIBUTING.md、.github/（PR 模板、issue 模板）和 labels 页都没有禁止 AI 的规则。
- 外部 PR 近期常被合并，例如 #22007、#22028、#22029、#21897。

## 改动

- `internal/backend/sftp/sftp.go`
  - stderr 改用 `os.Pipe()`（`cmd.Stderr = stderrW`）。`cmd.Wait()` 不会关闭它，所以读端总能读到 EOF，不会丢数据。父进程在 `StartForeground` 之后立即关闭自己持有的写端；StdinPipe/StdoutPipe 出错的路径也会关闭写端。
  - 读 stderr 的 goroutine 结束时 `close(stderrDone)`。`NewClientPipe` 失败时先等 `stderrDone` 再返回，最多等 `closeTimeout`（2s），避免子进程不退出或孙进程持有 stderr 时卡住。
  - 有意没让 `cmd.Wait()` 的 goroutine 等 stderr。否则如果 ControlMaster 之类的孙进程继承了 stderr，`Close()` 可能永远卡住。
- `internal/backend/sftp/sftp_test.go`：新增 `TestOpenFailurePrintsStderr`。用 `sftp.command` 运行 `sh -c 'exec >&-; sleep 0.5; echo connection refused >&2'`，先关 stdout 让 session 立即失败，再延迟打印 stderr，以此确定性地复现竞态。没有 sh 时 skip（Windows）。
- `changelog/unreleased/issue-22078`：Bugfix 条目，按 TEMPLATE 格式写。

## 验证

环境：Go 1.25.10（go.mod 指定的 toolchain），`GOCACHE` 和 `GOMODCACHE` 放在工作目录内。`apt-get install openssh-sftp-server` 之后 `TestBackendSFTP` 等测试才会真正运行，不再 skip。

| 命令 | 结果 |
|---|---|
| 只加新测试、不改 sftp.go：`go test -count=1 -run TestOpenFailurePrintsStderr ./internal/backend/sftp/` | **FAIL**：`stderr of the command was not logged before Open returned, got []` → red |
| 打补丁后同一命令 | PASS (0.50s) → green |
| `go test -race -count=10 -run TestOpenFailurePrintsStderr ./internal/backend/sftp/` | ok |
| `go test -count=1 -v ./internal/backend/sftp/`（有 sftp-server） | 8 个测试全部 PASS（TestBackendSFTP、TestLayout、TestCreateSetsDirPermissions、TestSaveSetsDirPermissions 等） |
| `golangci-lint run --concurrency 2 ./internal/backend/sftp/...`（仓库 .golangci.yml） | 0 issues |
| `go vet ./internal/backend/sftp/`，`gofmt -l internal/backend/sftp` | clean。全仓 `gofmt -l internal/` 只报出 `internal/backend/s3/s3_test.go`，这是 base 上已有的问题，与本补丁无关 |
| 实机复现：编译 base 和 fixed 两个 `restic`，在 4 核上跑 6 个 busy loop 制造负载，各执行 100 次 `restic -r sftp://127.0.0.1:2222//tmp/nope cat config`，统计输出含 "Connection refused" 的次数 | base **85/100**，fixed **100/100** |

## 需要提交者注意

- CONTRIBUTING 第 0 步建议先在 issue 下留言说明要做这个修复。可以先评论再开 PR，也可以直接开 PR。
- 不需要 DCO 或 Signed-off-by。提交信息采用 restic 风格（`sftp: ...` 前缀加简短摘要和正文），正文中写了 `Fixes #22078`。
- PR 模板是仓库自己的格式（三个标题加 checklist），pr_body.md 已按它改写，并加入披露段落。PR 时请勾选 "Allow edits from maintainers"。
- 有一个相关的 open PR #5752（sftp 断线重连）也改动 sftp 后端，合并时可能有小冲突，但它和本 issue 无关。
- 设计取舍已写在 PR 描述里：等待上限是 closeTimeout，且没有让 `cmd.Wait()` 等 stderr。维护者可能更倾向 reporter 的 Build B 写法。

## 如何提交

```bash
git clone https://github.com/restic/restic && cd restic
git checkout -b sftp-stderr-race origin/master
git am /path/to/0001-sftp-wait-for-ssh-s-stderr-before-reporting-a-failed.patch
gofmt -l internal/backend/sftp && go test ./internal/backend/sftp/
git push <your-fork> sftp-stderr-race   # PR 目标分支: master
```

PR 标题见 `pr_title.txt`，PR 正文见 `pr_body.md`。
