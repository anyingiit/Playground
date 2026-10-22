# 431 — OpenCHAMI/ochami#206: document `smd iface add` and `delete` in ochami-smd(1)

| Item | Details |
|---|---|
| Issue | https://github.com/OpenCHAMI/ochami/issues/206 |
| Tier | Free |
| Labels | documentation, good first issue; milestone v0.11.0; opened by maintainer synackd on 2026-10-20 |
| Base branch | `main` (patch built on f187792) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments and no linked PR. None of the open PRs touch `man/`. |
| AI policy | None |
| CLA/DCO | DCO, already signed off |

## Change
- Added entries for `add` (4 forms) and `delete` (5 forms) to the iface section of `man/ochami-smd.1.sc`, following the format of the compep and rfe sections.

## Verification
- This is a documentation change, so there is no red→green test.
- `make man` (scdoc 1.11) builds cleanly. The base version also builds.
- In the generated `ochami-smd.1`, the iface section now lists add, delete and get.
- Every option and its short form was checked against `cmd/smd/iface/{add,delete}.go`:
  - add: -d, -D (default "Undescribed Ethernet Interface", mutually exclusive with -d), -f
  - delete: -a/--all, -d, -f, --no-confirm

## Findings (written up in the PR body as a possible follow-up)
- `iface add` only accepts a single network pair (PreRunE uses `len(args) != 3`), but its help and examples say multiple pairs are allowed.
- An argument without a comma makes it panic (index out of range).
- The man page documents the current behaviour, which is a single pair.

## How to submit
This is the 4th PR in the same repository (426, 427, 428, 431). It is best submitted after the first three, or once some of them have been merged.
```
git checkout -b docs-smd-iface-man origin/main && git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）

- 补丁：克隆 OpenCHAMI/ochami，origin/main = f187792，`git am` 干净应用；`git diff --check` 无空白问题。
- 议题 #206（WebFetch）：open，无评论、无关联 PR；要求的三点（delete 的三种目标指定方式、#170 的“只用 ID / 空白或路径式 ID 为用法错误”规则、不从 MACAddress 推导 ID）均已覆盖。
- 逐条对照代码：
  - `add`：-d/--data、-D/--description（默认 "Undescribed Ethernet Interface"，与 -d 互斥，实测 cobra 报错）、-f/--format-input（json/json-pretty/yaml，默认 json，见 `cli.AddFormatInputFlag`）；POST `/Inventory/EthernetInterfaces`（`PostEthernetInterfaces`）。
  - `delete`：-a/--all、-d、-f、--no-confirm（无短选项）；未加 --no-confirm 时提示确认；逐 ID 发送 DELETE `/Inventory/EthernetInterfaces/{id}`，--all 发送 DELETE 到集合端点；`CheckIDs`/`CheckPathSegment` 拒绝空白、"."、".."、含 "/" 的 ID（命令行在 PreRunE、payload 在发请求前）；只有 MACAddress 的 payload 项实测报 usage error（退出码 2），提示 "delete does not derive an ID from MACAddress"。
  - “需要访问令牌”与命令 Long 帮助及其他章节的写法一致。
- 格式：与 compep/rfe 一致（`++` 换行、Tab 缩进、*粗体*/_斜体_、选项按字母序），并补上了与其他章节一致的 "Subcommands for this command are as follows:"。
- `make man`（scdoc 1.11.2）构建无警告；生成的 man/ochami-smd.1 的 iface 小节依次列出 add、delete、get。
- PR 正文中的 follow-up：自行构建二进制，以 `--ignore-config --uri http://127.0.0.1:1 --token t` 复现：4 个参数报 "expected -d or >= 3 arguments ..., got 4"（退出码 2）；无逗号的网络参数在 `cmd/smd/iface/add.go:92` panic（index out of range [1] with length 1）。描述准确，作为“可选后续”放在正文中措辞克制、合适。
- 竞争 PR：8 个 open PR 中无涉及 man/、iface 或 #206 的（#61 只改 component add 示例，#216 只改 group/rfe add 代码）。
- 提交：作者 anyingiit <49945850+anyingiit@users.noreply.github.com>，有 Signed-off-by，无 AI 模型名，标题为 `docs(smd):` Conventional Commits 风格，含 Fixes #206。
- pr_body.md：前两行为 attribution 块，含 AI 协助披露段落，内容与代码和实测一致。

结论：PASS — 文档内容与代码逐条一致，构建干净，follow-up 已复现属实，无竞争 PR，提交与 PR 正文均符合要求；无需修改补丁。
