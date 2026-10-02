# astrid-runtime/astrid #476 — duplicate registration returns UnsupportedEntryPoint

| 项 | 值 |
|---|---|
| Issue | https://github.com/astrid-runtime/astrid/issues/476 |
| Tier | 新锐 |
| Labels | area/capsule, bug, good first issue, p3 |
| Status | ✅ ready（已通过独立复审）— patch + PR 文本已就绪（提交前需本人 sign-off，并先认领 issue，见下文） |
| 重复 PR 检查 | precheck 阶段（2026-10-01）：没有关联的 open/merged PR，issue 未分配，评论里没人认领。 |
| Base | `main` @ 6de3fd3b |

## 问题理解
`CapsuleRegistry` 遇到重复注册（同一 principal 的 view 里已经有同 ID 的 capsule，或 uplink ID 已经存在）时，返回的是 `CapsuleError::UnsupportedEntryPoint`。错误信息因此变成 `Unsupported entry point: Already registered: <id>`，调用方只能靠字符串匹配来识别重复注册。issue 还提到文档里写了并不存在的变体。

代码在 issue 提出后有变化：
- connector 已改名为 uplink，`register_connector` 变成了 `register_uplink`。
- 文档现在只写 "Returns an error when the principal already has a capsule with that ID"，不再提到不存在的变体。

主 bug 没有变化。

## 合理性判断
- issue 由维护者打了 bug、good first issue 标签，修法就是 issue 自己提出的方向：新增专用变体。
- 变体名用 `UplinkAlreadyRegistered`，而不是 issue 里写的 `ConnectorAlreadyRegistered`，因为后者的命名早于 connector→uplink 改名。PR 正文已经说明。
- `CapsuleError` 没有标 `#[non_exhaustive]`，所以新增变体只会破坏穷尽 match。grep 了整个 workspace，没有对 `CapsuleError` 的穷尽 match，也没有代码或测试按 "Already registered" 字符串做匹配。
- astrid-capsule 和 astrid-capsule-types 都不在 CONTRIBUTING 列出的 security-critical crates 里，新贡献者可以改。

## 改动
- `crates/astrid-capsule-types/src/error.rs`：新增 `AlreadyRegistered(String)`，`#[error("Already registered: {0}")]`；新增 `UplinkAlreadyRegistered(String)`，`#[error("Uplink already registered: {0}")]`。payload 只放 ID，显示文本与原来一致，只是去掉了误导性的前缀。
- `registry.rs`：`commit_reserved_runtime`、`validate_reserved_runtime`、`register_existing` 中的 3 处 capsule 重复检查和 2 处 uplink 重复检查改为返回新变体。
- `registry/uplinks.rs`（`register_uplink`）和 `registry/replacement.rs` 中的 3 处 uplink 重复检查改为返回新变体。
- `# Errors` 文档：`register`（原来没有这一节，新增）、`register_for`、`register_existing`、`register_uplink`、`register_owned_by_default` 都写明了新变体。
- **没改** `registry/compatibility.rs:35` 的 "already registered under a non-default system owner"：这是所有权冲突，不是 view 里的重复。PR 正文写明了，并表示维护者需要的话可以改。
- 在 `crates/astrid-capsule/src/registry_tests.rs` 末尾新增 3 个回归测试（复用该文件的 `MockCapsule`、`pid`、`test_hash`）。CI 对 `*_tests.rs` 的行数上限是 2000（源码 1000），registry_tests.rs 现在 1061 行，registry.rs 962 行，都在上限内。
- `changes/476.fixed.md`：changelog fragment，以 issue 号命名，与仓库现有 fragment 的做法一致，末尾写 "Closes #476"。

## 验证（rust 1.95.0，`CARGO_TARGET_DIR=/home/user/work/astrid/target`）
- Red：保留新变体和测试，只还原各处调用点，运行 `cargo test -j2 -p astrid-capsule --lib duplicate_register`，结果 3/3 FAILED，例如 `expected AlreadyRegistered, got UnsupportedEntryPoint("Already registered: dup-capsule")`，uplink 的测试同理。
- Green：
  - `cargo test -j2 -p astrid-capsule registry`：34 passed。
  - `cargo test -j2 -p astrid-capsule -p astrid-capsule-types`：全部通过，其中 lib 799 passed。
- `cargo clippy -j2 -p astrid-capsule -p astrid-capsule-types --all-targets -- -D warnings`：无警告。
- `cargo fmt --check`：通过。
- 没有跑 `cargo test --workspace`（机器资源有限）。新增变体只会影响穷尽 match，grep 确认 workspace 里没有。

## 独立复审（2026-10-01）
- 重新读了 issue，确认修复覆盖 issue 所述问题（connector 已改名 uplink）；重复 PR 检查仍无关联 PR。
- 复审发现：实现阶段把测试拆到单独的 `registry_duplicate_tests.rs` 并在注释里称是为了 1000 行上限，但 CI 对测试文件的上限是 2000 行，这个拆分没有必要且注释不准确。已把 3 个测试并回 `registry_tests.rs`，删除该文件，amend commit 并重新导出 patch。
- 亲自复验 red→green：只还原 `registry.rs` 和 `registry/` 下的调用点，`cargo test -j2 -p astrid-capsule --lib duplicate_register` 3/3 FAILED；恢复后 `cargo test -j2 -p astrid-capsule -p astrid-capsule-types` 全过（lib 799 passed），clippy `-D warnings` 干净，`cargo fmt --check` 通过。
- 在 base 6de3fd3b 的全新 worktree 上 `git am` 干净应用，结果 tree 与复审后的 commit 完全一致。
- 已知小点（未改，与 base 行为相同）：`register_owned_by_default` 在已存在同 hash 的 default-owned runtime 时走 `add_system_view`，即使该 view 已有此 capsule 也不会报 `AlreadyRegistered`；这是原有行为，原文档同样这么写，不在本 issue 范围。

## 需要提交者注意
- **新贡献者流程（必须）**：先在 #476 下评论认领，等维护者把 issue 分配给你之后再开 PR，否则 "Unsolicited PRs will be closed"。PR 还需要维护者加上 `newcomer-approved` label。
- **DCO（必须由你本人加）**：每个 commit 都需要 `Signed-off-by`，而且 CONTRIBUTING 明确要求 sign-off 是人的声明，"An AI or other tool must not add it on the contributor's behalf"。所以 patch 里**没有** Signed-off-by。请你本人在 `git am --signoff` 或 `git commit --amend -s` 之后再推送。sign-off 的邮箱必须和 commit author 一致。
- **AI 披露**：仓库允许工具辅助，但 PR 的 "AI / Tool Assistance" 一节必须写清工具、涉及范围、协助性质，以及你如何审阅和验证。pr_body.md 已经写好，带 `Assisted-by: Claude Code`。政策示例格式是 `TOOL: MODEL_VERSION`，按 brief 要求没写模型名；如果你愿意，可以自行补上。
- 维护者可能要求你讲解改动，或者现场回答 review 问题。请先通读 diff，理解为什么新增两个变体、为什么 compatibility.rs 那一处没改。
- 模板里的 checklist 已经全部勾选。最后一项（Signed-off-by）只有在你本人 sign-off 后才成立。CI 会拒绝有空节的 PR，pr_body.md 每一节都有内容。
- 分支建议：fork 后基于 main 新建 `fix/476-already-registered`。

## 如何提交
```bash
git clone https://github.com/<you>/astrid && cd astrid   # 先 fork
git remote add upstream https://github.com/astrid-runtime/astrid && git fetch upstream
git checkout -b fix/476-already-registered upstream/main
git am --signoff /home/user/Playground/contributions/113-astrid-runtime-astrid-476/0001-fix-capsule-return-dedicated-AlreadyRegistered-error.patch
cargo test -p astrid-capsule registry && cargo clippy -p astrid-capsule -p astrid-capsule-types --all-targets -- -D warnings && cargo fmt --check
```
或者在**认领并被分配之后**直接运行：
```bash
tools/submit_pr.sh contributions/113-astrid-runtime-astrid-476 astrid-runtime/astrid main fix/476-already-registered contributions/113-astrid-runtime-astrid-476/pr_title.txt contributions/113-astrid-runtime-astrid-476/pr_body.md --signoff
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
