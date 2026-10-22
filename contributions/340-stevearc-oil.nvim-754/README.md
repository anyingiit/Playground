# stevearc/oil.nvim#754: 互换 foo 和 foo2 的名字时报 "Detected cycle"

| 项 | 值 |
|---|---|
| Issue | https://github.com/stevearc/oil.nvim/issues/754 |
| Tier | 高星（oil.nvim，Neovim 常用文件管理插件） |
| Labels | bug |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 21:25 UTC：issue 无评论、无 assignee、无关联 PR；2026-05 以来的 oil PR 列表里没有相关 PR |
| AI 政策 | 无 CONTRIBUTING，.github 下无 AI 条款 |
| 外部贡献 | 最近合并的 10 个 PR 都是外部贡献者（最新 #788，2026-10-12） |
| Base | `master` @ d3733d9 |
| 提交规范 | conventional（`fix: …`），release-please 生成 CHANGELOG，不用手改 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
`enforce_action_order` 遇到移动环时，先用 `vim.startswith(dest, src)` 判断是不是"把父目录移进自己"。这是纯字符串前缀判断，`foo -> foo2` 被误判成这种情况，于是整次保存报错。报错与否取决于哪一个 move 成为 loop_action，所以报告者说不稳定复现。

## 改动
- `lua/oil/mutator/init.lua`：前缀改成 `src_url .. "/"`，和下面对 selected 动作的检查写法一致。
- `tests/mutator_spec.lua`：新用例，两种顺序都测。

## 验证
- 红：未改 src 时新用例失败，报 `init.lua:318: Detected cycle in desired paths`。
- 绿：`./run_tests.sh` 全部通过（13 个 spec 文件，Failed 0 / Errors 0；nvim 0.11.4 + plenary master）。
- `luacheck lua tests` 干净；stylua v2.1.0 对改动文件 `--check` 干净（仓库里 ssh/connection.lua 有一处跟 stylua 版本有关的既有差异，与本改动无关）。
- 未跑：LuaLS typecheck（make lint，要额外拉工具）。

## 如何提交
```
tools/submit_pr.sh contributions/340-stevearc-oil.nvim-754 stevearc/oil.nvim master fix-754-prefix-cycle contributions/340-stevearc-oil.nvim-754/pr_title.txt contributions/340-stevearc-oil.nvim-754/pr_body.md
```

## 独立复核
复核时间 2026-10-22，在 `/home/user/work/oil.nvim` 分支 `fix-754`（HEAD 493c789，base d3733d9）上逐项重跑，没有沿用上面的结论。

- **Issue**：WebFetch 读取 #754，内容是 `foo`/`foo2` 互换名字后保存报 "Detected cycle in desired paths"。issue 仍为 open，没有评论，也没有关联 PR，与本包描述一致。
- **改动正确性**：
  - 检查了 URL 的构造方式。`src_url = cache.get_parent_url(id) .. entry[FIELD_NAME]`，`dest = parent_url .. diff.name`。parser 会去掉目录名末尾的 `/`，s3 的 `PRE x/` 和 ssh 的 `ls` 解析出来的名字也都不带 `/`，所以 src/dest 不会以 `/` 结尾，`src_url .. "/"` 不会出现 `//`。这个写法与下面 selected 检查（"Cannot move or copy parent into itself"）一致。
  - 用 headless nvim 打印了 `enforce_action_order` 的输出序列。`foo↔foo2` 的两种顺序、目录 `a/foo↔a/foo.bak`、三元环 `x→xx→xxx→x`（正反两种顺序）都得到正确的 tmp 拆分序列：先 `src→src__oil_tmp_N`，再移动另一项，最后 `tmp→dest`。
  - `/a→/a/b` 仍然在 `init.lua:318` 报 cycle 错误，`/a→/a/b/c` 仍然报 "Cannot move or copy parent into itself"。真实的父目录移入子目录照样被拒绝，没有发现回归。
  - 额外写了一个临时 e2e spec（只放在 scratchpad，没有提交）。它用 files 适配器在真实目录里做互换：文件 `foo↔foo2`（内容 A/B）和目录 `foo/↔foo2/` 都互换成功，内容正确。
- **红→绿**：只回退 `lua/oil/mutator/init.lua` 后，新用例失败，报 `init.lua:318: Detected cycle in desired paths`（mutator_spec 结果为 22 过、1 失败），e2e 也报同样的错。恢复后仓库回到原状：分支 fix-754，工作区干净，只剩 `.testenv` 未跟踪。
- **全量测试**：`./run_tests.sh` 跑了 13 个 spec 文件，全部 Failed 0 / Errors 0，结果为 Success。
- **lint/格式**：`luacheck lua tests` 退出码 0，没有输出。stylua 2.1.0 对两个改动文件做 `--check` 是干净的。全仓库检查只有 `lua/oil/adapters/ssh/connection.lua` 有差异，这是既有问题，与本次改动无关。
- **补丁与作者**：`git format-patch -1 HEAD` 的输出与包内 .patch 逐字节相同。author 和 committer 都是 `anyingiit <49945850+anyingiit@users.noreply.github.com>`。在 patch、pr_title、pr_body 里搜索模型名，只在 disclosure 段出现 "Claude Code"。
- **PR 文本**：pr_body 的描述与代码和测试结果相符，没有夸大，包含 disclosure 段。标题和提交信息用 `fix: …` 小写祈使句，与仓库 conventional 风格一致。仓库没有 PR 模板。
- **小建议（不阻塞）**：新用例只断言 `#ordered_actions == 3`，没有断言具体顺序。目前的实现我已经人工确认正确。

结论：PASS

## 复核后补充
- 按复核建议，新用例补了顺序断言（临时名 → 另一文件就位 → 临时名移到目标）。mutator_spec 23 通过；stylua、luacheck 干净；patch 已重新生成。
