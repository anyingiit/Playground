# go-jet/jet #609 — MySQL stringQuote doesn't escape backslashes

| 项 | 值 |
|---|---|
| Issue | https://github.com/go-jet/jet/issues/609 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready（patch + PR 文本已完成） |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=609` 和 `is:pr backslash` 都是 0 结果；issue 处于 open 状态，无指派、无评论 |
| AI 政策 | 仓库里没有 CONTRIBUTING / AGENTS / AI 相关规定，PR 模板也不要求，没有禁止 AI |

## 问题理解
MySQL 默认 sql_mode 下，字符串字面量中的 `\` 是转义符。`internal/jet/sql_builder.go` 里的 `stringQuote` 只把 `'` 替换成 `''`，所以 `jet.FixedLiteral("\\'; DROP TABLE t; --")` 会生成 `'\''; DROP TABLE t; --'`，值能从字面量里逃逸出来，造成注入。`DebugSql()` 输出同样受影响。PostgreSQL 和 SQLite 把反斜杠当普通字符，不受影响。

## 合理性判断
这是一个真实的安全缺陷。issue 里提出的修法之一是转义反斜杠，MySQL 方言对 `[]byte` 已经有自定义序列化（`X'..'`），在同一个钩子里补上 `string` 是最小且一致的改法。

## 改动
- `mysql/dialect.go`：`argumentToString` 新增 `case string`，用 `strings.NewReplacer("\\","\\\\","'","''")` 转义。返回 string 的 `driver.Valuer` 会递归走到这里，也一并覆盖。
- `mysql/literal_test.go`：新增回归测试 `TestStringLiteralBackslashEscaping`，覆盖 FixedLiteral 注入 payload、Windows 路径和 DebugSql 三种情况。
- 刻意没动的部分：`WriteJsonObjKey` 仍走通用的 `stringQuote`，因为 `tests/mysql/select_json_test.go:517-542` 依赖 MySQL 去解释别名里的 `\\`、`\n`；`fmt.Stringer` 也仍走通用路径，`time.Time` 同样是 Stringer，不能一起拦截。这些都写进了 PR 说明。

## 验证
在 `/home/user/work/jet` 下执行（go1.24.7）：
- Red：只加测试、不改代码时，`go test ./mysql/ -run TestStringLiteralBackslashEscaping` 失败（实际输出 `'\''; DROP ...`，期望 `'\\''; DROP ...`）
- Green：加上修复后同一测试通过
- `go test ./mysql/ ./postgres/ ./sqlite/ ./internal/...`：全部 ok
- `gofmt -l mysql internal`：无输出；`go vet ./mysql/`：通过
- `golangci-lint run --no-config ./mysql/...`：改动前后都是 7 个既有问题，没有新增（仓库的 `.golangci.yml` 是 v1 格式，本机 golangci-lint v2 加载不了，所以用了 `--no-config`）
- 没有跑 `tests/mysql`（需要 MySQL 数据库）

## 需要提交者注意
- 仓库不要求 DCO，也不要求 AI trailer。commit 作者是 anyingiit（noreply 邮箱），commit 里没有 AI 字样。
- 这是安全问题，issue 本身已经公开，用普通 PR 提交即可。
- 已知的取舍：如果服务器开启了 `NO_BACKSLASH_ESCAPES`，Debug/FixedLiteral 里的 `\` 会显示成两个，只影响显示，不影响安全。PR 里已说明。

## 如何提交
```bash
git clone https://github.com/go-jet/jet && cd jet   # base: master
git checkout -b mysql-escape-backslash
git am /path/to/071-go-jet-jet-609/0001-mysql-escape-backslashes-in-quoted-string-literals.patch
# 或使用脚本：
tools/submit_pr.sh contributions/071-go-jet-jet-609 go-jet/jet master mysql-escape-backslash contributions/071-go-jet-jet-609/pr_title.txt contributions/071-go-jet-jet-609/pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
