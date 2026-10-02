# getsotto/sotto #393 — CLI: reject out-of-range machine-token lifetimes before local setup

| 项 | 值 |
|---|---|
| Issue | https://github.com/getsotto/sotto/issues/393 |
| Tier | 新锐 |
| Labels | bug, good first issue, help wanted |
| Status | ✅ ready — patch + PR text done, all checks green |
| Base | `main` @ 452c390 (feat: add bounded Stripe coverage reads (#396)) |
| Duplicate-PR check | 2026-09-24 开工前 + 完成前各查一次：`is:pr 393` → 0；`is:pr expires` / `is:pr token lifetime` → 只有已合并的 #383（引入该 flag 的特性 PR）；issue 无 assignee、无评论、无关联 PR |
| AI 政策 | 仓库 CONTRIBUTING / .github / docs 中未发现 AI/LLM/Copilot/agent 相关限制（已 grep），无 AGENTS.md/CLAUDE.md |

## 为什么符合“新锐”
- 31 stars / 41 forks，Rust，端到端加密的团队 secret 同步工具（CLI + Axum server + WASM 浏览器端），781 commits，Apache-2.0，文档完整（威胁模型、安全审计范围）。
- 本周非常活跃：2026-09-24 当天合并了多个不同的人类贡献者的 PR（维护者 Maxerns，外部贡献者 cyncui、TayfurYldz 等），另有多个打开中的外部 PR。不是 issue-farm：issue 由维护者撰写，带精确复现和验收标准。

## 问题理解
`sotto token create --expires-in-days <N>` 的 clap 定义是裸 `Option<u32>`，所以 0、366、4294967295 在解析阶段都能通过；之后命令进入本地初始化（打开/创建 `store.db`、查找 `sotto.toml`），在项目外运行时报 "no sotto.toml found"（退出码 3）并留下 store.db，用户看不到真正的问题（服务端只接受 1–365 天，见 `crates/server/src/machine.rs` 的 `MAX_LIFETIME_DAYS = 365`）。

## 合理性判断
- 由维护者提出，标注 good first issue/help wanted，有明确验收标准。
- 仓库已有完全相同的模式：`share --views/--expire` 用 `clap::value_parser!(..).range(..)` + `sotto_cli::remote::share::MAX_*` 常量在解析期拒绝，并有 "rejected before local setup" 进程级测试（`crates/cli/tests/share_cli.rs`）。本改动完全照此模式。
- 服务端校验保持不变（仍是权威校验）。

## 改动
- `crates/cli/src/remote/machine.rs`: 新增 `pub const MAX_LIFETIME_DAYS: u32 = 365;`（带注释说明与服务端一致、服务端仍权威）。
- `crates/cli/src/main.rs`: `TokenCommand::Create.expires_in_days` 加 `value_parser = clap::value_parser!(u32).range(1..=MAX_LIFETIME_DAYS as i64)`；help 文案改为 "Days until the token stops working (1-365; the server defaults to 90)."；新增单元测试 `token_lifetime_parses_bounds_and_rejects_out_of_range_values_before_setup`（1/365 可解析，0/366/4294967295/-1 报错且含 `--expires-in-days` 与 `1..=365`，省略 flag 为 None）。
- `crates/cli/tests/share_cli.rs`: 新增进程级测试 `invalid_token_lifetimes_are_rejected_before_local_setup`（`--plain token create --expires-in-days 0|366|4294967295` → 退出码 2，stderr 含 flag 与范围、不含 sotto.toml，且 `SOTTO_DATA_DIR` 未被创建）。

## 验证
- Red（仅加测试和常量、未加 value_parser）：
  - `cargo test -p sotto-cli --bin sotto token_lifetime` → FAILED: `accepted --expires-in-days=0`
  - `cargo test -p sotto-cli --test share_cli token_lifetime` → FAILED: `assertion left == right failed: accepted 0`（实际退出码 3）
- Green（加 fix 后）：两者均 ok。
- 全量（CI 相关子集）：
  - `cargo fmt --all --check` → OK
  - `cargo clippy -p sotto-cli --all-targets -- -D warnings` → OK（会同时检查 dev-dep sotto-server）
  - `cargo test -p sotto-cli` → lib 136 passed，bin 25 passed，e2e 5 passed（DB-gated，未设置 SOTTO_RUN_DB_TESTS/DATABASE_URL 所以实际跳过），share_cli 9 passed，spinner 6 passed，theme_cli 7 passed，0 failed
  - 未运行：workspace 级 clippy/test 的 core/server/wasm 部分、web/npm、Postgres e2e、cargo-deny/audit（改动只涉及 CLI 参数解析，无依赖变化）。
- 手动：项目外 `sotto --plain token create --expires-in-days 0|366|4294967295` → `error: invalid value '0' for '--expires-in-days <EXPIRES_IN_DAYS>': 0 is not in 1..=365`，不创建 store.db；1 和 365 仍进入原有流程（报缺少 sotto.toml，创建 store.db，与 issue 描述的有效值行为一致）。

## 需要提交者注意
- **DCO 必需**：CONTRIBUTING 与 PR 模板要求每个 commit 都有 `Signed-off-by`，issue 也要求 signed commits。patch 中**未**加 sign-off，请提交者自己：`git am 0001-fix-cli-reject-out-of-range-token-lifetimes-before-l.patch && git commit --amend -s --no-edit`。
- PR 模板是仓库自己的简短格式（Summary / Closes / Tests / DCO 勾选），下面的 PR body 把它们合并进了统一格式。
- 文案规范：英式英语、不用 em dash（已遵守）。
- 仓库未发现关于 AI 生成贡献的限制；PR 中有披露段落。

## 如何提交
```sh
git clone https://github.com/<you>/sotto && cd sotto   # fork of getsotto/sotto
git checkout -b fix/token-lifetime-range-393 origin/main
git am /path/to/0001-fix-cli-reject-out-of-range-token-lifetimes-before-l.patch
git commit --amend -s --no-edit     # DCO sign-off
git push -u origin fix/token-lifetime-range-393
```

## PR title
fix(cli): reject out-of-range token lifetimes before local setup

## PR body
```markdown
## Description

Summary: bound `sotto token create --expires-in-days` to 1..=365 at argument parsing, so invalid lifetimes are rejected before any local setup.

`--expires-in-days` was a bare `Option<u32>`, so 0, 366 and 4294967295 parsed fine and the command went on to open/create the local store and look for `sotto.toml`. Outside a project that meant exit code 3 with "no sotto.toml found" (and a fresh `store.db`) instead of an explanation of the lifetime limit.

This follows the existing pattern used for `share --views/--expire`:

- `crates/cli/src/remote/machine.rs`: new `pub const MAX_LIFETIME_DAYS: u32 = 365`, mirroring the server's limit. The server still validates the lifetime authoritatively; this only moves the obvious rejection earlier.
- `crates/cli/src/main.rs`: `value_parser = clap::value_parser!(u32).range(1..=MAX_LIFETIME_DAYS)` on the flag, and the help text now reads "Days until the token stops working (1-365; the server defaults to 90)." Omitting the flag still sends no lifetime, so the server default applies.

Now:

```
$ sotto --plain token create --expires-in-days 366
error: invalid value '366' for '--expires-in-days <EXPIRES_IN_DAYS>': 366 is not in 1..=365
```
(exit code 2, no local store created)

Tests:
- Parser test `token_lifetime_parses_bounds_and_rejects_out_of_range_values_before_setup`: 1 and 365 parse, 0 / 366 / 4294967295 / -1 are rejected with the flag name and `1..=365`, and omitting the flag gives `None`.
- Process test `invalid_token_lifetimes_are_rejected_before_local_setup` in `tests/share_cli.rs`: exit code 2, the diagnostic names the flag and range, it never mentions `sotto.toml`, and `SOTTO_DATA_DIR` is not created.

Both new tests fail on `main` (`accepted --expires-in-days=0`; process exits 3) and pass with the change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #393

## Checklist

- [x] Tests pass locally (`cargo fmt --all --check` ✔; `cargo clippy -p sotto-cli --all-targets -- -D warnings` ✔; `cargo test -p sotto-cli` ✔ - lib 136, bin 25, share_cli 9, spinner 6, theme_cli 7 passed; the DB-gated e2e tests were not enabled locally)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [x] Documentation is updated (if applicable) — the flag's `--help` text now states the 1-365 range
- [x] I signed off every commit (`git commit -s` / Developer Certificate of Origin).
```
