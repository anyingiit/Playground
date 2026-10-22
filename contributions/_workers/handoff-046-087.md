# 交接：第二轮 046–087（2026-10-22 19:05 UTC）

本轮没有新开 PR（按调度要求在开 PR 前停下）。截止 2026-10-23 01:00 UTC。

## 已提交（共 20 个，均已写入 SUBMISSIONS.md / submissions.json）
- 10-02 提交的 19 个：046 049 052 054 056 057 059 060 061 062 065 066 067 068 069 071 072 074 082
- 086 orium/rpds#117（旧会话 10-22 18:46 开出）

## 已跳过（11 个，已移到 `_skipped/`，README 顶部写了原因）
- issue 已修复关闭：047 050 051 055 073 077 079 085
- 有竞争 PR：063（go-smtp#320）、075（plotly.py#5825）、080（parquet-go#615）

## 待提交（11 个）
补丁都已在 2026-10-22 的上游默认分支上验证能打上；需要重新移植的已把 `0001-*.patch` 换成新版本（旧版在 git 历史里）。

| # | 上游 | 补丁 | 测试（在最新上游上） | 下一步 |
|---|---|---|---|---|
| 058 | arxanas/git-branchless (master) | 原补丁可直接打上 | 未重跑 | 跑 `cargo test -p git-branchless-revset` 后提交 |
| 064 | GREsau/schemars (master) | 原补丁 | ✅ 红（4 个 default:: 失败）→ 绿（5/5） | 可直接提交 |
| 076 | gkampitakis/go-snaps (main) | 原补丁 | 绿：snaps 包 11 个 TestSummary/TestDiff 失败，与 base 完全相同（环境颜色输出导致），新测试通过 | 可提交 |
| 078 | image-rs/image-png (master) | 原补丁 | 未重跑 | 跑 `cargo test --workspace --all-targets` 后提交 |
| 087 | jnsahaj/lumen (main) | 原补丁 | ✅ 绿 `cargo test --locked --bin lumen php` 2 passed；红在跑（去掉 highlight/config.rs、mod.rs、Cargo.*） | 看红结果后提交 |
| 053 | zerobrewhq/zerobrew (main) | **已更新**：CHANGELOG 冲突，条目改放到 Unreleased 新 `### Fixed` | ❌ 未测：上游要求 rustc 1.96，本机 Homebrew rustc 1.94 | 需要新版 rustc（不要改系统 brew 的话可用 rustup 装到独立目录）后跑 `cargo test -p zb_cli --lib cli::tests`；红法见 README |
| 083 | cloudflare/pint (main) | **已更新**：changelog 版本改为 `## v0.90.0`（上游已到 v0.89.4） | ✅ 红→绿（TestAlertsForCheck；testscript 0278 ok；config ok）。`./internal/checks` 全量有失败，与 base 对比还在跑 | 确认与 base 一致后提交 |
| 070 | typstyle-rs/typstyle (master，旧名 Enter-tainer) | **已更新**：markup.rs 重新移植（上游新增了文档注释）、CHANGELOG 条目放到 Unreleased 并加 #478 链接 | 在跑：红→绿 `cargo test -p typstyle-tests --test tests -- list-indent-tab4` + 全量 `--skip e2e` | 看结果后提交 |
| 081 | samber/ro (main) | **已更新**：测试插到 TestOperatorFilterDistinctBy 之后；docs/data 的 sourceRef 行号按新插入的 25 行重新平移（L>138 的 +25） | ✅ 红（undefined: NotZero）→ 绿；`go test -race .` 与 base 一致（0 失败；首次跑有一次偶发失败）；`go vet` 的 lostcancel 是 base 已有 | 可提交 |
| 048 | DeusData/codebase-memory-mcp (main) | **已更新**：采用旧会话的重新移植（http_server.c 已重构，计数先存局部变量） | ❌ 未测 | 跑 `make -f Makefile.cbm -j2 test-focused TEST_SUITES=httpd`，红（只留测试）→ 绿后提交 |
| 084 | agavra/tuicr (main) | 原补丁冲突：AGENTS.md、src/forge/pr_open.rs、src/vcs/diff_parser.rs | 未开始 | 需要重新移植并重跑测试 |

## 本地路径（本机）
- 记录克隆：`~/Workspace/_contrib_clones/pg-046-087`（分支 claude/serene-hamilton-br3vum）
- 上游克隆（已应用补丁、已提交到本地 HEAD）：`/private/tmp/claude-501/-Users-user-laptop-Workspace/82c2edb2-bd9c-4548-94e1-5939e262c43a/scratchpad/chk/<编号>`；base 对比用的 worktree 在同目录 `base076`、`base081`、`base083`
- 测试日志：同 scratchpad 下 `rg_batch1.log`、`rg_batch2b.log`、`rg_070.log`、`rg_081.log`、`base_cmp.log`

## 注意
- Go 用 `GOTOOLCHAIN=go1.27.0`（本机 /usr/local/go 是 1.22，pint 要求 ≥1.27）。
- `tools/submit_pr.sh` 的 folder/title/body 参数用绝对路径（脚本会 cd）。typstyle 提交用 `typstyle-rs/typstyle`。
- 每次提交前 `gh search prs --author anyingiit` + `gh pr list -R <repo> --author anyingiit --state all` 去重（搜索索引有延迟，后者更可靠）。
