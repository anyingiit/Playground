# lacs-project/sysknife#567 — history --since 把截止时间向下取整到整小时

| 项 | 内容 |
|---|---|
| Issue | https://github.com/lacs-project/sysknife/issues/567 |
| Tier | 自由 |
| Labels | bug, help wanted, medium |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01 复核：Issue 处于 open，无 assignee，无 `claimed` 标签，无评论；`is:pr 567` 搜到 0 个结果，仓库没有 open PR |
| Base | `main` @ 603ca81 |

## 问题理解
CLI 用 `(now - epoch) / 3600` 把 `--since` 转成整小时，daemon 再按 `now - N hours` 过滤：30 分钟前会变成 0 小时，结果为空；90 分钟前会变成 1 小时，60–90 分钟之间的记录会丢失。

## 合理性判断
这是维护者自己提的 bug，标签为 help wanted / medium，给出的修复范围也很明确：传精确截止时间，保留 planner 用的 `since_hours`，CLI 的两个调用点都要改，比较前统一换算成 UTC，并补 20/75 分钟的测试。本 PR 按这个范围实现。

## 改动
- `transactions.rs`：新增 `HistorySince { Hours(u32), Cutoff(DateTime<Utc>) }`。SQLite 的 `Cutoff` 用 `julianday(created_at) >= julianday(?)` 比较（统一换算成 UTC）。
- `store.rs` / `store/postgres.rs`：trait 和两种实现都改为接收 `Option<HistorySince>`。Postgres 用 `created_at::timestamptz >= $n::timestamptz` 比较。
- `dispatcher.rs`：`query_history` 请求和 `ListJobHistory` 参数都新增 `since`（RFC 3339）。用 `resolve_history_since` 解析；`since` 和 `since_hours` 同时传入时报 `validation_failure`。
- CLI：`since_to_hours` 换成 `since_to_cutoff`（规范化为 UTC RFC 3339）。`run_history`、MCP `sysknife_history` 和 `client.query_history` 都改为发送 `since`。
- 测试：daemon 加 5 个，CLI 净增 1 个（删 5 个 `since_to_hours_*`，加 6 个 `since_to_cutoff_*`）；postgres 集成测试加 Cutoff 断言（本地没有 PG，属于 ignored）。

## 验证
- Red（在 main 上只加 dispatcher 测试）：`cargo test -p sysknife-daemon --lib -- since_keeps_sub_hour` 中 2 个失败（30 分钟截止返回 2 条而非 1 条；10 分钟截止仍列出 2 条）。
- Green：`cargo test -p sysknife-daemon --lib -- since cutoff` 8 个全部通过。
- `cargo fmt --all -- --check` 通过；`cargo clippy -p sysknife-daemon -p sysknife-cli --all-targets --locked -- -D warnings` 通过。
- `cargo test -p sysknife-cli --locked` 全部通过（295 + 22 + 2 + 4 + 3）。
- `cargo test -p sysknife-daemon --lib`：923 通过，5 个 watermark 测试失败。原因是这几个测试依赖进程级 `OnceLock`，需要 nextest 那样一个测试一个进程；用 `--exact` 单独跑都通过。
- daemon 集成测试：只有 `execute_spec::a_sigterm_ignoring_child...` 失败，在 main 上同样失败（沙箱环境问题）。postgres_store 6 个通过，5 个 ignored。
- `python3 scripts/check_evidence_claims.py` 通过。
- 未运行：`cargo nextest run --workspace` 和 `scripts/ci-local.sh`（没有 nextest，也没有 GUI 依赖库）。

## 需要提交者注意
- **先在 issue 里留言认领**：CONTRIBUTING 要求开工前在 thread 里说一声，维护者会加 `claimed` 标签。例如："I'd like to take this one, I have a fix with tests ready."
- AI 政策（CONTRIBUTING "Working with an AI assistant"）：允许使用，欢迎披露；要求作者**亲自通读 diff**，并且只写**实际跑过的**验证结果。PR body 中的数字都来自本地实际运行，请提交前自己读一遍 diff。
- DCO 不强制，所以没有加 Signed-off-by。
- **测试数量证据文件**：新增测试会改变 `tests/evidence/workspace-tests.json` 和 README 等 3 份文档里的数字。按 CONTRIBUTING 的 fallback 没有改动，PR 中已说明 +6，由维护者刷新。如果你本地有完整环境，可以运行 `UPDATE_TEST_BASELINE=1 scripts/test_baseline.sh`，并更新 3 份文档后追加一个 commit。
- CHANGELOG 一般由维护者自己记（例如 `docs(changelog): log #564`），所以没有改。
- 首个 PR 的 CI 需要维护者批准才会运行。

## 如何提交
```sh
git clone https://github.com/anyingiit/sysknife && cd sysknife   # 先 fork lacs-project/sysknife
git remote add upstream https://github.com/lacs-project/sysknife && git fetch upstream
git checkout -b fix/history-since-exact-cutoff upstream/main
git am /path/to/0001-fix-history-send-the-exact-since-cutoff-instead-of-w.patch
cargo test -p sysknife-daemon -p sysknife-cli --locked   # 可选复验
git push -u origin fix/history-since-exact-cutoff
gh pr create --repo lacs-project/sysknife --head anyingiit:fix/history-since-exact-cutoff \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

PR 标题和正文见 `pr_title.txt` / `pr_body.md`（按仓库自带的 PR 模板组织，并包含 motivation/disclosure 段落）。
