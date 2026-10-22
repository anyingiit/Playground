# 391 — Gaurav-Gosain/tuios#980 copy mode 的 `^`/`$` 停在文本上

| 项 | 值 |
|---|---|
| Issue | https://github.com/Gaurav-Gosain/tuios/issues/980 |
| Tier | 新锐（2025 年创建，5.5k★，本月 +1.9k，测试很全） |
| Labels | 无 |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳其建议） |
| 重复 PR 检查 | 2026-10-22 20:40 UTC：issue 无评论、无 assignee、Development 空；`is:pr copy mode` 无相关开放 PR（#1020 是维护者的 go fix 现代化重构，可能轻微冲突） |
| AI 政策 | AGENTS.md 面向 agent；无禁止 AI 规定；维护者活跃合并外部 PR（104 个外部合并） |
| Base | `main` @ 9c8f0df |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
copy mode 里 `$`/行尾动作跳到窗格最右列（空白填充），`^` 等同 `0`。issue 要求：行尾停在最后一个文字字符，`^` 到第一个非空字符，保留 `0`/line_start 到第 0 列，并提供可绑定的 first-nonblank 和 text-end 动作。

## 改动
- helpers：`getCellAtCol`、`firstNonBlankCol`、`lastTextCol`（支持 scrollback 行、宽字符、空行）。
- handlers：normal/visual 的 `^`、`$`，以及 `copy_mode_line_end`、新增 `copy_mode_first_nonblank` 动作。
- config：新动作常量、描述、help 行；仿照 `hold_window_mode`，无默认键（不放进默认 map），reachability 测试的 handled 集合里加上它。
- 测试：新文件 `copymode_line_motion_test.go`；修改 `TestCopyModeBorderlessMotionReachesLastRow` 中一处 `$` 断言（改为 `l` 走到最右列）。
- 文档：`docs/KEYBINDINGS.md`。

## 验证
- 红：回退 handlers/helpers → 新测试失败（`^`→0、`$`→77、动作不运行）；绿：全部通过
- `go test ./internal/input/ ./internal/config/ ./internal/app/ ./cmd/tuios/ -count=1` 全过（复核建议采纳后重跑）；`go vet`、`gofmt -l` 干净
- 未跑 e2e/tui 与 ghostty 后端测试
- 独立复核 agent：VERDICT PASS；采纳两条建议（新动作加描述 + reachability 豁免，按 hold_window_mode 的先例；补 scrollback 行测试）

## 需要提交者注意
- 提交信息用 Conventional Commits（`fix(input): …`），已照做。
- PR 模板是仓库自己的 `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`，pr_body.md 已按其章节填写并加入披露段落。
- 如果维护者的 #1020（go fix 现代化）先合并，可能需要 rebase。

## 如何提交
```
git clone https://github.com/Gaurav-Gosain/tuios && cd tuios
git checkout -b copy-mode-text-line-motions origin/main
git am /path/to/0001-fix-input-stop-copy-mode-s-and-on-the-line-s-text.patch
```
