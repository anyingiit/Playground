# jaegertracing/jaeger#9717 — M1: remote gRPC storage 8-byte trace ID placement

| 项 | 值 |
|---|---|
| Issue | https://github.com/jaegertracing/jaeger/issues/9717 |
| Tier | 高活跃高Star |
| Labels | good first issue, help wanted |
| Status | ✅ ready — patch + PR text 完成（仅 M1） |
| 重复PR检查 | 2026-10-01：PR 搜索 "9717" / "trace ID" 无相关 open PR；issue 无评论、无 assignee（项目不做 assign） |
| Base | main @ a58fb8e |

## 问题理解
Issue 提出把 trace ID 统一成 32 位 hex，分四个相互独立的 milestone。本补丁只做 **M1**：
`internal/storage/v2/grpc/handler.go`（GetTraces）和 `tracereader.go`（FindTraceIDs、FindTraceSummaries）用 `copy(sized[:], bytes)` 转换线上的 trace ID，8 字节 ID 被放进高 64 位；而 `model.TraceIDFromBytes` 和所有 writer 都放在低 64 位，导致远程存储查到/返回的 ID 与存储不一致。

## 合理性判断
维护者自己写的 issue，带 good first issue / help wanted，M1 明确给出了做法（"Route the handler and reader through model.TraceIDFromBytes or an equivalent that places 8 bytes in the low half, with a regression test"）。范围小、清晰，符合 AI_POLICY 对 "clearly scoped fix" 的要求。

## 改动
- 新增 `traceIDFromBytes` 辅助函数（tracereader.go）：长度为 8 时放入低半部分，其他长度保持原 `copy` 行为（不扩大行为改变范围）。
- handler.GetTraces、reader.FindTraceIDs、convertSummaryBatch 三处改用该函数。
- 测试：新增 `TestHandler_GetTraces_ShortTraceID`、`TestTraceReader_FindTraceSummaries_ShortTraceID`；把 `TestTraceReader_FindTraceIDs` 中原先断言高半部分的 "less than 16 bytes" 用例改为断言低半部分。

## 验证
- Red（未改实现，仅测试）：三个测试全部 FAIL（`go test ./internal/storage/v2/grpc/ -run <name>`）。
- Green：`go test -race -count=1 ./internal/storage/v2/grpc/...` → ok
- `go vet`、`golangci-lint run ./internal/storage/v2/grpc/...`（用 internal/tools 中的 v2.13.1 以 go1.27 编译）→ 0 issues；`golangci-lint fmt --diff` 无输出；import-order 脚本通过。
- `go test ./cmd/remote-storage/...`：仅 `TestAdminServerHandlesPortZero` 失败，在未修改的 base a58fb8e 上同样失败（沙箱环境相关），其余 ok。
- 未跑完整 `make lint test`。

## 需要提交者注意
- **DCO 必需**：commit 已用 `anyingiit <49945850+anyingiit@users.noreply.github.com>` 加了 `Signed-off-by`。CONTRIBUTING 要求 "real name (no pseudonyms)"，如需改为真实姓名请 `git commit --amend -s --reset-author` 后重导。
- **AI_POLICY.md**：允许 AI 辅助，但要求：PR 模板中勾选 AI 使用程度（已勾 Heavy）；提交者必须理解并能解释改动、亲自回复 review（禁止让 agent 自动回复）；PR 描述/观点需是你本人的。请在提交前通读 diff 和 PR 文本并按自己的话调整。
- **新贡献者 open PR 数量上限**（CONTRIBUTING_GUIDELINES "Pull Request Limits for New Contributors"），提交前确认自己在 jaeger 的 open PR 数。
- 只做 M1，PR 写的是 "Part of #9717" 而非 Closes。
- 8 字节以外的长度沿用旧行为（未改成报错）；PR 描述中已说明，如维护者偏好严格校验可改用 `model.TraceIDFromBytes` 并返回错误。
- PR 标题按仓库惯例 `fix(scope): Capitalized summary`。维护者会加 changelog 标签（如 changelog:bugfix-or-minor-feature）。

## 如何提交
```bash
git clone https://github.com/anyingiit/jaeger && cd jaeger   # 先 fork
git remote add upstream https://github.com/jaegertracing/jaeger && git fetch upstream
git checkout -b fix-grpc-8byte-trace-id upstream/main
git am /path/to/0001-fix-storage-Place-8-byte-trace-IDs-in-the-low-half-i.patch
go test ./internal/storage/v2/grpc/...
git push -u origin fix-grpc-8byte-trace-id
gh pr create --repo jaegertracing/jaeger --head anyingiit:fix-grpc-8byte-trace-id --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
fix(storage): Place 8-byte trace IDs in the low half in remote gRPC storage

## PR body
见 pr_body.md
