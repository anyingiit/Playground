# emersion/go-smtp#315 — BDAT chunk discard missing

| 项 | 值 |
|---|---|
| Issue | https://github.com/emersion/go-smtp/issues/315 |
| Tier | 自由（~2k stars） |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文案已就绪 |
| 重复 PR 检查 (2026-10-01) | /pulls?q=315 无结果；`is:pr bdat` 只有 #312（DATA 读取优化，无关）和几个已合并的旧 PR；issue 没有评论，也没有指派 |
| AI 政策 | 仓库里没有 CONTRIBUTING/AGENTS 文件，issue 模板也没提 AI → 允许 |

## 问题理解
服务端一直对外宣告 CHUNKING。客户端可以在 `BDAT n` 后面不等回复直接发 n 字节的 chunk（pipelining）。`handleBdat` 遇到以下几种情况会直接返回 5xx，但没有读走 chunk，结果 chunk 内容被当成 SMTP 命令解析：没有 MAIL/RCPT、第二个参数不是 LAST、参数过多。RFC 3030 要求即使拒绝命令也要消费掉 chunk。

## 合理性判断
这是协议层面的正确性 bug，issue 里给出了复现测试；同一文件里 MaxMessageBytes 分支已经有丢弃逻辑，作者的意图很明确。修复合理。

## 改动（conn.go, server_test.go）
- 先解析 size。size 缺失或格式错误时 chunk 长度未知，无法丢弃，保持原行为。
- size 已知之后，所有拒绝分支（参数过多、未知参数、缺少 MAIL/RCPT、MaxMessageBytes 超限）都先调用新增的 `discardChunk(size)`。这个函数丢弃期间临时关闭 line limit，结束后恢复原值。
- 新增表驱动测试 `TestServer_Chunking_rejectedChunkDiscarded`，4 个子用例。chunk 内容是 `QUIT\r\n`，之后发 NOOP，必须拿到 250。

## 验证（Go 1.24.7，工作目录 /home/user/work/go-smtp）
- Red（修复前）：`go test -run TestServer_Chunking_rejectedChunkDiscarded .` → 4 个子测试全部 FAIL，报错 `221 2.0.0 Bye`
- Green：`gofmt -l .` 无输出；`go vet .` 通过；`go test ./...` → `ok github.com/emersion/go-smtp`；`go test -count=1 -run Chunking -v .` 全部 PASS

## 需要提交者注意
- 仓库不要求 DCO，也不要求 AI trailer，所以 commit 里没有加 Signed-off-by / Assisted-by。
- commit 风格沿用 `server: ...` 前缀。仓库没有 PR 模板和 CHANGELOG。
- 行为变化：size 合法但命令被拒时，服务端现在会读走最多 size 字节（上限 2^32-1，与原有 MaxMessageBytes 分支一致）。

## 如何提交
base 分支：`master`
```
git clone https://github.com/emersion/go-smtp && cd go-smtp
git checkout -b fix-bdat-discard
git am /home/user/Playground/contributions/502-emersion-go-smtp-315/0001-server-discard-BDAT-chunk-when-the-command-is-reject.patch
# 或者直接用脚本：
tools/submit_pr.sh contributions/502-emersion-go-smtp-315 emersion/go-smtp master fix-bdat-discard contributions/502-emersion-go-smtp-315/pr_title.txt contributions/502-emersion-go-smtp-315/pr_body.md
```

## PR 标题
见 `pr_title.txt`：server: discard BDAT chunk when the command is rejected

## PR 正文
见 `pr_body.md`。
