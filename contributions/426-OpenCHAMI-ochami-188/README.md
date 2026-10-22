# 426 — OpenCHAMI/ochami#188: metadata delete prompts for confirmation first

| Item | Details |
|---|---|
| Issue | https://github.com/OpenCHAMI/ochami/issues/188 |
| Tier | Free (OpenCHAMI is an HPC system-management project under LF Projects; maintainer synackd is very active) |
| Labels | bug, good first issue; milestone v0.11.0; opened 2026-10-07 by maintainer synackd |
| Base branch | `main` (patch built on f187792) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments, no assignee and no linked PR. None of the 5 open PRs (#213, #182, #103, #61, #42) touches `cmd/metadata` or `cmd/prompts_test.go` (checked the file lists of #213 and #61; #182 is a single BSS-client test file, +467/−0). |
| AI policy | None |
| CLA/DCO | DCO; the patch already has the Signed-off-by line. CI may also check commit signatures (see AUDIT). |

## Change
- In the 4 `cmd/metadata/*/delete.go` files, the prompt now comes before `GetClient` and `HandleToken`, following the same pattern as `boot bmc delete`.
- Added 4 test cases.

## Verification
- Red: all 4 new cases fail. Green: they pass.
- `go test ./...` passes, and golangci-lint v2.15.0 reports 0 issues.
- Manual check with the binary: answering n exits with 8; `--no-confirm` exits with 3 when no URI is configured.

## How to submit
```
git clone https://github.com/OpenCHAMI/ochami && cd ochami && git checkout -b fix-metadata-delete-confirm origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）

- **基线**：全新克隆 OpenCHAMI/ochami，origin/main 仍为 `f187792`；`git am` 干净应用。作者 `anyingiit <49945850+anyingiit@users.noreply.github.com>`，Signed-off-by 与作者一致。
- **代码**：4 个 `cmd/metadata/*/delete.go` 改动后，与 `cmd/boot/bmc/delete.go` 逐行同构：先 prompt（`CodeGeneric` / `CodeDeclined`），再 `GetClient`，再 `HandleToken`，注释措辞一致；`runCore*` 去掉 client 参数，全仓库无其他调用者；删除的 `pkg/client/metadata_service` import 确已无用（`go vet`、gofmt、lint 均无告警）。`--no-confirm` 路径：跳过 prompt，直接取 client 和 token。
- **范围外扫描**：仓库内所有调用 `LoopYesNo` 的 15 个文件（全部是 delete 命令）在打补丁后都是先 prompt、后取 client 和 token，每个文件只调用一次 `GetClient`。`config cluster delete` 不提示也不建 client，不受影响。其他 metadata 命令不提示，不存在同类问题。
- **Red→green**：只把 `cmd/metadata` 回退到 base，`TestDeleteConfirm_DeclineBeforeClient` 中只有新增的 4 个 metadata 用例失败；恢复后 4 个用例全部通过。
- **全量测试**：`go test ./...`（go1.27.3）全部通过。
- **Lint**：golangci-lint v2.15.0（与 `.github/workflows/lint.yml` 中的版本一致）报告 0 issues。
- **手工复现**：用构建出的二进制，在隔离的 HOME 下对 defaults/group/instance/peer 四个命令分别运行：输入 n 的退出码均为 8；`--no-confirm` 且无 URI 时退出码均为 3。另起本地假服务器，用 `--no-confirm --uri ... --token tok` 运行，4 个命令都发出了带 `Bearer tok` 的 DELETE。退出码（因假服务器返回空响应）与 base 二进制一致，行为未回归。
- **PR 冲突**：当前 5 个 open PR 都不改 `cmd/metadata` 或 `cmd/prompts_test.go`。#213 改了 smd 的 delete.go，但与本补丁不重叠。已更正上方“Duplicate check”行，原来只列了 3 个 PR。
- **Issue**：#188 仍无评论、无 assignee、无关联 PR；补丁的修法和测试正是 issue 中建议的方案。
- **Commit**：`fix(metadata): ...` 符合 Conventional Commits 与仓库历史风格，提交信息中无 AI 模型名。
- **pr_body.md**：英文；前两行为 attribution block；有 AI 协助披露段；所述命令、退出码和输出片段均已复现，无夸大。未改动。

结论：PASS。补丁正确、范围恰当，与现有 delete 命令完全一致；所有声明均已独立复现，无需改动补丁。提交前仍需注意 AUDIT 中提到的签名提示：CI 可能要求密码学签名。
