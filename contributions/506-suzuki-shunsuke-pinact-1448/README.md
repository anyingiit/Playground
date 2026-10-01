# suzuki-shunsuke/pinact #1448 — Error message is unhelpful

| 项目 | 值 |
|---|---|
| Issue | https://github.com/suzuki-shunsuke/pinact/issues/1448 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready |
| 重复 PR 检查 | 2026-10-01 `/pulls?q=1448` 0 结果；issue 无评论、无 assignee、无关联 PR |
| Base branch | `main` (@ ef96802) |

## 问题理解
`processAction` 各分支在无法 pin 时只返回 `ErrCantPinned`（"action can't be pinned"），用户看不出原因。issue 举例：`@master`/`@latest`（非 semver，按设计不支持）和 `@<md5/sha224 等 hex>`（不是完整 commit SHA）。

## 合理性判断
合理：纯错误信息改进，不改行为；仓库已有 `docs/why_pinact_not_pin.md` 解释设计，新消息直接链接它。issue 为维护者仓库中开放问题，无人认领。

## 改动
- `pkg/controller/run/parse_line.go`：新增 `errCantPinned(reason)`（`fmt.Errorf("%w: %s", ErrCantPinned, reason)`）和 `errNonSemverVersion(v)`（≥7 位纯 hex 时提示"不是完整 40 位 commit SHA"，否则提示仅支持 semver + `--branch-to-tag` + 文档链接）；替换所有 7 处裸 `ErrCantPinned`。`errors.Is` 仍成立，退出码不变。
- `parse_line_internal_test.go`：新增 `TestController_parseLine_cantPinnedReason`（6 个子用例，不需 API）。

## 验证
- Red：修复前新测试 6/6 失败（消息只有 "action can't be pinned"）。
- Green：`go test ./pkg/controller/run -run TestController_parseLine_cantPinnedReason -v` 全过。
- `go test ./... -race -covermode=atomic`（= `cmdx t`）全 ok；`go vet ./...` ok；`golangci-lint run ./pkg/controller/run/...`（v2.14.0，aqua 指定版本）0 issues；`gofumpt -l`（v0.12.0）无输出。

## 需要提交者注意
- 仓库要求 **签名提交**（Require signed commits）：`git am` 之后请用自己的 GPG/SSH 签名重新提交（`git commit --amend -S --no-edit`）。
- 贡献指南允许使用 AI，但要求**明确披露并自行审阅、负责**；PR body 已含披露段，请自己读一遍 diff 再提交。
- PR 模板 checklist 已保留（不得删除）；勾选"commits are signed"前确认确实签名。
- 指南要求先 issue 讨论：issue #1448 已存在但维护者尚未回复，可考虑先在 issue 下简单留言说明方案。
- 无 DCO、无 AI trailer 要求，提交中未加。

## 如何提交
```sh
git clone https://github.com/anyingiit/pinact && cd pinact   # 先 fork
git checkout -b fix/explain-cant-pin origin/main
git am /path/to/0001-fix-explain-why-an-action-can-t-be-pinned.patch
git commit --amend -S --no-edit   # 签名
git push -u origin fix/explain-cant-pin
# 或：
tools/submit_pr.sh <folder> suzuki-shunsuke/pinact main fix/explain-cant-pin <folder>/pr_title.txt <folder>/pr_body.md
```
PR 标题/正文：见 `pr_title.txt` / `pr_body.md`。
