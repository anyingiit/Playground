# kubecolor/kubecolor#171

Status: ✅ ready — 补丁、测试 red→green、全量检查、PR 文本均已完成 (2026-10-01)

| 项 | 内容 |
|---|---|
| Issue | https://github.com/kubecolor/kubecolor/issues/171 "Possibly incorrect subcommand parsing when common options passed" |
| Tier | 自由 |
| Labels | bug |
| 状态 | 开放、无指派、无评论 |
| 重复 PR 检查 | `/pulls?q=171` 无相关；开放 PR 仅 #369（bundled watch flags 与 pager，改的是 flag 解析 switch，与本问题不同，可能有轻微文本冲突）和 #280（line reading）。无重复 |
| AI 政策 | CONTRIBUTING / labels / 仓库内无 AI 相关规定；不需要 DCO、不需要 AI trailer |

## 问题理解
`kubecolor -n config get pod`：`InspectSubcommandInfo` 从左往右找第一个“看起来像子命令”的参数，把 `-n` 的值 `config` 当成了子命令，于是用错 printer。

## 合理性判断
确为 bug（kubectl 本身会把 `config` 当 namespace）。修复范围小，维护者已贴 bug 标签。

## 改动 (`kubectl/subcommand.go`)
- 新增 `globalFlagsWithValue`（`kubectl options` 中需要值的全局 flag：`-n/--namespace`、`--context`、`--kubeconfig`、`-s/--server`、`--user`、`--cluster`、`-v/--v`、`--token`、`--as*`、日志相关等）和 `isGlobalFlagWithSeparateValue`。
- 查找子命令时，遇到这些 flag（值以单独参数给出的形式）就跳过下一个参数。`-n=x` / `-nx` 本就是单参数，不受影响；子命令之后的 flag 不受影响（找到子命令即返回）。
- `kubectl/subcommand_test.go` 新增 10 个用例。

## 验证 (Go 1.26.6，GOCACHE 在工作目录内)
- Red（只加测试）：`go test ./kubectl/` → FAIL，7 个新子测试失败（`-n config get pod`、`--namespace config get pod`、`--context logs get pod`、`--kubeconfig apply describe pod`、`-s top --user exec get pod -o wide`、`-n get`、`--context testplugin get pod`）。
- Green：`go test ./kubectl/` ok；`go test -race ./kubectl/` ok
- `go test ./...` 全部 ok；`go run ./internal/cmd/testcorpus`（make corpus）Passed 98 / Failed 0
- `go fmt ./...`、`go vet ./...` 无输出
- `staticcheck ./...`（make lint）：6 条，全部在 `internal/cmd/configdoc/print_env.go`，属既有问题，与改动文件无关（kubectl/ 0 条）

## 需要提交者注意
- 提交者身份 anyingiit（49945850+anyingiit@users.noreply.github.com）；仓库不要求 DCO / AI trailer，未添加。
- PR 正文已含 Claude Code 披露段落。
- 若 #369 先合并，可能需要 rebase（同文件不同函数）。

## 如何提交
base 分支：`main`（补丁基于 189d201）
```bash
git clone https://github.com/kubecolor/kubecolor && cd kubecolor
git checkout -b fix-171-global-flag-values
git am /path/to/350-kubecolor-kubecolor-171/0001-*.patch
go test ./...
# fork 并推送分支后：
tools/submit_pr.sh contributions/350-kubecolor-kubecolor-171 kubecolor/kubecolor main fix-171-global-flag-values contributions/350-kubecolor-kubecolor-171/pr_title.txt contributions/350-kubecolor-kubecolor-171/pr_body.md
```

## PR 标题 / 正文
见 `pr_title.txt`、`pr_body.md`。
