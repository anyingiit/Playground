# 392 — Gaurav-Gosain/tuios#585 review 面板的 `]` `[` `}` `{` 可绑定

| 项 | 值 |
|---|---|
| Issue | https://github.com/Gaurav-Gosain/tuios/issues/585 |
| Tier | 新锐（同 391） |
| Labels | 无 |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳测试建议） |
| 重复 PR 检查 | 2026-10-22 21:00 UTC：issue 无评论、无 assignee、Development 空；维护者在 #575 说"单独跟踪"，未表示自己做；无相关开放 PR |
| AI 政策 | 同 391，无禁止 |
| Base | `main` @ 9c8f0df |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
review 面板的 hunk/文件跳转键硬编码；AZERTY Mac 上需 Option，和 tuios 的 Alt 冲突。要求像其他键位一样可在 config 绑定，并出现在 `tuios keybinds` / `keybinds explain`。

## 改动
新增 `[keybindings.review]` 段（review_next_hunk / prev_hunk / next_file / prev_file，默认 `]` `[` `}` `{`），按 transfers/copy_mode 的方式全部接线（默认值、旧配置补默认、校验、scope、registry、描述）；review_input 先查绑定再走自身按键；页脚提示与帮助面板读绑定键；文档加 AZERTY 示例。

## 验证
- 红：回退 review_input.go → reachability 的 8 个 review 子测试和重绑定测试失败；绿：全过
- `go test ./internal/input/ ./internal/config/ ./internal/app/ ./cmd/tuios/ -count=1` 全过；`go vet`、`gofmt` 干净
- 实测二进制：`tuios keybinds list` 有 Review 表，`keybinds explain ']'` 显示 `Review: next hunk… [review]`
- 未跑 e2e/tui
- 独立复核 PASS；采纳"补编辑器内 `]` 仍为文本"的测试；"冲突键 doctor 警告"未做，在 PR 里提出可后续补

## 需要提交者注意
- 391 和 392 是同仓库两个独立 PR，都基于 main；单独打都没问题，但两者在 registry.go 的 ActionDescriptions 相邻行冲突。若 391 已合并（或 392 要叠在 391 分支上），改用 `alt-0001-on-top-of-391.patch`（已解决冲突并跑过 input/config 测试）。
- PR 模板同 391。

## 如何提交
```
git clone https://github.com/Gaurav-Gosain/tuios && cd tuios
git checkout -b review-keys-bindable origin/main
git am /path/to/0001-feat-review-bind-the-review-overlay-s-hunk-and-file-.patch
```
