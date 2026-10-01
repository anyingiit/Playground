# pgdogdev/pgdog#1682 — RESET ALL in a multi-statement query panics the client's task

| 项 | 值 |
|---|---|
| Issue | https://github.com/pgdogdev/pgdog/issues/1682 |
| Tier | 新锐 |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文本已完成，红→绿已验证 |
| Base | `main` @ 80d6059（2026-10-01 复核：在 3151f93 上 git am 干净应用，红→绿复现） |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=1682` 0 结果；`is:pr RESET` 只有已合并的 #1655（RESET ALL 恢复启动参数，不同问题）；issue 无 assignee、无评论 |

## 问题理解
`try_multi_set()` 把除 `SET TRANSACTION` 以外的所有 `VariableSetStmt` 都交给 `parse_set_param()`，而后者遇到 `RESET ALL`（kind 5）或 `SET x FROM CURRENT` 会直接 `panic!`。Npgsql 在重置连接时发送的 `SET SESSION AUTHORIZATION DEFAULT;RESET ALL;CLOSE ALL;...` 会触发这个 panic。单条 `SET x FROM CURRENT` 走 `set()` 也会 panic。

## 合理性判断
这是明确的 bug（客户端任务 panic），issue 也给出了复现方法和建议方案（返回 MultiStatementSafety 错误）。仓库里有 AGENTS.md/CLAUDE.md，说明不排斥 AI 辅助；CONTRIBUTING 中没有禁止 AI 的条款。

## 改动（`pgdog/src/frontend/router/parser/query/set.rs`）
- 新增 `is_set_param()`（`VAR_SET_VALUE | VAR_SET_DEFAULT | VAR_RESET`）。
- `try_multi_set()` 只把这三类当作 SET param；`RESET ALL` 和 `FROM CURRENT` 算作“其他语句”，交给已有的 mixed-SET 逻辑处理（拆分执行或返回 `MultiStatementSafety`）。
- `set()` 对单条 `SET ... FROM CURRENT` 按 `SET TRANSACTION` 的方式直接转发给服务器。
- 测试：在 `query/test/test_set.rs` 中新增 `test_multi_statement_reset_all` 和 `test_set_from_current`。

## 验证
环境：`RUSTFLAGS="--cfg tokio_unstable"`（本机没有 mold，会覆盖 .cargo/config.toml 里的 linker 参数），本机没有装 cargo-nextest，所以用的是 cargo test。
- 红：未修复时运行 `cargo test -p pgdog --bin pgdog -- query::test::test_set::`，结果 16 passed、2 failed，两个新测试都以 `panicked at set.rs:42:13` 失败（即 issue 中的 panic）。
- 绿：同一命令全部通过（18/18）。
- 更大范围：`cargo test -p pgdog --bin pgdog -- router::parser --test-threads=1` 结果 760 passed、26 failed。逐个单独进程重跑这 26 个（和 nextest 每个测试一个进程的方式一致）后，25 个通过；剩下的 `sequence::test::test_sequence_setval_quoted_name_executes` 需要连接 Postgres（Connection refused），与本次改动无关。
- `cargo fmt --all -- --check` 通过；`cargo clippy -p pgdog --bin pgdog` 无警告。
- 没有运行：integration 测试（需要 Postgres/docker）。

## 需要提交者注意
- 仓库不要求 DCO，也不要求 AI trailer；commit 作者为 anyingiit（noreply 邮箱）。
- 仓库没有 PR 模板，PR body 采用 brief 规定的格式。
- CHANGELOG.md 对小修复通常不更新，因此没有改。

## 如何提交
```bash
git clone https://github.com/pgdogdev/pgdog && cd pgdog
git checkout -b fix-multi-statement-reset-all origin/main
git am /path/to/contributions/266-pgdogdev-pgdog-1682/0001-fix-parser-don-t-panic-on-RESET-ALL-SET-FROM-CURRENT.patch
# 或者直接用脚本：
tools/submit_pr.sh contributions/266-pgdogdev-pgdog-1682 pgdogdev/pgdog main fix-multi-statement-reset-all contributions/266-pgdogdev-pgdog-1682/pr_title.txt contributions/266-pgdogdev-pgdog-1682/pr_body.md
```
PR 标题：见 pr_title.txt；PR body：见 pr_body.md。
