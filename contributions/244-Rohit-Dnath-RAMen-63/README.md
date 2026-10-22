# Rohit-Dnath/RAMen#63: SPOP / SRANDMEMBER copy the whole set to pick one member

| 项 | 值 |
|---|---|
| Issue | https://github.com/Rohit-Dnath/RAMen/issues/63 |
| Tier | 自由（Go，Redis 兼容内存库） |
| Labels | good first issue, performance |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 20:10 UTC：`repo:Rohit-Dnath/RAMen SPOP` → 只有已合并的 #50（引入命令）和无关 #42；issue 无评论、无 assignee、无关联 PR |
| AI 政策 | CONTRIBUTING 无 AI 限制（提到 AI 的只是产品的 MCP 模块） |
| Base | `main` @ dab982a |
| DCO / CLA | 均不需要 |
| 需先认领 | 否 |

## 问题理解
`SPop` / `SRandMember` 先把整个 set 复制到 slice 再 `sampleMembers`（还会整体 shuffle），单次 O(n)，SPOP 还持写锁；循环 SPOP 清空大集合 O(n²)。Issue 给出方案：count 1 用 map range 取第一个（不完全均匀需写文档）；小 count 用蓄水池/部分 Fisher-Yates；负 count 保留复制。要求：现有测试通过、普通调用不 O(n) 分配、加大集合 benchmark。

## 改动
- `internal/store/set.go`：`sampleMembers` → `sampleSet(set, count)`：count==1 取 map range 第一个（同 `RandomKey` 做法）；1<count<n 蓄水池抽样 + 对结果 shuffle；count≥n 或负数仍复制。注释说明非完全均匀。
- `internal/store/store_test.go`：分配回归测试（10 万成员，count 1/5，每次 ≤4 KiB）、均匀性 sanity 测试、两个 1M 成员 benchmark。新增 import `runtime`。
- `docs/commands.md`：SPOP / SRANDMEMBER 行注明单成员 O(1) 且不完全均匀。
- commit 风格：仓库直接用句子式标题（非 Conventional Commits），已照做；`Fixes #63`。

## 验证（go 1.25.0，按 go.mod）
- 红：回退 set.go 后 `go test ./internal/store/ -run 'TestSetSample|TestSRand'` → FAIL："SRANDMEMBER count 1 allocates 1605708 bytes per call, want <= 4096"
- 绿：恢复后 → ok
- `go vet ./...` 干净；`gofmt -l` 无输出；`go test -race ./... -count=1` 全部 ok（store 22s）
- Benchmark（1M 成员）：SRandMember 71.0ms/16.0MB → 535ns/16B；SPop 69.5ms/16.0MB → 791ns/16B

## 如何提交
```
tools/submit_pr.sh contributions/244-Rohit-Dnath-RAMen-63 Rohit-Dnath/RAMen main set-sample-without-copy contributions/244-Rohit-Dnath-RAMen-63/pr_title.txt contributions/244-Rohit-Dnath-RAMen-63/pr_body.md
```
（手动：fork → `git checkout -b set-sample-without-copy origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 20:30 UTC）
- 上游：#63 open、未指派、无评论；PR 搜索 `63` → 只有无关的 #53，`SRANDMEMBER` → 只有已关闭的 #50。
- `git am` 干净（main@dab982a），作者 anyingiit noreply。
- 红→绿确认；gofmt/go vet 干净；`go test -race ./...` 全过；新测试 `-race -count=30`、TestSRand `-count=500` 压测均通过。
- 各 count 分支与旧行为及 Redis 规则一致；Algorithm R 正确，结果均匀；map 首键随机但不均匀的说明准确且已文档化。均匀性测试误报概率约 1e-48；store 包无后台 goroutine，TotalAlloc 测试不受干扰。
- 结论：PASS
