# 428 — OpenCHAMI/ochami#191: remove the duplicate CA certificate load in smd group/rfe add

| Item | Details |
|---|---|
| Issue | https://github.com/OpenCHAMI/ochami/issues/191 |
| Tier | Free |
| Labels | good first issue; milestone v0.11.0; opened 2026-10-07 by maintainer synackd |
| Base branch | `main` (patch built on f187792) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments, no assignee and no linked PR. The 5 open PRs (#213, #182, #103, #61, #42) don't touch `cmd/smd/{group,rfe}/add.go`, per 426's review. Rechecked in the 2026-10-22 independent review: none of the PRs touch the 3 files in this patch. #213 changes `cmd/discover/static/static.go` but not the `UseCACert` part, and this patch doesn't touch that file. |
| AI policy | None |
| CLA/DCO | DCO, already signed off |

## Change
- Removed the duplicate `rt.UseCACert` call in `cmd/smd/group/add.go` and `cmd/smd/rfe/add.go`. `GetClient` already loads the CA.
- New test `TestSMDAdd_TrustsCACert`: a TLS server that is trusted only through `--cacert`, run for both commands.

## Verification
- This is a refactor with no behaviour change, so there is no red→green. The new test passes both before and after the fix.
- I confirmed the test depends on `--cacert`: with the flag removed, both cases fail (TLS, exit 7).
- `TestCommands_RejectInvalidCACert` (invalid cacert → CodePayload) still passes.
- `go test ./...` passes. golangci-lint v2.15.0 reports 0 issues.

## How to submit
This is the third PR to the same repository, after 426 and 427. The branches don't conflict. Submit it after 426 and 427, or spread them out.
```
git checkout -b smd-add-single-cacert origin/main && git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- **应用补丁**：重新 clone 后，在 origin/main（f187792）上 `git am` 干净应用。
- **修复安全**：`smd group add` / `smd rfe add` 都经 `smd_lib.GetClient` 取得 client，而 `GetClient`（`internal/cli/smd/smd.go:33`）已调用 `rt.UseCACert`，删除第二次调用不改变行为。
- **范围**：`discover static`（用 `smd.NewClient` 自建 client）未改动。全仓 grep 后，没有其他命令重复加载 CA。pcs/bss/cloud-init/boot/metadata/rcs 的 `GetClient` 各只加载一次，命令层也没有再调用。
- **新测试 `TestSMDAdd_TrustsCACert`**：
  - `go test -race -count=3` 通过。`gotMethod` 写法与本文件其他测试一致：handler 返回、响应送达后才读取，有 happens-before，不存在数据竞争。
  - 符合仓库规范：`t.Parallel()`（含子测试）、有以句号结尾的文档注释、使用 `t.TempDir`。
  - 去掉 `--cacert` 后两个子测试都失败（exit 7，`x509: certificate signed by unknown authority`），说明测试确实依赖该参数。
  - 在修复前的代码上测试也通过，符合“重构的回归保护”这一定位。
- **既有测试**：`TestCommands_RejectInvalidCACert`（含 smd group/rfe add 用例）仍通过。
- **全量验证**：`go test ./...` 全部通过（含 internal/conventions），`golangci-lint` v2.15.0 报告 0 issues，`go vet` 通过。
- **重复工作检查**：issue #191 无评论、无指派、无关联 PR。5 个 open PR（#213、#182、#103、#61、#42）都不涉及本补丁的 3 个文件。
- **提交**：Author 与 Signed-off-by 均为 anyingiit <49945850+anyingiit@users.noreply.github.com>，提交信息中没有 AI 模型名。`refactor(smd):` 符合 Conventional Commits，历史中已有 `fix(smd)`、`feat(smd)` 等 scope。
- **pr_body.md**：前两行为署名块，内容与实际改动及验证结果一致，含 AI 辅助披露段落，并有 `Fixes #191`。
- **小建议（非阻塞）**：新测试只断言 HTTP 方法，没有断言路径。这对测试 TLS 信任已足够。

结论：PASS（改动正确且最小，范围符合 issue，测试有效且无竞争，lint 和全量测试通过，提交和 PR 描述合规）。
