# charmbracelet/lipgloss#749 — v2: importing lipgloss runs `tmux info` at package init

| 项 | 值 |
|---|---|
| Issue | https://github.com/charmbracelet/lipgloss/issues/749 |
| Tier | 高星 (Go) |
| Labels | 无（issue 2026-10-01 新开，尚未分类；仓库有 `bug`/`v2`/`proposal` 等标签） |
| Status | ✅ ready — patch + PR text done (not submitted)，已经独立复审；含一个需维护者认可的兼容性取舍（见下） |
| Base | `master` @ 6a419c6 (2026-09-11, "feat: add `FitContent` property to table renderer (#697)") |
| Duplicate-PR check | 2026-10-01 检查：`pulls?q=749`、`Writer lazy`、`tmux`、`colorprofile Detect` 均无相关 PR（只有 #692 compat 包 NO_COLOR、#713 query 非终端句柄，均与本问题不同）；issue 0 评论、无 assignee、无关联分支/PR |

## 问题理解

`writer.go` 里 `var Writer = colorprofile.NewWriter(os.Stdout, os.Environ())` 在包初始化时就调用
`colorprofile.Detect`。在 tmux 里（`TMUX` 已设置、stdout 是 TTY、非 TrueColor 环境）Detect 会
`exec.CommandContext(context.Background(), "tmux", "info")`，无超时。于是只要 import lipgloss（哪怕只用
`Style.Render`）每次启动都要起一个子进程；报告者的 CLI `version` 命令从 4.4ms 变成 8.8ms，tmux server
卡住时甚至会阻塞在 `main()` 之前。期望：import 不起进程，Writer 在首次使用时（Print 系列）再检测。

## 合理性判断

- 真实的性能/可靠性回归（v1→v2），问题描述准确，代码定位清楚；issue 提出的方案（首次使用时再检测）合理。
- AI 政策：仓库无 CONTRIBUTING/AGENTS/CLAUDE；README 和 UPGRADE_GUIDE_V2 甚至主动建议用 LLM 做迁移；标签说明无 AI 限制。无禁令。
- 难点：`Writer` 是导出的 `*colorprofile.Writer` 变量（UPGRADE 指南文档化了 `lipgloss.Writer = ...` 与
  `lipgloss.Writer.Profile = ...` 两种用法），无法做到 100% 行为兼容的懒加载。采用 `Profile == Unknown`
  作为“尚未检测”哨兵（`colorprofile.Unknown` 官方语义就是“没有 profile”，`Detect` 从不返回它），
  上述两种文档化用法都保持可用。

## 改动

- `writer.go`
  - `Writer` 初始化为 `&colorprofile.Writer{Forward: os.Stdout}`（Profile = Unknown），不再在 init 检测。
  - 新增 `defaultWriter()`：加锁，若 `Writer.Profile == Unknown` 则对 `Writer.Forward` 调 `colorprofile.Detect` 并写回；返回 `Writer`。
  - `Print/Println/Printf` 改写到 `defaultWriter()`；`Sprint/Sprintln/Sprintf` 改用 `defaultWriter().Profile`。`Fprint*` 不变。
  - `Writer` 文档注释说明懒检测行为及如何跳过（设 Profile / 替换 Writer）。
- `writer_test.go`（新文件）：`TestWriterDetectsProfileLazily` 用子进程重跑测试二进制（`-test.run=^TestWriterHelper$`），
  环境 `TMUX=...`、`TERM=xterm`、`TTY_FORCE=1`、`PATH=<tmp>`，tmp 里放一个假的 `tmux` 脚本（`: > marker`）记录是否被调用。
  子测试：`import`（只 import 不应调用 tmux）、`print`/`sprint`（应触发检测）、`preset profile`（先设 `Writer.Profile` 再 Print，不应检测）。Windows 上 skip。

## 验证

环境：`GOCACHE/GOMODCACHE/GOPATH` 均设在 `/home/user/work/s2-1258` 内；系统 go1.24 自动下载 go.mod 要求的 toolchain go1.26.7。

| 命令 | 结果 |
|---|---|
| 未修复（`git stash push writer.go`，保留新测试）`go test -run TestWriter -v .` | **FAIL**：`import` 子测试 “importing lipgloss ran `tmux info`…”，`preset_profile` 子测试 “color profile was detected even though Writer.Profile was set”；print/sprint PASS → red |
| 修复后 `go test -run TestWriter -count=1 -v .` | 4 个子测试全部 PASS → green |
| `go test -p 2 -count=1 ./...` | lipgloss / list / table / tree 全部 ok（compat 无测试） |
| `go vet . ./compat` | clean。（`go vet ./...` 在未改动的 `table/table_test.go:826` 报 “result of … String call not used”，为基线已有问题） |
| `golangci-lint run -j 2 .`（仓库 `.golangci.yml`；系统自带 v2.5.0 用 go1.25 构建，无法加载 go1.26 模块，故用 go1.26.7 重新 `go install` 了同版本 v2.5.0） | 改动文件无告警；仅 3 条基线已有的 gofumpt 告警（`color.go:152`、`get.go:483`、`terminal.go:46` 的裸 `return`），均为未改动文件 |
| `gofmt -l .` | 无输出 |

## 需要提交者注意

- **兼容性取舍（PR 描述里已向维护者说明）**：在任何 Print/Sprint 被调用之前，直接读取 `lipgloss.Writer.Profile`
  会得到 `Unknown`，直接 `fmt.Fprint(lipgloss.Writer, s)` 会因 Unknown（≤NoTTY）被剥掉 ANSI 颜色。若维护者不接受，
  可能会改成导出访问函数或在 colorprofile 侧处理（加超时/缓存），PR 可能被关闭或要求改设计。
- `compat` 包仍在 init 时检测 Profile 并查询背景色（独立的 opt-in 包，且已有 #692 涉及），本 PR 未改。
- 仓库无 PR 模板、无 CONTRIBUTING、无 DCO、无 CHANGELOG 文件；提交信息为 Conventional Commits（`fix: ...`），合并时会追加 `(#PR号)`。
- 已在 PR 描述中加入 Claude Code 披露段落；提交中无 AI 名称/trailer。
- issue 当天新开、维护者尚未回应；提交前建议再看一眼 issue 是否已有维护者表态或 PR。

## 如何提交

```bash
git clone https://github.com/charmbracelet/lipgloss && cd lipgloss
git checkout -b lazy-writer-profile origin/master
git am /path/to/0001-fix-detect-the-default-Writer-s-color-profile-lazily.patch
go test ./...
git push <your-fork> lazy-writer-profile   # PR 目标分支: master
```

PR 标题见 `pr_title.txt`，PR 正文见 `pr_body.md`。

## 独立复审（2026-10-01 23:50 UTC）

- 全新 `git clone --depth 1`（master @ 6a419c6，与 Base 一致）后 `git am` 补丁：干净应用；提交作者为 `anyingiit <49945850+anyingiit@users.noreply.github.com>`；补丁/提交信息中无 AI 模型名。
- red/green：把 `writer.go` 还原为基线、保留新测试 → `import` 与 `preset_profile` 子测试 FAIL；应用修复 → 4 个子测试全部 PASS。
- `go test -count=1 ./...` 全部 ok；`gofmt -l .` 无输出；`go vet .` clean；`golangci-lint run .`（v2.5.0，以 `GOTOOLCHAIN=go1.26.7` 构建）仅 3 条基线已有 gofumpt 告警（color.go / get.go / terminal.go），改动文件无告警。
- 核实了 colorprofile `Writer.Write` 对 `Profile <= NoTTY`（含 Unknown）会 `ansi.Strip`，README 与 PR 正文对兼容性取舍的描述准确。仓库内无其他代码直接读取 `lipgloss.Writer`。
- 重查 issue #749：仍 open、0 评论、无 assignee、无关联 PR；最新 PR（#742–#748）均与本问题无关。
- 结论：修复针对 issue 的核心诉求（import 不再起 `tmux info` 子进程，Print*/Sprint* 首次使用时检测），风格与仓库一致；无需修改补丁。

