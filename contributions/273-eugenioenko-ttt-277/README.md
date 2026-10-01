# eugenioenko/ttt#277 — Add read-only file indicator and save protection

| 项目 | 内容 |
|---|---|
| Status | ✅ ready — 实现完成，red→green 已验证，go test / vet / golangci-lint / gofmt 全部通过（2026-10-01） |
| Issue | https://github.com/eugenioenko/ttt/issues/277 |
| Tier | 新锐 |
| Labels | good first issue |
| Base | `main` @ 5db5bcf |
| 重复 PR 检查 | 2026-10-01 用 WebFetch 查了 issue 页面（没有关联 PR、没有 assignee、没有评论）和 `/pulls?q=read-only`，没有找到相关 PR |
| AI 政策 | 允许 AI 辅助贡献：CONTRIBUTING 只要求删掉多余注释，AGENTS.md 是写给 AI 贡献者的说明 |

## 问题理解
文件权限为 0444 时，编辑器没有任何只读提示，保存时会悄悄覆盖。原因是保存流程先写临时文件再 rename 覆盖目标文件，只要所在目录可写，rename 就会成功。issue 期望两点：在 tab 或状态栏显示只读标记；保存前警告或阻止，除非用户明确选择覆盖。

## 合理性判断
这是维护者自己从 QA BUG-019 拆出来的 good first issue，需求明确、范围小，没有人认领。

## 改动（8 个文件，+140/−1）
- `internal/core/buffer/buffer.go`、`io.go`：新增 `ReadOnlyOnDisk` 字段，在 `recordDiskInfo` 里设置（加载和保存都会调用），判断标准是文件没有任何写权限位（`Perm()&0222 == 0`）。
- `internal/ui/tabbar_widget.go`、`editor_group.go`：tab 标题加 ` (readonly)` 后缀，沿用项目里只读查看 tab 已有的写法。如果 tab 本身已经是只读查看 tab，就不再重复加。
- `internal/app/commands_editor.go`：`SaveFile` 遇到只读文件先弹出 `Cancel / Overwrite` 确认框（默认 Cancel）。选 Overwrite 后进入原有的“磁盘已修改”检查（拆成 `saveFileCheckingDisk`），再走正常保存。因为 SaveFile 本来就保留文件权限，覆盖后文件仍是 0444。
- `internal/app/app_lsp.go`：LSP rename 的 `SaveOnRename` 遇到只读文件时不自动保存，buffer 保持未保存状态。
- 测试：`internal/core/buffer/io_test.go` 新增 `TestReadOnlyOnDisk`；新增 `tests/e2e/readonly_file_test.go`，共 3 个用例。

## 验证（在 /home/user/work/ttt，Go 1.25.0）
- **red**（只保留结构体字段，回退 io.go / commands_editor.go / editor_group.go 的行为改动）：`TestReadOnlyOnDisk`、`TestReadOnlyFileShowsIndicator`、`TestReadOnlyFileSavePromptsAndCancelKeepsFile` 失败。`...OverwriteKeepsPermissions` 在修复前也能通过，它是回归保护用例，不是 red 用例。
- **green**：`go test ./internal/core/buffer/ -run TestReadOnlyOnDisk` 和 `go test ./tests/e2e/ -run TestReadOnlyFile -v` 全部通过。
- `go test ./...`：全部通过。注意：本环境的 `GIT_AUTHOR_*` 环境变量和全局 git config 会让 `TestBlameLineBasic`、`TestGitRelativePathEnablesBlameForExternalFileSymlink` 失败（它们断言 blame 作者是 "Test User"）。去掉这些环境变量、并设置 `GIT_CONFIG_GLOBAL=/dev/null` 后，`internal/git` 和 `internal/app` 都能通过。这两个失败是环境问题，和本改动无关。
- `go vet ./...` 干净；`golangci-lint run ./...` 报告 0 issues；`gofmt -l internal tests` 无输出。
- 没有运行：`go test -race ./...`、pnpm functional / integration 测试（需要 pnpm 和编译好的二进制）。

## 需要提交者注意
- 不需要 DCO，也不要求 AI trailer；commit 作者是 anyingiit（noreply 邮箱）。
- AGENTS.md 要求界面可见的改动在 PR 里附截图，并且要在真实二进制里跑过。建议提交前在本地执行：`make build && chmod 444 /tmp/x.txt && ./bin/ttt --size 100x20 --exec "open /tmp/x.txt; screenshot /tmp/ro.png" /tmp/x.txt`（命令写法以 AGENTS.md 的 `--exec` 说明为准），然后把截图贴进 PR 正文。
- 只读判断依据的是权限位，不是当前用户的实际写权限：一个 0644 但属于其他用户的文件不会被标记。这是有意保持简单，审阅时如有需要可以说明。

## 如何提交
```bash
tools/submit_pr.sh contributions/273-eugenioenko-ttt-277 eugenioenko/ttt main fix/readonly-file-indicator contributions/273-eugenioenko-ttt-277/pr_title.txt contributions/273-eugenioenko-ttt-277/pr_body.md
```
手动提交的话：fork 后在 `main` 上执行 `git am 0001-feat-editor-flag-read-only-files-and-confirm-before-.patch`，push 到分支，然后开 PR。标题见 `pr_title.txt`，正文见 `pr_body.md`。
