# vavallee/bindery #2792 — author merge writes books.updated_at in the #914 time.String shape

| 项 | 值 |
|---|---|
| Issue | https://github.com/vavallee/bindery/issues/2792 |
| Tier | 新锐 |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 仍为 open，没有 assignee，也没有评论。`pulls?q=2792` 只搜到不相关的 #2794。用关键词搜 timeValueArg、"author merge updated_at" 时只出现 #921（#914 的原始修复）、#2841、#2759、#2671，都和本 issue 无关。`main` 上 author_aliases.go:369 仍然是直接绑定 `time.Now().UTC()`。 |
| Base | `main` @ f86bbf8（2026-10-01，v1.39.1 changelog） |

## 问题理解
`AuthorAliasRepo.Merge` 在把源作者的书 reparent 到目标作者时，执行 `UPDATE books SET author_id=?, updated_at=? ...`，`updated_at` 直接绑定了 `time.Time`。modernc sqlite 驱动会把它存成 Go 的 `time.String()` 格式（`2026-10-01 18:26:26.79 +0000 UTC`），而不是 #914 之后约定的 RFC3339Nano。读取时 `parseFlexibleTime` 能兼容这种格式，所以不会报错，但同一列会混入两种格式，按文本排序或比较时会出错。

## 合理性判断
- issue 由维护者开出，标签是 bug 和 good first issue，修法也已经写在 issue 里。
- 同文件附近的 `books.go:1210/1411`、`editions.go:320` 都已经用 `timeValueArg(time.Now().UTC())`，这里是漏掉的一处。
- 只改 issue 指出的 books 那一行。`author_identifiers.updated_at`（第 425 行）同样直接绑定了 time.Time，但这张表的所有写入点（包括 `upsertIdentifierTx`）都是这样写的。只改 merge 这一处，反而会让这张表出现两种格式，所以没有改，PR 正文里已说明。

## 改动
- `internal/db/author_aliases.go`：`time.Now().UTC()` 改为 `timeValueArg(time.Now().UTC())`，只动这一行。
- `internal/db/author_aliases_test.go`：新增 `TestMerge_WritesBookUpdatedAtAsRFC3339`，用 `CAST(updated_at AS TEXT)` 读出原始文本，检查其中不含 `" UTC"`，并且能按 RFC3339Nano 解析。
- `changelog.d/2792-merge-updated-at.md`：按仓库约定新增 changelog fragment（`### Fixed`），没有改 CHANGELOG.md。

## 验证（go 1.26.6，GOCACHE/GOMODCACHE 放在 /home/user/work/bindery-cache）
- Red（`git stash` 掉 author_aliases.go 的修复，只保留测试）：`go test -count=1 ./internal/db -run TestMerge_WritesBookUpdatedAt` 失败，报错为 `merge stored books.updated_at in Go default shape "2026-10-01 18:26:26.795488699 +0000 UTC"; want RFC3339Nano`。
- Green：加上修复后，同一条命令通过（PASS）。
- `go test -count=1 ./internal/db`：ok（39.6s）
- `go test -race -count=1 ./internal/db -run 'TestMerge|TestAlias'`：ok
- `go build ./...` 和 `go vet ./...`：通过。`gofmt -l internal/db` 无输出。
- `go test -p 2 -timeout=20m -count=1 ./cmd/... ./internal/...`：退出码 0，58 个包全部 ok，没有 FAIL。
- **没有运行**：`golangci-lint v2.11.4`、`govulncheck`、web 构建。本环境不下载、不执行外部 lint 工具，改动也不涉及 web。

## 独立复核（reviewer，2026-10-01 19:10 UTC）
- 在新的浅克隆（`main` @ ebde7ad，v1.39.1 deploy promote，比实现时的基线 f86bbf8 更新）上 `git am` 干净应用。
- 只回退 `author_aliases.go` 后新测试失败（stored `"... +0000 UTC"`），恢复后通过。
- `go test -count=1 ./internal/db` ok，`go build ./...`、`go vet ./internal/db` 通过，`gofmt -l internal/` 无输出。
- 复核 issue 原文：维护者只要求改 books 那一行并加测试，与 patch 一致；`author_identifiers`（含 `upsertIdentifierTx`）确实全部直接绑定 time.Time，不改是合理的。
- commit 作者 anyingiit，带 DCO Signed-off-by，无 AI 模型名；PR 正文有说明段落和 `Closes #2792`。复核未做修改。

## 需要提交者注意
- **仓库要求 DCO**（PR 有 `DCO / Sign-off` 检查），patch 的 commit 已经带上 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`，与作者一致。提交前请确认你愿意按 DCO 签署。
- AI 政策：AGENTS.md 和 `.claude/skills` 明确欢迎 AI agent，只有一个要求：PR 模板里写着 "Commits authored by a coding agent fail this check; author them as yourself"。patch 的作者已经是 anyingiit，没有 AI trailer。PR 正文中保留了 Claude Code 的说明段落。
- PR 模板是 Summary / How it was verified / Checklist / Test plan，pr_body.md 按这个模板写（Motivation 段放在 Summary 下）。
- 建议分支名：`fix/2792-merge-updated-at`（仓库约定 `fix/<NN>-<slug>`）。
- 提交前请在本地跑一次 `golangci-lint run ./...`（v2.11.4）。

## 如何提交
```bash
git clone https://github.com/vavallee/bindery && cd bindery
git checkout -b fix/2792-merge-updated-at origin/main
git am /home/user/Playground/contributions/705-vavallee-bindery-2792/0001-fix-db-write-books.updated_at-as-RFC3339-on-author-m.patch
go test ./internal/db/... && golangci-lint run ./...
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/705-vavallee-bindery-2792 vavallee/bindery main fix/2792-merge-updated-at contributions/705-vavallee-bindery-2792/pr_title.txt contributions/705-vavallee-bindery-2792/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
