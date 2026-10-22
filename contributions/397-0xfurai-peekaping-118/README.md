# 397 — 0xfurai/peekaping#118 TCP / DNS 监控支持 IPv6 地址

| 项 | 值 |
|---|---|
| Issue | https://github.com/0xfurai/peekaping/issues/118 |
| Tier | 新锐（2025 年创建的 Go 版 Uptime Kuma 替代，增长快，测试全） |
| Labels | bug, good first issue, help wanted |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**（第二轮），已采纳全部建议） |
| 重复 PR 检查 | 2026-10-22 21:45 UTC：issue 无关联 PR；仓库仅 3 个开放 PR（#421/#393 push token、#397 secrets），无冲突。维护者 10-18 评论确认并邀请 PR（指明用 net.JoinHostPort） |
| AI 政策 | 无禁止条款；仓库有 AGENTS.md/CLAUDE.md，维护者自己用 agent |
| Base | `main` @ 32d2a93 |
| DCO / CLA | 无 |
| 需先认领 | 否（维护者已公开欢迎 PR） |

## 改动
- `executor/tcp.go`：`net.JoinHostPort`；已写成 `[::1]` 的主机先去掉方括号，避免变成 `[[::1]]`（复核发现的回归，已修）。
- `executor/dns.go`：resolver 地址一次算好，`net.Resolver` 和 miekg/dns 两条路径都用。
- 测试：IPv6 回环监听测试（无 IPv6 时 skip）+ 任何环境都跑的“地址格式正确”测试（含 `[::1]` 子用例）；`startDNSServerOn`、`listenIPv6Loopback` 辅助函数。
- CHANGELOG Unreleased → Fixed 一条。

## 验证
- 红：main 上 `::1` 的三个子测试报 `too many colons in address`；绿：全部通过。
- 本沙箱无 IPv6（AF_INET6 不支持），两个真实监听测试 skip，未亲眼看到通过；复核读代码判断在有 IPv6 的 CI 上能过。
- `go vet` 干净；healthcheck 包测试除 Ping（需 ICMP，main 上同样失败）外全过。
- 独立复核 agent：第二轮 VERDICT PASS（逐一核对 `[`、`[]`、`[::1]x`、zone id 等边界，与修改前行为一致或更好）。第一轮 FAIL（`[::1]` 写法会被双重括号）→ 已修并加测试；另采纳：去掉多余参数、PR 标题按仓库惯例加 `#118` 前缀、正文和 CHANGELOG 说明方括号兼容。

## 如何提交
```
git clone https://github.com/0xfurai/peekaping && cd peekaping
git checkout -b ipv6-tcp-dns-monitors origin/main
git am /path/to/0001-fix-server-dial-IPv6-hosts-in-TCP-and-DNS-monitors.patch
```
无 PR 模板；pr_body.md 已含披露段落。
