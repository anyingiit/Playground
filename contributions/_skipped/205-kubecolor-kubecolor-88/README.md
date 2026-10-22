# kubecolor/kubecolor#88 — Colorize `kubectl auth` commands（跳过）

| 项 | 值 |
|---|---|
| Issue | https://github.com/kubecolor/kubecolor/issues/88 |
| Labels | enhancement, good first issue |
| Status | ⏭️ skipped（2026-10-22）— 需要维护者的设计决策 / 维护者要求先做重构 |
| 检查基于 | `main` @ 151704c（含已合并的 #370） |

## 跳过原因
1. 维护者 applejag 在 #88 里说：`auth` 的难点是“子命令的子命令”需要不同的上色规则（`can-i` 输出 yes/no，`can-i --list` / `whoami` 是表格，`reconcile` 像 apply），kubecolor 目前不支持；不确定能否在不大改的情况下做到，大重构已计划在 #113（仍 open），“good first issue 标签可能贴错了”，只有能用小改动做时才应该做。
2. 之前的尝试 #234（semihbkgr，给 SubcommandInfo 加 SubcommandArgs 并做了 `auth can-i` 的 printer）被维护者关闭，理由原话大意：喜欢这个想法，但这个功能应该走更大的重构/重写，而不是在现有方案上打补丁，因为补丁引入了新 bug（review 里指出 flag 值解析的边界情况）。
3. 2024-11 有人（tzabbi）在评论里认领过，虽已过期，但加上 1、2 两点，现在再交一个 `auth` 嵌套子命令方案很可能重蹈 #234 覆辙。
4. 完整实现还需要新增 theme 键（can-i 的 yes/no 颜色、reconcile 的 verb 颜色），会牵涉配置文档（configdoc），同样需要维护者定方向。

## 可选的最小改动（未实现，供 owner 决定）
不依赖嵌套子命令解析的一小步：在 `printer/kubectl_output_colored_printer.go` 的 Apply/Create/... 那个分支里加上 `kubectl.Auth`，只对 `-o json` / `-o yaml` 使用 `JSONPrinter` / `YAMLPrinter`（覆盖 `auth whoami -o json|yaml`、`auth reconcile -o yaml`），其余仍单色。这只是 “Refs #88”，不能关闭 issue；是否值得提，建议先在 #88 问维护者。
