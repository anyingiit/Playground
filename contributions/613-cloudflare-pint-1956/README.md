# cloudflare/pint #1956 — alerts/for: option to disable default-value check

| 项 | 值 |
|---|---|
| Issue | https://github.com/cloudflare/pint/issues/1956 |
| Tier | 自由 |
| Labels | (none) |
| Status | ✅ ready — patch + PR text done |
| 重复 PR 检查 | 2026-10-01: /pulls?q=1956 无相关 PR（仅一个无关 dependabot PR）；issue 无评论、无指派、无关联 PR |
| AI 政策 | 仓库内无 AGENTS.md / CLAUDE.md / CONTRIBUTING，未发现 AI 相关限制；不要求 DCO |
| Base | `main` @ 373a5a2 |

## 问题理解
`alerts/for` 检查同时报告两类问题：`for`/`keep_firing_for` 非法值（Bug），以及显式写成默认值 `0` 的冗余字段（Information）。
issue 作者希望能单独关闭"默认值冗余"提示（团队习惯显式写 `for: 0m`），但保留非法值校验。目前只能整体禁用该检查。

## 合理性判断
合理：pint 已有同类先例 `check "promql/regexp" { smelly = false }`（检查级 settings 块，通过 `checks.SettingsKey` 注入 context）。本改动完全照搬该模式，默认行为不变。

## 改动
- `internal/checks/alerts_for.go`：新增 `AlertsForSettings{Redundant *bool}`（默认 true），`Check` 从 context 读取设置；`redundant=false` 时不报默认值。
- `internal/config/check.go`：`Decode()` 支持 `check "alerts/for"`。
- 测试：`internal/checks/alerts_for_test.go` 新增 4 个用例（+ `.snap`）；新增 testscript `cmd/pint/tests/0278_alerts_for_redundant_disabled.txt`（端到端：配置 `redundant=false`，`for: 0m`/`keep_firing_for: 0s` 不报，`for: -5m` 仍报 Bug）。
- 文档：`docs/checks/alerts/for.md` Configuration 章节；`docs/changelog.md` 新增 `v0.89.0 / Added`（v0.88.0 已发布）。

## 验证
（GOCACHE/GOMODCACHE 放在工作目录内）
- Red：把条件 `settings.redundantEnabled && value.Value == 0` 改回 `value.Value == 0` → `TestAlertsForCheck/default_for_value_/_redundant_disabled`、`.../default_keep_firing_for_value_/_redundant_disabled` FAIL；去掉 check.go/alerts_for.go 改动 → testscript 0278 FAIL（`unknown check "alerts/for"`）。
- Green：`go test -count=1 -run TestAlertsForCheck ./internal/checks/` ok；`go test -run TestScript/0278 ./cmd/pint` ok。
- `go test -race -count=1 -p 2 ./internal/checks/ ./internal/config/ ./cmd/pint/`：checks ok、config ok；cmd/pint 仅 `0228_watch_pidfile_remove_error` 失败 —— 在 base 分支上同样失败（环境以 root 运行，`chmod 000` 不生效），与本改动无关。
- `make format`：无改动；`make lint`：golangci-lint 0 issues，deadcode 无输出。
- 未跑：完整 `make test`（全仓库 `-race -count=3`），受限于共享 CPU。

## 需要提交者注意
- 仓库无 AI 政策、无 DCO 要求；PR 描述中已包含 AI 辅助披露段落。
- 选项名 `redundant` 是我选的（对应问题摘要 "redundant field with default value"），维护者可能希望换名，按 review 调整即可。
- changelog 新开了 `## v0.89.0` 小节；若提交时上游已有未发布小节，请合并进去（`git am` 冲突时手工处理）。
- PR 描述提到 0228 测试在 root 环境下失败；若你本地非 root 运行通过，可删除该说明。

## 如何提交
```bash
git clone https://github.com/anyingiit/pint && cd pint   # 先 fork cloudflare/pint
git checkout -b alerts-for-redundant-option origin/main
git am /path/to/0001-Add-redundant-option-to-alerts-for-check.patch
git push -u origin alerts-for-redundant-option
# 或：
tools/submit_pr.sh contributions/613-cloudflare-pint-1956 cloudflare/pint main alerts-for-redundant-option contributions/613-cloudflare-pint-1956/pr_title.txt contributions/613-cloudflare-pint-1956/pr_body.md
```

## PR
Title: 见 `pr_title.txt` — `Add redundant option to alerts/for check`
Body: 见 `pr_body.md`
