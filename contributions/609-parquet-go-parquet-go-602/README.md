# parquet-go/parquet-go#602 — GenericWriter.Reset clears path_in_schema

| 项 | 值 |
|---|---|
| Issue | https://github.com/parquet-go/parquet-go/issues/602 |
| Tier | 自由 |
| Labels | (none) |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | /pulls?q=602 无结果；issue 无评论、无指派、无关联 PR（2026-10-01） |
| AI 政策 | CONTRIBUTING / labels / .github 中均无 AI 相关规定；无 PR 模板；无 DCO 要求 |
| Base | `main` @ eaeafbd |

## 问题理解
v0.32.0 起复用 `GenericWriter`（`Reset` 后写第二个文件）时，后续文件的 column chunk `path_in_schema` 变成 `[""]`，Athena/Spark 读取失败。v0.30.1 正常。

根因：`writer.reset` 对上一文件的 `w.rowGroups[i]` 调用 `format.RowGroup.Reset()`，它会就地 `clear()` `SortingColumns` 和每列 `MetaData.PathInSchema`。而 writer 构造这些元数据时，`PathInSchema` 直接用的是 column writer 的 `columnPath`（`thrift.Slice[string](c.columnPath)`），`SortingColumns` 直接用的是 `w.sortingColumns`。所以 Reset 把 writer 仍在使用的列路径和排序列清零了。
额外发现：同类问题也会把配置的 sorting columns 清零（第二个文件起 `sorting_columns` 变成 `{0,false,false}`），issue 没提到，一并修复并测试。

## 合理性判断
明确的回归 bug，issue 作者已定位到 `format/reset.go`。修复点放在 writer 侧（只在 writer.reset 中先把共享 slice 置 nil），不改 format 包给 footer 解码器复用的 Reset 语义，改动最小。`EncodingStats` 在代码里已经 `slices.Clone`，说明维护者对这种别名问题本就是在 writer 侧处理。

## 改动
- `writer.go`：`writer.reset` 中 Reset 前将 `Columns[j].MetaData.PathInSchema` 和 `SortingColumns` 置 nil（+注释）。
- `writer_test.go`：新增 `TestWriterResetPreservesColumnChunkMetadata`。

## 验证
（GOCACHE/GOMODCACHE 放在 /home/user/work 下，已清理）
- Red（未修复）：`go test -run TestWriterResetPreservesColumnChunkMetadata -count=1 .` → FAIL：file 1/2 `path_in_schema got=[""]`，sorting columns 变为 `{ColumnIdx:0 Descending:false}`。
- Green：同命令 → PASS。
- `go test -trimpath -race -count=1 ./...` → 全部 ok（约 3 分钟）。
- `go vet -tags purego .` → 干净（CI 用的就是 purego vet；不带 tag 的 vet 在 `column_buffer_amd64.s` 上有既有 asm 告警，与本改动无关）。
- `gofmt -l .` 无输出；`GOTOOLCHAIN=go1.25.1 go tool -modfile go.tools.mod modernize -test .` 无输出（`make format` 的检查部分）。

## 需要提交者注意
- 仓库无 DCO、无 AI trailer 要求，commit 中未加 Signed-off-by / Assisted-by。
- 无 PR 模板，pr_body.md 采用 brief 格式。
- CHANGELOG.md 停在 v0.17，不按 PR 维护，未改。
- 修复不改 `format` 包；若维护者更倾向在 `newWriterRowGroup` 里 clone path（每 row group 多一点分配），可按 review 调整。

## 如何提交
```bash
tools/submit_pr.sh contributions/609-parquet-go-parquet-go-602 parquet-go/parquet-go main fix-writer-reset-path-in-schema contributions/609-parquet-go-parquet-go-602/pr_title.txt contributions/609-parquet-go-parquet-go-602/pr_body.md
```
手动：fork → `git checkout -b fix-writer-reset-path-in-schema origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR。

## PR
标题：见 `pr_title.txt`；正文：见 `pr_body.md`。
