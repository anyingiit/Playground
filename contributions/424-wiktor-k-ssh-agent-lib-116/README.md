# 424 — wiktor-k/ssh-agent-lib#116: switch documentation references to RFC 9987

| Item | Detail |
|---|---|
| Issue | https://github.com/wiktor-k/ssh-agent-lib/issues/116 |
| Tier | Free (Rust SSH agent library; the maintainer is active and merged #114 recently) |
| Labels | good first issue, pr welcome (added by maintainer wiktor-k on 2026-09-15) |
| Base branch | `main` (patch built on 3114e4e) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments, no assignee and no linked PR. The 3 open PRs (#113, #111, #87) are unrelated. |
| AI policy | None |
| CLA/DCO | DCO required. The patch already carries `Signed-off-by: anyingiit`. No CLA. |

## Change
- 12 files, 24+/23−, documentation and comments only.
- Draft-14 § 3.x links become RFC 9987 § 5.x links.
- Fixed the session-bind label (8.8.1 → 8.1.1).
- Fixed the wrong citation in the unknown_request test (§ 4.1 → § 5.1, wording updated to the RFC).
- The constraint decoder comment now cites § 8.2 instead of draft-12.
- The README link now points at the RFC.

## Implementation check (written up in the PR body, not fixed in this patch)
- An unknown key constraint type makes `handle_socket` close the connection instead of replying `SSH_AGENT_FAILURE`. RFC 9987 § 5.2.7 requires that reply with a MUST, and draft-14 already did.
- A throw-away test confirmed it: the response is None and the follow-up request also gets None.
- The fix involves a design choice (the error type or a new variant). The PR offers it as a follow-up and uses `Refs #116` so the issue stays open.

## Verification
- This is a documentation change, so a red→green test doesn't apply. The checks were run instead:
  - `cargo test --all`: all passed.
  - clippy `-D warnings`: clean.
  - codespell on the tree and on the commit message: clean.
  - stable `cargo fmt --check`: clean.
  - `cargo doc`: no new warnings. The only warning is the existing one at agent.rs:269.
- Every link anchor was checked against the section numbers in rfc9987.txt.

## How to submit
```
git clone https://github.com/wiktor-k/ssh-agent-lib && cd ssh-agent-lib && git checkout -b docs-rfc9987 origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）

- **应用补丁**：全新克隆 `wiktor-k/ssh-agent-lib`（main = 3114e4e），`git am` 干净应用，共 12 个文件，24+/23−，只改文档和注释。
- **议题核对**：已用 WebFetch 查看 #116。议题有两项要求：文档改为引用 RFC 9987，并对照 RFC 复查实现。议题没有评论、没有指派人、也没有关联 PR。补丁用 `Refs #116`，议题会保持打开，符合"只完成第一项"的情况。
- **逐条核对链接**（对照 rfc9987.txt 和 draft14.txt）：
  - draft § 3 / 3.2 / 3.2.6 / 3.2.7.3 / 3.4 / 3.5 / 3.6 / 3.6.1 / 3.8 / 3.8.1 分别对应 RFC § 5 / 5.2 / 5.2.6 / 5.2.7.3 / 5.4 / 5.5 / 5.6 / 5.6.1 / 5.8 / 5.8.1。标题和内容一一对应，锚点格式 `#section-x.y` 正确。
  - 原来引用 draft § 4.1 是错的（那一节是 "Advertising agent forwarding support"）。改成 RFC § 5.1（Generic Agent Responses）正确，引文与 RFC 原文逐字一致。
  - 会话绑定链接的标签从 § 8.8.1 改为 § 8.1.1（Reserved Message Type Numbers），与 URL 一致，正确。
  - 约束解码器注释从 draft-12 § 5.2 改为 RFC § 8.2（Constraint Identifiers），正确。
  - README 链接已指向 rfc-editor。
- **残留引用**：`grep -rn draft-miller` 无结果，也没有 `ietf.org/archive`、`datatracker` 或 "Internet Draft" 的残留。已有的 RFC9987 § 8.1 / 9.2 / 5.1 引用也核对过，均正确。OpenSSH `PROTOCOL.agent` 的链接本来就是固定 commit 的引用，不属于过时引用。
- **检查**（CARGO_TARGET_DIR=/home/user/work/ssh-target）：
  - `cargo test --all` 全部通过；
  - clippy `-D warnings` 干净；
  - `uvx codespell --config .codespellrc` 对代码树和提交信息都干净；
  - `cargo fmt --all -- --check` 退出码为 0；
  - `cargo doc` 只有 agent.rs:269 这一条已有警告，与 PR 描述一致。
- **独立验证 PR 中的实现问题**：
  - 写了一个一次性测试，参照 tests/unknown_request.rs，用 `listen` 起 TCP agent。
  - 对照组：原样发送 `req-add-identity-constrained-lifetime.bin`，返回 `[6]`（SUCCESS）。
  - 把约束类型字节 1 改成 3 后：没有任何响应，连接被关闭（0.1 秒内，不是超时）。在同一连接上接着发 RequestIdentities，也是 None。
  - 测试已删除。
  - 结论：PR 描述准确。RFC 9987 § 5.2.7 要求必须回复 SSH_AGENT_FAILURE（MUST），draft-14 § 3.2.7 也有同样的 MUST。
  - 此外核实了：未知请求类型和 Session 默认未实现的请求，都经 `UnsupportedCommand` 走到 `Response::Failure`，符合 § 5.1。
- **额外观察**（同一机制，不需要改补丁，可作为后续 PR 的素材）：
  - 已知类型的请求只要消息体解码失败（例如截断或格式错误），也会经 codec 错误直接断开连接，而不是回复 FAILURE。
  - RFC § 5.1 的 "On failure, the agent MUST reply with SSH_AGENT_FAILURE" 也可以覆盖这种情况。
  - 修复未知约束时可以一并考虑。
- **提交检查**：
  - 作者和 Signed-off-by 都是 `anyingiit <49945850+anyingiit@users.noreply.github.com>`；
  - 提交信息中没有 AI 模型名或 Co-authored-by；
  - 标题采用祈使句、首字母大写、不加前缀，与仓库近期的提交风格一致（如 "Update and document `Request::Unknown` variant"）。
- **pr_body.md 检查**：
  - 英文；
  - 前两行是署名块；
  - 有 AI 协助披露段落；
  - 对实现问题的描述准确，没有夸大，明确写了"不在本 PR 修复"；
  - 测试结论与我复现的结果一致。
  - 不需要修改。

结论：PASS。补丁只改文档，所有章节号和锚点都正确，没有残留的 draft 引用，四项检查全部通过。PR 描述中关于"未知约束类型直接断开连接"的说法已独立复现确认，描述准确，没有夸大。提交签名和风格都符合要求。
