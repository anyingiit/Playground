# hanami/hanami#1284 — Generate action cannot find slice in certain code formatting styles

| 项 | 值 |
|---|---|
| Issue | https://github.com/hanami/hanami/issues/1284 （修复代码在 https://github.com/hanami/cli ） |
| Tier | 自由 |
| Labels | help-wanted |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Base | hanami/cli `main` @ b97aa831df61 (2026-10-01) |
| Duplicate-PR check | 2026-10-01 ~23:00 UTC：issue open、无 assignee、0 条评论；hanami/hanami `pulls?q=1284` → 0；hanami/cli `pulls?q=1284` → 0；hanami/cli `pulls?q=slice+routes` → 只有早已合并的旧 PR（#342/#114/#33…），无人处理该 matcher |
| 排除列表 | exclude_slugs.txt 中无 hanami |

## 问题理解

`hanami generate action home.subscribe --slice=main ...` 在 `config/routes.rb` 中用
`/slice[[:space:]]*:main/` 查找 slice 块（`lib/hanami/cli/generators/app/action.rb#add_route_to_block`）。
当 routes 文件用括号写法（hanamismith 生成的就是这种）：

```ruby
slice(:health, at: "/status") { root to: "show" }
slice(:main, at: "/") { root to: "home.show" }
```

正则匹配不到，报 `cannot find (?-mix:slice[[:space:]]*:main) in config/routes.rb`（HEAD 上实际是
`block_contains?` 里 `content.index` 返回 nil 导致 TypeError，同一根因）。

重要发现：issue 的实际例子是**单行花括号块**。只把正则放宽（scout 建议的一行修复）会让匹配成功，但
`Dry::Files#inject_line_at_block_bottom` 无法往单行块里插入，会把路由插到**错误位置**（已用脚本验证：
路由被插在 health 那行之后、main 块之外），即从“报错”变成“静默写坏 routes.rb”。所以本补丁同时处理单行块。

相关背景：hanamismith PR #1 曾尝试改模板为 do...end，被其维护者拒绝，认为根因在 Hanami；之后才开了本 issue。

## 合理性判断

- 维护者给 issue 打了 `help-wanted`，属明确的 bug，范围小。
- hanami/cli CONTRIBUTING：PR 必须针对已报告的 issue 且必须带测试 —— 满足。
- 无 AGENTS.md / CLAUDE.md；仓库及 labels 页面无任何 AI 相关限制。

## 改动（hanami/cli）

- `lib/hanami/cli/generators/app/action.rb`
  - slice 匹配正则改为 `/slice[[:space:]]*\(?[[:space:]]*:#{namespace}/`，支持 `slice(:main, ...) do`。
  - 新增私有常量 `SINGLE_LINE_BLOCK` 和方法 `expand_single_line_block`：若匹配到的 slice 行是单行
    `{ ... }` 块，则改写成多行 `do ... end`（保留原 body，追加新路由），一次 `fs.write`（输出一次 “Updated config/routes.rb”）。
    非单行块仍走原来的 `inject_line_at_block_bottom`。重复检测 `block_contains?` 先执行，不变。
- `spec/unit/hanami/cli/commands/app/generate/action_spec.rb`：新增 2 个用例（括号 + do 块，两个 slice 都追加；
  issue 原样的单行花括号块，含 `--url --http=post`）。
- `CHANGELOG.md`：Unreleased → Fixed 增加一条。

## 验证

环境：Ruby 3.3.6；仓库 Gemfile 中 `pg`/`mysql2` 需要本机没有的开发库，故用一份去掉这两个 gem 的 Gemfile 副本
（`BUNDLE_GEMFILE=/home/user/work/Gemfile.hanami-local BUNDLE_PATH=/home/user/work/hanami-bundle`）安装依赖；其余与仓库一致。

| 命令 | 结果 |
|---|---|
| 新测试 + 基线 lib（`git show b97aa83:lib/.../action.rb`）：`bundle exec rspec spec/unit/hanami/cli/commands/app/generate/action_spec.rb -e parentheses -e single-line` | **2 examples, 2 failures**（TypeError，找不到 slice）→ red |
| 同上 + 修复后 | 2 examples, 0 failures → green |
| `bundle exec rspec spec/unit/hanami/cli/commands/app/generate/` | 169 examples, 0 failures, 1 pending |
| `bundle exec rspec spec/unit`（修复后） | 456 examples, 121 failures —— 全部是 db/*（本地无 Postgres/MySQL）和 gem/new_spec 4 个（本地 locale 导致 ASCII-8BIT 编码比较失败）；基线同样这些失败（基线 122 = 这 121 + 新测试） |
| `bundle exec rubocop lib/hanami/cli/generators/app/action.rb spec/.../action_spec.rb`（CI 的 rubocop job） | no offenses |
| 在 b97aa83 新 worktree 上 `git am` 补丁 | 干净应用 |

## 独立复审（2026-10-01 23:10 UTC）

- 重读 issue：open、help-wanted、无 assignee、无评论；补丁覆盖 issue 原样的单行括号写法，范围只限 `add_route_to_block`。
- 复跑：只回退 `lib/hanami/cli/generators/app/action.rb` 到 b97aa83 → `action_spec.rb` 57 examples, 2 failures（两条新用例，TypeError）；恢复后 57 examples, 0 failures, 1 pending。
- `bundle exec rubocop` 两个改动的 Ruby 文件 → no offenses。
- 补丁与 clone 提交 c683251 的 `git format-patch` 输出逐字一致；提交作者 anyingiit，提交信息无 AI 模型名；仓库无 DCO 要求。
- `hanami/hanami/pulls?q=1284` → 0；hanami/cli 打开的 PR 只有无关的 #444。
- 注：复审后已删除 `/home/user/work/hanami-bundle`，复跑前需按上文 Gemfile 副本重新 `bundle install`。

## 如何提交

```bash
git clone https://github.com/hanami/cli && cd cli
git checkout -b fix-slice-route-matcher origin/main
git am /path/to/0001-Find-parenthesized-and-single-line-slice-blocks-when.patch
git push <your-fork> fix-slice-route-matcher   # PR 目标: hanami/cli main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。注意 PR 开在 **hanami/cli**，正文用 `Fixes hanami/hanami#1284` 跨仓库引用。

## 需要提交者注意

- 无 DCO、无 PR 模板、无 AI 政策限制；PR 正文含 Claude Code 披露段落。
- CHANGELOG 条目的署名格式仓库惯例是 `(@user in #PR号)`，目前写成 `(@anyingiit, hanami/hanami#1284)`，开 PR 后可改为 `(@anyingiit in #<PR号>)`。
- 设计取舍：单行块会被改写为 do...end（改变用户该行格式）；hanamismith 的 rubocop 可能会再改回单行，这不影响功能。PR 正文已说明，若维护者更希望对单行块直接给清晰报错，可简单改。
- 已知边界（复审发现，未改）：`block_contains?`（`lib/hanami/cli/files.rb`）从 slice 行一直查到下一个 `end`。对单行 `{ }` 块，这个范围会越过本块延伸到后面的块；若后面某个 slice 块里已有**完全相同**的路由字符串，会误报 “already exists” 而跳过。场景很少见，属于既有 `block_contains?` 的局限；维护者若在意可在 `expand_single_line_block` 里只检查本行 body。
- 匹配仍未加 `\b`，`:main` 也会前缀匹配 `:main_admin`（原有行为，未在本 PR 范围内改动）。
- 本地 clone（含提交 c683251）：`/home/user/work/hanami-cli`，分支 `fix-slice-route-matcher-parentheses`。
