# 430 — curiousdannii/remglk-rs#18: glk_set_echo_line_event should not affect a pending line input request

| Item | Details |
|---|---|
| Issue | https://github.com/curiousdannii/remglk-rs/issues/18 (context: i7/extensions#187) |
| Tier | Free (Rust implementation of RemGlk, used by Parchment/emglken; maintainer curiousdannii) |
| Labels | bug, good first issue; opened by the maintainer on 2026-10-11 |
| Base branch | `master` (default branch; patch built on 6e52722) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments and no linked PR. |
| AI policy | None |
| CLA/DCO | None |

## Change
- A buffer window records the echo setting at the moment line input is requested (`line_input_echo`). `handle_line_input` uses that value, and `cancel` goes through the same path.
- New Glulx regression test `echolinetest`, with its `.inf` source, `.ulx` and `.regtest`, added to `runtests.sh`.

## Verification
- Red: the base version fails both checks.
- Green: with the fix, the full `tests/runtests.sh` passes (rc=0).
- `cargo clippy` shows no warnings.

## Notes for submission
- The patch contains a binary `.ulx` file (2 KB), generated with `git format-patch --binary`. `git am` restores it.
- The PR body explains how to compile it.

```
git clone https://github.com/curiousdannii/remglk-rs && cd remglk-rs && git checkout -b echo-line-event-pending origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）

- 克隆 curiousdannii/remglk-rs 到 /home/user/work/review430。默认分支是 `master`（不是 `main`），HEAD 为 6e52722。`git am` 应用补丁无冲突，`tests/echolinetest.ulx`（2048 字节，blob 64c4123）已正确还原。已把本 README 中的 `main` 更正为 `master`。
- 规范：Glk 0.7.5 §4.2 写明 "glk_set_echo_line_event() does not affect a pending line input request"，§3.5.4 写明该调用对文本网格窗口无效。补丁在 `request_line_event` 时把 `echo_line_input` 快照到 `BufferWindow.line_input_echo`，`handle_line_input` 使用该快照，符合规范。
- 各结束路径：输入到达（`handle_line_input`）和 `glk_cancel_line_event`（同样调用 `handle_line_input`）都使用请求时的值。关闭窗口时请求直接丢弃，不回显，不涉及该值。没有请求挂起时修改 echo 只改 `echo_line_input`，下一次请求会重新快照；`line_input_echo` 的 Default 值为 false，但每次使用前一定已被赋值，因此正确。
- 网格窗口：仍然总是回显，与规范一致。
- 其他读取点：grep 显示 `echo_line_input` 只在 `glk_set_echo_line_event` 和 `request_line_event` 中使用。GlkOte 协议（protocol.rs）不包含 echo 字段，回显完全在 remglk 端完成，也没有窗口序列化。没有遗漏的路径。
- 构建与测试：`cargo build` 成功。glulxe master 按 prepare.sh 的 sed 修改后编译通过。`./tests/runtests.sh` 全部通过，rc=0。
- 红测：只还原 remglk/src 后重新构建，并删除、重编 glulxe。echolinetest 失败：`<LiteralCheck "xyzzy">: not found` 和 `<LiteralCheck !"plugh">: inverse test should fail`，与 PR 描述一致。恢复补丁后转绿。
- `cargo clippy`：0 个警告。
- 测试程序：选择子 0x0150、0x00D0、0x00C0、0x0023、0x002F、0x0001 均正确。`@glk` 参数按倒序压栈，第一个参数在栈顶，顺序正确。window_open(0,0,0,3=TextBuffer,0) 正确，evtype_LineInput=3 正确，val1 是字符数。两个方向都覆盖了。
- 用 Inform 6.44 运行 `inform6 -G echolinetest.inf` 重新编译，结果与提交的 .ulx 逐字节一致。头部序列号为 261022（编译日期），换一天编译只会有这 6 个字节不同。
- "!plugh" 反向检查有意义：在回显关闭时，输入文本只可能通过回显出现在输出中；同时 "Read 5 characters." 证明输入确实被接收了。未修复时这项检查确实失败。
- 提交：作者 anyingiit <49945850+anyingiit@users.noreply.github.com>，没有 AI 模型名，标题 "Fix #18: ..." 与仓库的 "Fix #14: ..." 风格一致。
- pr_body.md：内容准确，前 2 行是署名块，包含 AI 辅助披露段落。
- 竞争 PR：仓库开放的 PR 只有 #16、#17（dfabulich，都与 echo 无关）。issue #18 没有评论，也没有关联的 PR。

结论：PASS。修复正确、范围最小，符合 Glk 规范。测试红/绿都已验证，.ulx 可由源码复现，提交和 PR 描述都合规。唯一需要的改动是 README 中的分支名（main→master），已修正，不需要改补丁。
