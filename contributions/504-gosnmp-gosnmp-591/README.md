# gosnmp/gosnmp#591 — SNMP over TCP framing for large responses

| 项 | 值 |
|---|---|
| Issue | https://github.com/gosnmp/gosnmp/issues/591 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01: `/pulls?q=591` 与 `is:pr TCP` 均无相关 PR（仅 #522 EOF panic、#615 trap closer 等无关）；issue open、未指派、无评论 |
| Base | `master` @ d2a3184e8a0f |

## 问题理解
TCP 是字节流，但 `receive()` 每次 `Conn.Read` 当作一个完整的 UDP 报文处理。大响应被分段时只解码第一段 → `error verifying packet sanity: Got 1448 Expected: 2611`；剩余字节被当作新报文 → `invalid packet header`。多个响应落在同一段时也会出错。

## 合理性判断
明显的 bug，RFC 3430 规定以 BER 长度分帧。仓库无 AGENTS.md/CONTRIBUTING，grep 无 AI 政策，labels 无"human only"描述 → 允许 AI 辅助 PR。

## 改动
- `marshal.go`: `receive()` 在 TCP（非 PacketConn）时走新 `receiveStream()`：先读 tag+长度首字节，再读长度字节（≤4），用 `parseLength` 得到总长，`io.ReadFull` 精确读满，不多读下一条报文。首字节前的干净 EOF 仍返回 `io.EOF`，重连逻辑不变。UDP 路径不变。
- `marshal_test.go`: 2 个回归测试（TCP 分块 Get 端到端；net.Pipe 拆包/粘包）。

## 验证
`export GOCACHE=... GOTOOLCHAIN=local`（本地 go1.24.7，go.mod 要求 1.24.0）
- 红：`git stash marshal.go; go test -tags marshal -run TCP .` → FAIL：`Get failed: error verifying packet sanity: Got 1000 Expected: 5835`、`message 0: got 1 bytes, want 245 bytes`
- 绿：同命令 ok
- `go test -count=1 -tags {helper,marshal,misc,api} .` 全部 ok；`-race -tags marshal -run 'TCP|SendOneRequest'` ok
- `gofmt -l .` 空；`go vet -tags all ./...` 干净；`make lint`（license header）ok
- `go test -fuzztime 15s -tags marshal -fuzz '^FuzzUnmarshal$'` PASS
- golangci-lint：本地 2.5.0 不认识 `modernize`，去掉该项后运行：6 个问题，与 base 完全相同（均为既有代码），新代码无新增
- 未运行：`end2end` 与 netsnmp 测试（需要本地 snmpd/libsnmp-dev）

## 需要提交者注意
- 仓库不要求 DCO、不要求 AI trailer；patch 作者为 anyingiit noreply 邮箱，无 Signed-off-by。
- CHANGELOG 的 unreleased 段只有占位符，近期 PR 未更新，因此未改；如维护者要求，加 `* [BUGFIX] Frame SNMP messages over TCP using the BER length #<PR>`。
- PR 正文含 AI 辅助披露段落。
- 默认分支为 `master`（提交前确认）。

## 如何提交
```bash
git clone https://github.com/gosnmp/gosnmp && cd gosnmp
git checkout -b fix-tcp-framing-591 origin/master
git am /home/user/Playground/contributions/504-gosnmp-gosnmp-591/0001-*.patch
go test -tags marshal -run TCP .
# 或使用脚本：
tools/submit_pr.sh contributions/504-gosnmp-gosnmp-591 gosnmp/gosnmp master fix-tcp-framing-591 contributions/504-gosnmp-gosnmp-591/pr_title.txt contributions/504-gosnmp-gosnmp-591/pr_body.md
```

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。
