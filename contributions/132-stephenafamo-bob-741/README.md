# stephenafamo/bob#741 — Preload 别名改为确定性（deterministic）

| 项 | 值 |
|---|---|
| Issue | https://github.com/stephenafamo/bob/issues/741 （NextUniqueInt in Preload does not play nice with pgx's statement caching） |
| Tier | 自由 |
| Labels | enhancement, help wanted |
| Status | ✅ ready — patch 和 PR 文本已完成（未提交）；已通过独立复审（2026-10-01） |
| Base | `main` @ 13ef1b5（2026-08-31） |
| Duplicate-PR check | 2026-10-01 检查：issue 仍 open，无评论、无 assignee，没有关联 PR；`pulls?q=741` 结果为 0；用关键词 `NextUniqueInt` 搜到 #639、#721，都已合并，内容是把 randInt 换成 NextUniqueInt，正是造成本问题的改动；用 `preload alias` 搜到的只有 #763（count preloader 列名，与本问题无关）。 |

## 问题理解

`orm.Preload` 在没有 `PreloadAs` 时，给每个 LEFT JOIN 的表起别名 `fmt.Sprintf("%s_%d", to, bob.NextUniqueInt())`。这个计数器是全局递增的，所以同一个查询每 build 一次 SQL 文本都不一样（`users_10001` → `users_10005` …）。pgx 的自动 prepared statement cache 以 SQL 文本为 key，于是缓存永远不命中，而且缓存会持续膨胀。issue 作者目前的绕过办法是手动给每个关系加静态的 `PreloadAs`。

## 合理性判断

- 这是 help wanted 的 enhancement，问题真实存在：我在测试里复现了，两次 build 得到的 SQL 不同。
- 历史背景：#639 因为生产环境出现过随机别名冲突，把 RandInt 换成了全局计数器；#721 修了 randInt 溢出。所以新方案不能再用“随机数”，并且要保证同一个查询内别名唯一。
- 维护者没有给出设计指导。这里选了一个不破坏 API 的默认方案：对路径做 hash。PR 描述里列出了几种可选方案（可读路径名、per-query 计数器）及各自的取舍，维护者想换方案时可以直接调整。
- AI 政策：仓库没有 CONTRIBUTING、AGENTS.md、CLAUDE.md，也没有 PR 模板；README 和 .github 里没有禁止 AI 的规定，label 描述是 GitHub 默认文案。PR 中已包含披露段落。

## 改动

- `orm/load.go`：新增 `preloadAlias(to, parent, relName, side)`。它对 `parent \0 relName \0 side` 计算 FNV-1a 64 位 hash，用 base36 表示，得到别名 `<to>_<hash>`（hash 部分最多 13 个字符）。`Preload` 里原来调用 `NextUniqueInt` 的那一行改为调用它；`PreloadAs` 的逻辑不变。
  - 同一个父别名下的不同关系、以及挂在不同父别名下的同一个关系，得到的别名都不同（父别名本身也是确定性的）。
  - 别名长度有上界，不会因为嵌套变深而超过 PostgreSQL 63 字节的标识符限制。
- `orm/load_alias_test.go`（新增，`package orm_test`，用 psql dialect 构建 SQL，不需要数据库）：
  - `TestPreloadAliasesAreDeterministic`：posts → Author(users) → Pets、Editor(users) → Pets，build 4 次，SQL 必须完全一致。
  - `TestPreloadAliasesAreUniqueWithinQuery`：4 个 JOIN 别名互不相同，并且保留 `users_`/`pets_` 前缀。
  - `TestPreloadAsKeepsStaticAlias`：`PreloadAs("author")` 仍然生效。
- `CHANGELOG.md`：在 Unreleased 下新增 `### Changed` 条目。

## 验证

环境：Go 1.24.7（go.mod 要求 go 1.24.0）；`GOCACHE`/`GOMODCACHE` 放在 /home/user/work/bob-cache，用完已删除；`GOFLAGS=-p=2`。

| 命令 | 结果 |
|---|---|
| 去掉 orm/load.go 的修改，只保留新测试：`go test ./orm/ -run 'PreloadAlias\|PreloadAs' -count=1` | **FAIL**：`TestPreloadAliasesAreDeterministic` 两次 build 的 SQL 不同（`users_10001…` 对 `users_10005…`），另外两个用例通过 → red |
| 打上补丁后，同一条命令 | ok → green |
| `go test -race -count=1 ./...`（CI 的命令，不含 coverage 参数） | 所有不依赖 Docker 的包都 ok（root、orm、expr、dialect/sqlite、dialect/mysql、gen、gen/language、gen/drivers、bobgen-psql/driver/parser、internal、types…）。有 4 个包 FAIL：`dialect/psql`（TestMain 启动 postgres testcontainer）、`gen/bobgen-{psql,mysql,sqlite}/driver`（`panic: rootless Docker not found`），都是本机没有 Docker 导致，与本改动无关；dialect/psql 包内没有 preload 相关的测试。 |
| `go test -race -count=1 ./orm/ . ./dialect/sqlite ./dialect/mysql ./expr`（最终 commit 后） | 全部 ok |
| `gofmt -l .`、`go vet ./orm/` | 无输出 |
| `golangci-lint run ./orm/...`（本机是 v2.5.0，CI 用 latest） | 0 issues |
| `golangci-lint run ./...` | 6 个 issue，全部在未改动的文件里（gen/bobgen-*/driver、debug_exec_test.go、gen/language/go.go），是 lint 版本差异导致的已有问题 |

## 如何提交

```bash
git clone https://github.com/stephenafamo/bob && cd bob
git checkout -b deterministic-preload-alias origin/main
git am /path/to/0001-feat-orm-make-Preload-join-aliases-deterministic.patch
git push <your-fork> deterministic-preload-alias   # PR 目标分支：main
```
PR 标题用 pr_title.txt，正文用 pr_body.md。

### 需要提交者注意
- 提交信息用 Conventional Commits（`feat(orm): ...`），和仓库近期的提交风格一致；仓库没有 DCO，也没有 PR 模板。
- 维护者在 #639 要求过更新 CHANGELOG，已经加上。仓库的条目常以 `([#PR](...)) (thanks @user)` 结尾；目前链接的是 issue，提交 PR 后可以改成 PR 号，是否加 thanks 由你决定。
- 这是一个设计选择（对路径做 hash，没有改 API）。另外有一个行为变化：同一个查询里，从同一个父表对同一个关系 Preload 两次，现在两个 JOIN 会用同一个别名（以前是两个不同的别名）。PR 描述里已经写明，维护者如果倾向其他方案，可能要求修改。
- 生成的 join helper（`120_joins.go.tpl`）仍然使用 NextUniqueInt，不在本 issue 的范围内，PR 中已说明。
- 依赖 Docker 的测试（dialect/psql、gen drivers）没有在本机运行，提交后由 CI 覆盖。
- 别名后缀从原来的约 5 位数字变成最多 13 个 base36 字符。表名很长（约 45 字符以上）时，`"<alias>.<column>"` 这个列别名更容易超过 PostgreSQL 63 字节限制而被截断（以前也有这个风险，只是现在阈值低了约 8 个字符）。如果维护者在意，可以改用 32 位 FNV（最多 7 个字符），单个查询内的碰撞概率仍可忽略。

## 独立复审记录（2026-10-01）

- 重新阅读 issue #741（仍 open、无维护者评论）；`pulls?q=741` 与 `preload alias` 搜索均无重复 PR。
- 复现 red→green：把 `orm/load.go` 换回 base 版本后 `go test -count=1 ./orm/ -run 'PreloadAlias|PreloadAs'` FAIL（`users_10005…` 等每次不同）；恢复补丁后 `go test -count=1 ./orm/` ok。
- `gofmt -l orm`、`go vet ./orm/` 无输出；`golangci-lint run -j2 ./orm/...` 0 issues；`golangci-lint fmt --diff ./orm/...`（gofumpt extra-rules）无差异。
- 确认“同一父表重复 Preload 同一关系会得到相同别名”这一行为变化（构建出两条同别名的 JOIN，PostgreSQL 会报错），已在 PR 描述中说明，未改动设计。
- commit 作者为 anyingiit，无 AI 模型名；补丁未修改。
