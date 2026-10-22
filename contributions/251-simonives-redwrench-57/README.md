# simonives/redwrench#57: no_tier_rule_has_an_empty_description test skips the Developer tier

| 项 | 值 |
|---|---|
| Issue | https://github.com/simonives/redwrench/issues/57 |
| Tier | 自由（Rust，MCP 服务器，单人维护） |
| Labels | bug, good first issue, priority: low（milestone v1.1） |
| Status | ✅ ready，独立复核 PASS（未提交） |
| 重复 PR 检查 | 2026-10-22 20:45 UTC：仓库所有非 owner PR 都是 dependabot，无人做过 #57；issue 无评论、无 assignee、Development 为空 |
| AI 政策 | 仓库有 AGENTS.md/CLAUDE.md（面向 AI agent 的指引），维护者自己也用 agent；无禁 AI 条款 |
| Base | `main` @ ed406f2 |
| DCO / CLA | 均无（CONTRIBUTING：贡献按 MIT + Apache-2.0 双许可） |
| 需先认领 | 否 |
| 说明 | 改动很小（只改测试，6+/1-）。仓库此前没有外部人类贡献，维护者可能自己顺手修；价值低但被明确邀请，成本极小 |

## 问题理解
测试 `no_tier_rule_has_an_empty_description` 写于 Developer 层出现之前，只遍历 Safe/Standard/Unrestricted，Developer 层 9 条 `DEVELOPER_TOOLS` 规则从未被检查。

## 改动
`src/policy/tiers.rs` 测试数组加 `TierName::Developer`（rustfmt 后展开成多行），与 issue 给的修法一致。

## 验证
- 新测试通过（所有 Developer 规则本来就有描述）。
- 变异：把 `developer_rules()` 里 allow 的描述改成空白，新测试失败，原测试仍通过，说明覆盖确实生效。
- `cargo test`：lib 158 过 5 失败，失败的 5 个是提权降级测试（`run_as_*`、`dispatch_drops_privilege_*`），需要 Fedora/非 root 环境，未打补丁的 main 上一样失败。PR 正文里如实写了，并且没有勾 `cargo test` 那一项。
- clippy `-D warnings` 干净，`cargo fmt --check` 干净。

## 如何提交
`tools/submit_pr.sh <本目录> simonives/redwrench main test/57-developer-tier-descriptions pr_title.txt pr_body.md`（加 `--trailer`：维护者自己的 commit 带 AI Co-Authored-By，用 Assisted-by 与正文披露一致；不加 `--signoff`）

## 独立复核（2026-10-22 20:55 UTC）
PASS。复核者在新克隆上确认：补丁可干净应用；lib 158 过 / 5 败 / 1 忽略，与 main 完全相同；clippy、fmt 干净；变异结论成立（报错命令为 'bash'）。其他 `[Safe, Standard]` 循环是层级专属测试，不是同类 bug。已采纳：`src/policy/` 勾选项保留模板原文、改为未勾并注明 N/A；变异说明移到测试清单下；测试数补上 "1 ignored"；提交时加 `--trailer`。
