# SurgeDM/Surge #265 — Add a file exists reaction setting

| 项 | 值 |
|---|---|
| Issue | https://github.com/SurgeDM/Surge/issues/265 |
| Tier | 新锐（约 3.6k stars，2026 年起快速增长，issue 编号已到 #700+） |
| Labels | good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：没有 open/merged PR。#268（Bingtagui404）做过 file-exists action，2026-04-05 因无活动被 stale 关闭，没有合并。issue 无人分配，评论里也没人认领。 |
| Base | `main` @ ce77b5de（2026-09-30） |

## 问题理解
Surge 遇到同名文件时一律自动改名为 `name(1).ext`，无法配置。issue 想要一个设置项，可选：覆盖 / 改名 / 每次询问。

## 合理性判断
- issue 是维护者 SuperCoolPencil 自己开的，带 good first issue 标签。
- #268 的同类实现没有被拒，维护者只要求补 Overwrite 模式的测试和文档，后来作者没再跟进，PR 被 stale 关闭。
- "每次询问"没有做：下载也会从 CLI、HTTP API、浏览器扩展进来，这些场景没法交互。PR 正文已说明，并表示可以后续单独做一个只在 TUI 里生效的询问模式。

## 改动
- `internal/config/settings.go`：General 下新增 `file_exists_action`（string，`rename` 默认 / `overwrite`），带 ValidateFunc，非法值由 `Validate()` 回退为默认值。
- `internal/orchestrator/file_utils.go`：`ResolveDestination` 读取这个设置。overwrite 模式下，如果同名的是普通文件，就沿用原名，完成后替换旧文件。以下三种情况仍回退为 `name(N).ext`：名字被活动下载占用、存在 `.surge` 工作文件、同名的是目录。`GetUniqueFilename` 的公开签名不变。
- `internal/orchestrator/events.go`：`finalizeCompletedFile` 原来在 rename 失败后，只要目标路径存在就算成功。overwrite 模式下，这会把替换失败（例如 Windows 上文件被占用）误报成成功，同时保留旧文件。现在只有 `.surge` 已经不存在时才这样判定。
- TUI：在该行按 Enter，在 `< Rename >` 和 `< Overwrite >` 之间切换，做法与 Theme 行相同。
- `docs/SETTINGS.md` 新增一行说明；`cmd/root_downloads.go` 更新了一处注释。

## 验证（Go 1.26.0）
- Red（还原实现文件，只保留 settings 和测试）：`go test ./internal/orchestrator ./internal/tui -run 'FileExistsAction|FinalizeCompletedFile'` 的结果：
  - `TestResolveDestination_FileExistsAction` 失败（overwrite 时得到 `report(1).pdf`）
  - `TestFinalizeCompletedFile_FailedReplaceIsNotSuccess` 失败
  - `TestSettings_FileExistsActionCycles` 失败（显示 "rename"）
- Green：上面这些测试和 `TestFileExistsActionValidation`、`TestFinalizeCompletedFile_OverwritesExistingFile` 全部通过。
- `go test -p 2 -race ./...`：除 `internal/strategy/single TestSingleDownloader_PreallocateFailure_ReleasesFileHandle` 外全部通过。这个测试在 base 上也失败，原因是以 root 运行时只读权限不生效，与本改动无关。
- `gofmt -l ./internal ./cmd`（无输出），`go vet`（config/orchestrator/tui/cmd），`go build ./...`，`go test ./internal/lint/...`：都通过。
- **没有运行**：CI 里的 `golangci-lint@latest` 和 `flakylint`。本环境不允许下载并执行外部 lint 工具，请提交前在本地跑一次：
  `go run github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest run` 和 `go install github.com/malikov73/flakylint/cmd/flakylint@v0.2.0 && flakylint ./...`

## 需要提交者注意
- 仓库没有 AI 相关政策（CONTRIBUTING、.github、labels 都查过），不需要 DCO，也没有 PR 模板和 CHANGELOG。
- PR 正文写的是 "Closes #265"，但注明了没有做 prompt 模式。如果希望 issue 保持打开，可以改成 "Refs #265"。
- 提交前请本地补跑 golangci-lint 和 flakylint（见上）。
- 维护者在 #268 提过要更新 USAGE.md。现在设置项都写在 docs/SETTINGS.md，所以只改了那里。

## 如何提交
```bash
git clone https://github.com/SurgeDM/Surge && cd Surge
git checkout -b feat/file-exists-action origin/main
git am /home/user/Playground/contributions/619-SurgeDM-Surge-265/0001-feat-settings-add-file_exists_action-setting-rename-.patch
go test ./... && go run github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest run
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/619-SurgeDM-Surge-265 SurgeDM/Surge main feat/file-exists-action contributions/619-SurgeDM-Surge-265/pr_title.txt contributions/619-SurgeDM-Surge-265/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
