# open-nexus-OS/open-nexus-OS#47: add unit tests for the nxs-pack tool

| 项 | 值 |
|---|---|
| Issue | https://github.com/open-nexus-OS/open-nexus-OS/issues/47 |
| Tier | 自由 |
| Labels | area: tooling, good first issue, tests |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 19:58 UTC：`repo:open-nexus-OS/open-nexus-OS nxs-pack` → 0；issue 无评论、无 assignee、Development 为空 |
| AI 政策 | 欢迎 AI（仓库自带 CLAUDE.md/AGENTS.md 给 agent 用）；规则：**不要 `Co-authored-by` trailer**（CONTRIBUTING / git-workflow 明文）。commit 无任何 trailer |
| Base | `main` @ 9a81e5a |
| DCO / CLA | 无 DCO。**有 CLA**（cla-assistant GitHub Action，首个 PR 时机器人提示；在 PR 下评论 `I have read the CLA Document and I hereby sign the CLA` 即签，GitHub 登录即可，符合规则） |
| 需先认领 | **是**：issue 写 "To claim the issue, comment on it"。提交前先在 #47 评论认领（如 "I'd like to take this one, I have a patch with unit tests ready."），再开 PR |

## 问题理解
`nxs-pack`（把 `.nxb` bundle 打包成签名 `.nxs`）没有任何测试，header 写着 `TEST_COVERAGE: No tests`。issue 要求给纯 host 侧 helper 加 `#[cfg(test)]` 模块：`parse_args`、`parse_meta`/`req_str`/`opt_u64`、`parse_manifest`、`read_file_with_limit`、`sha256`，覆盖正常输入、缺字段、超大文件，用临时目录；之后更新 header。Done when：`cargo test -p nxs-pack` 通过。

## 改动
- `tools/nxs-pack/src/tests.rs`（新）：17 个测试；拒绝类用仓库惯用的 `test_reject_*` 命名。放单独文件是因为 structure-gate 对单个 .rs 有 600 行上限（main.rs 425 行，内联会逼近上限），`tools/nx` 也用 `mod tests;` 这种布局。
- `tools/nxs-pack/src/main.rs`：`parse_args` 改为调用 `parse_args_from(iter)`（只为可测，行为不变）；末尾 `#[cfg(test)] mod tests;`；header 的 TEST_COVERAGE 更新。
- `tools/nxs-pack/Cargo.toml` + `Cargo.lock`：dev-dependency `tempfile = "3"`（锁文件里本来就有，nxb-pack 同样用法；只多一行依赖引用）。
- 未改 CHANGELOG：仓库的 Unreleased 只记"关闭 task"级别的功能叙述，纯测试补充不需要（PR 里说明）。

## 验证
- `cargo test -p nxs-pack`：17 passed（原 0 个）
- 变异检验（相当于红→绿）：`>`→`>=` 限长、去掉 name trim、`n < 0`→`n < -1`、改 `--meta` 拼写，每个变异都有测试失败
- `cargo +nightly-2025-01-15 clippy -p nxs-pack --all-targets -- -D warnings` 干净；`cargo fmt --check --config-path config/rustfmt.toml` 干净；`scripts/check-structure.sh` PASS
- 未跑：`just check` 全套（本机无 just / cargo-deny）、`just diag-os`、QEMU（与 host 工具测试无关）

## 如何提交
1. 先在 issue #47 评论认领。
2. ```
   tools/submit_pr.sh contributions/248-open-nexus-OS-open-nexus-OS-47 open-nexus-OS/open-nexus-OS main test/nxs-pack-unit-tests contributions/248-open-nexus-OS-open-nexus-OS-47/pr_title.txt contributions/248-open-nexus-OS-open-nexus-OS-47/pr_body.md
   ```
   （不要加 `--signoff` 或 `--trailer`。）
3. CLA 机器人出现后，在 PR 下评论 `I have read the CLA Document and I hereby sign the CLA`。该 workflow 只在 `pull_request_target`（opened/edited/synchronize/reopened）触发，没有 issue_comment 触发器：评论后需**编辑一次 PR 描述**（触发 edited）让检查重跑，签名才会被记录。

## 独立复核（2026-10-22 20:10 UTC）
- 新克隆 main@9a81e5a，`git am` 干净；无任何 trailer。
- `cargo test -p nxs-pack` 17 passed（重复 5 次稳定）；clippy `-D warnings`、fmt（仓库 config）、structure-gate、仓库 `just lint` 同款参数、`just diag` 风格 check 全过。
- 复核者另做 10 个变异，全部被测试捕获。
- 竞争 PR：无；仓库 0 个 open PR。
- 采纳的措辞修正：sha256 向量说法（"" 不是 FIPS 180-2 示例）、TEST_COVERAGE 写成 "17 unit tests"、README 补 CLA 需编辑 PR 描述触发重跑。
- 结论：PASS。
