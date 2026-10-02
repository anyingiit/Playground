# ipfs-cluster/ipfs-cluster #2323 — allocations endpoint name filtering

| 项 | 值 |
|---|---|
| Issue | https://github.com/ipfs-cluster/ipfs-cluster/issues/2323 |
| Tier | 自由 |
| Labels | `exp/novice`, `good first issue`, `help wanted`, `kind/enhancement` |
| Status | ✅ ready — 独立复审通过（2026-10-01）：patch 可在 master@60b35f2 上 `git am`，red→green 已复现 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=2323` 结果为 0；`is:pr allocations` 没有相关 PR。issue 无人分配、0 评论、没有关联 PR。 |
| Base | `master` @ 60b35f2 |

## 问题理解
`GET /allocations` 目前只能按 pin 类型（`?filter=`）过滤。想找特定名字的 pin，只能把整个 pinset 拉下来在客户端过滤，pin 很多时代价很大。issue 作者（非维护者）希望增加一个按 pin name 过滤的 query 参数。

## 合理性判断
- 改动小，并且向后兼容：两个新参数都是可选的，不传时行为不变。
- 语义直接复用 Pinning Services API 已有的 `name` + `match`（exact/iexact/partial/ipartial），不引入新的设计，因此不需要先做设计讨论。
- 局限：pinset 没有 name 索引，过滤是在服务端流式输出时做的。它减少了响应体积和客户端的工作，但服务端仍要遍历全部 pin。PR 正文已说明。

## 改动
- `api/pinsvcapi/pinsvc/pinsvc.go`：把 `Pin.MatchesName` 的实现提取为包级函数 `MatchesName(name, nameOpt, strategy)`，方法改为委托调用，行为不变。
- `api/rest/restapi.go`：`allocationsHandler` 读取 `name` 和 `match`。`match` 为空时默认 exact；`match` 非法时返回 400（`invalid match value`），写法与非法 `filter` 相同。流式迭代的条件变为：类型匹配并且名字匹配。rest 包新 import 了 `pinsvc`（pinsvc 只依赖 `api`，不会产生 import cycle）。
- `test/rpc_api_mock.go`：mock `Cluster.Pins` 的三个 pin 加上名字 aaa/bbb/ccc，与 `StatusAll` mock 一致。已 grep 确认其他用到 mock 的测试都没有比较 Pins 的 name。
- `api/rest/restapi_test.go`：`TestAPIAllocationsEndpoint` 新增 5 个断言，覆盖 exact 默认、partial 名不匹配、ipartial、iexact 与 filter=pin 组合、非法 match 返回 400。
- 没有改动：Go client（`Client.Allocations` 是导出接口，改签名属于 breaking change）和 `ipfs-cluster-ctl pin ls`。PR 正文中表示可以后续用非 breaking 的方式补上。

## 验证（Go 1.26.0，GOCACHE/GOMODCACHE 放在 clone 内，用完已删除）
```bash
cd /home/user/work/ipfs-cluster
export GOCACHE=$PWD/.gocache GOMODCACHE=$PWD/.gomodcache GOFLAGS=-p=2
go test -run TestAPIAllocationsEndpoint ./api/rest/ -count=1
```
- Red（只改了测试和 mock、handler 还没改时）：5 个新断言全部失败（restapi_test.go:531/536/541/546/552，http 和 libp2p 两个端点都失败）。
- Green（加上实现后）：`--- PASS: TestAPIAllocationsEndpoint`（http 和 libp2p 都通过）。
- `go test ./api/... ./cmd/... -count=1`：api、api/common、api/ipfsproxy、api/pinsvcapi、api/rest、api/rest/client、cmd/ipfs-cluster-ctl、cmd/ipfs-cluster-service 全部 ok。
- `go vet ./api/... ./test/`：干净。`gofmt -l api test` 只报出 `api/pb/generate.go`，这是 base 上本来就有的问题，不是本改动的文件。
- 没有运行：根包和 sharness 的集成测试（耗时长，并且不会走到 mock `Cluster.Pins`）。CI（tests.yml）会跑这些。

## 需要提交者注意
- issue 带 `help wanted` / `good first issue`，无人分配；仓库没有要求先认领（assign）的规则，可以直接提 PR。如想更稳妥，可先在 issue 下留言说明正在处理。
- 不需要 DCO / CLA，不要加 Signed-off-by。
- 仓库没有 AI 政策：CONTRIBUTING 只给了一个已经 404 的链接，没有 AGENTS.md，没有 PR 模板，没有 DCO。`.github/config.yml` 要求 PR 写清上下文并自审，PR 正文已加入 "Self-reviewed" 一项。
- commit 用的是 Conventional Commits 风格的 `feat(restapi): ...`。仓库近期提交混用 `feat:`/`chore:`/`refactor:`，可以接受。
- 如果维护者更希望 rest 包不依赖 pinsvc，可以把 `MatchingStrategy` 移到 `api/types.go`，但那样改动面更大，所以这次没有做。

## 如何提交
```bash
git clone https://github.com/ipfs-cluster/ipfs-cluster && cd ipfs-cluster
git checkout -b feat/allocations-name-filter origin/master
git am /home/user/Playground/contributions/810-ipfs-cluster-ipfs-cluster-2323/0001-feat-restapi-support-name-filtering-in-allocations.patch
go test ./api/... -count=1
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/810-ipfs-cluster-ipfs-cluster-2323 ipfs-cluster/ipfs-cluster master feat/allocations-name-filter contributions/810-ipfs-cluster-ipfs-cluster-2323/pr_title.txt contributions/810-ipfs-cluster-ipfs-cluster-2323/pr_body.md
```

## 独立复审（2026-10-01）
- 在干净的 worktree（origin/master = 60b35f2，与 `git ls-remote` 一致）上 `git am` 成功。
- 只回退 `api/rest/restapi.go`：`go test -run TestAPIAllocationsEndpoint ./api/rest/ -count=1` → FAIL（第 531–552 行断言）；恢复后 → `--- PASS`。
- `go test ./api/... ./cmd/... -count=1` 全部 ok；`go vet ./api/rest/ ./api/pinsvcapi/... ./test/` 干净；`gofmt -l api/rest api/pinsvcapi test` 无输出。
- 确认 consensus/informer/ipfshttp/pubsubmon/pintracker 的测试虽使用 mock RPC，但都不调用 `Cluster.Pins`，mock 加名字不影响它们。
- 复审未发现需要修改的代码问题；仅修正了 README 中的 Labels 字段。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
