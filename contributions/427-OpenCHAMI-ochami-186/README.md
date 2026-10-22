# 427 — OpenCHAMI/ochami#186: fix the `metadata --uri` help text

| Item | Details |
|---|---|
| Issue | https://github.com/OpenCHAMI/ochami/issues/186 |
| Tier | Free |
| Labels | bug, documentation, good first issue; milestone v0.11.0; opened 2026-10-07 by maintainer synackd |
| Base branch | `main` (patch built on f187792) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments, no assignee and no linked PR, and no open PR touches it. |
| AI policy | None |
| CLA/DCO | DCO, already signed off |

## Change
- One help string in `cmd/metadata/metadata.go`: "boot service" becomes "metadata service".
- A new `TestServiceURIFlagUsage` checks the `--uri` help text of all 7 service commands. This also covers the issue's request to check the other commands.

## Verification
- Red: on the base, the new test fails (metadata says boot service). Green: it passes after the fix.
- `go test ./...` passes, and golangci-lint v2.15.0 reports 0 issues.
- The binary's `metadata --help` output is correct.

## How to submit
Submit together with 426 (two independent PRs to the same repository; the branches do not conflict):
```
git checkout -b fix-metadata-uri-help origin/main && git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）

- **应用补丁**：全新克隆 `OpenCHAMI/ochami`，在 origin/main（f187792）上执行 `git am`，补丁干净应用。
- **修复内容**：`cmd/metadata/metadata.go` 中 `--uri` 的帮助文本已从 "boot service" 改为 "metadata service"，与 issue #186 建议的措辞一致。
- **其他服务命令**：逐一核对 boot / bss / cloud-init / pcs / rcs / smd 六个顶层命令的持久 `--uri` 文本，各自名称正确；测试中的映射表与源码中的实际文本完全一致。另有 `discover static` 的本地 `--uri`（写的是 "SMD"，用途正确），它不是顶层持久 flag，不在测试范围内，PR 描述也没有声称覆盖它。
- **测试质量**：`TestServiceURIFlagUsage` 调用了 `t.Parallel()`，每次新建 `NewRootCmd()`，不共享状态；文档注释以句号结尾（godot）；风格与同文件的 `TestNoDuplicateFlags` 一致。测试双向检查：缺少映射条目会报错，映射条目没有对应命令也会报错。
- **遍历中删除 map**：循环遍历的是 `rootCmd.Commands()` 切片，不是 map，所以 `delete(services, …)` 没有任何问题（况且 Go 本身也允许在 range map 时删除）。
- **红→绿**：只把 `metadata.go` 还原后，新测试失败（`ochami metadata --uri usage = "... of boot service"`）；应用补丁后通过。
- **`go test ./... -count=1`**（go1.27.3）：全部通过。
- **`golangci-lint run ./...`**（v2.15.0）：0 issues；`gofmt -l` 与 `git diff --check` 均无输出。
- **构建**：`go build` 成功，`ochami metadata --help` 显示 `absolute base URI or relative base path of metadata service`。
- **查重**：issue 仍为 open，无指派、无评论、无关联 PR。当前 5 个 open PR（#213、#182、#103、#61、#42）都不涉及此问题；#213 的文件列表不包含 `cmd/metadata/metadata.go` 和 `cmd/root_test.go`，不会冲突。
- **提交**：作者为 anyingiit <49945850+anyingiit@users.noreply.github.com>，带 Signed-off-by；提交信息中没有 AI 模型名称；标题 `fix(metadata): …` 符合 Conventional Commits。
- **pr_body.md**：英文、内容准确；前两行是署名块；有 AI 辅助披露段落。无需修改。

结论：PASS。修复正确且最小；测试有效、稳健并符合仓库 lint 规则；所有声明均已复现，也没有重复或冲突的 PR。
