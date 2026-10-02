# jaegertracing/jaeger#9717 — M4：移除 ES dbmodel 读取侧 trace/span ID 补零

| 项 | 值 |
|---|---|
| Issue | https://github.com/jaegertracing/jaeger/issues/9717 |
| Tier | 高活跃高Star |
| Labels | good first issue, help wanted |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 只有 #9721 (Piyush4801) 关联本 issue，且只做 M1（gRPC 8-byte ID）。M2/M3/M4 无 PR、无人认领评论；本补丁只做 M4。 |
| Base | `main` @ a58fb8e |
| Patch | `0001-fix-es-Require-full-width-trace-and-span-IDs-when-re.patch` |

## 问题理解
Issue 要求统一 trace ID 为 32 位 hex，分 4 个互相独立的里程碑。M4：让 `dbmodel.TraceID.ToOTEL` / `dbmodel.SpanID.ToOTEL`（ES/OS v2 reader）严格要求 32/16 字符，删除 16 字符 fixture 和只为覆盖补零而存在的测试。

## 合理性判断
- 由维护者自己写的分解计划，标 good first issue；里程碑声明互相独立，M4 不依赖 M1–M3。
- 所有 writer 都经 pdata 写 32 字符，补零只服务历史数据（issue 原文结论）。
- M3（anonymizer）与在途 #9627 重叠、M2 与 #8583 部分重叠，所以选了干净独立的 M4。

## 改动
- `internal/storage/v2/elasticsearch/tracestore/core/dbmodel/model.go`：ToOTEL 宽度不符直接报错，直接 `hex.Decode` 到 pcommon 数组；去掉 `strings` import。
- 删除未被引用的 `tracestore/core/fixtures/es_01.json`（16 字符 ID）及配套 `domain_01.json`。
- 更新测试：ids_test（补零用例改为拒绝用例，新增空 ID 用例）、from_dbmodel_test、reader_test、spansearch_test、core/writer_test（改用全宽 ID / 新错误文本）。
- 行为变化：存储文档里空 traceID/spanID 以前解析为全 0，现在报错（PR 正文已说明）。

## 验证（Go 1.27.0）
- 红：仅应用新 ids_test.go，`go test ./internal/storage/v2/elasticsearch/tracestore/core/dbmodel/ -run ToOTEL` → FAIL（短 ID/空 ID 未报错，旧错误文本）。
- 绿：加修复后同命令 PASS。
- `go test ./internal/storage/v2/elasticsearch/...` → 全部 ok。
- `go vet ./internal/storage/v2/elasticsearch/...` → 无输出。
- `go run mvdan.cc/gofumpt@v0.11.0 -d -e <changed files>` → 无 diff。
- golangci-lint v2.13.1（从 internal/tools 编译）`run ./internal/storage/v2/elasticsearch/tracestore/...` → 仅 1 个既有 revive 问题（core/writer.go:277，未改动文件）。
- 未运行：完整 `make lint test`、ES/OpenSearch 集成测试（需要集群）。

## 需要提交者注意
- **DCO 必须**：提交前用自己的身份 `git commit --amend -s --no-edit` 加 Signed-off-by（补丁里没有）。
- **AI 政策**（AI_POLICY.md）：允许 AI 辅助，但要求在 PR 模板里勾选 AI 使用等级（已勾 Heavy）、提交者能解释每一行、**不能让 agent 自动回复 review**，评审回复要自己写。PR 描述最好再用自己的话改一改（政策强调“Talk to us yourself”）。
- **新贡献者 PR 数量限制**：0 个已合并 PR 时同时只能开 1 个 PR，提交前确认自己在 jaeger 没有其他打开的 PR。
- 本 PR 只是 `Part of #9717`，不要写 Closes。
- 可以先在 issue 下留言“working on M4”（项目不分配 issue，评论后直接提 PR 即可）。

## 如何提交
```bash
git clone https://github.com/anyingiit/jaeger && cd jaeger   # 先 fork
git remote add upstream https://github.com/jaegertracing/jaeger && git fetch upstream
git checkout -b es-strict-id-width upstream/main
git am /path/to/0001-fix-es-Require-full-width-trace-and-span-IDs-when-re.patch
git commit --amend -s --no-edit
go test ./internal/storage/v2/elasticsearch/...
git push origin es-strict-id-width
gh pr create --repo jaegertracing/jaeger --head anyingiit:es-strict-id-width --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
fix(es): Require full-width trace and span IDs when reading from Elasticsearch

## PR body
见 `pr_body.md`。
