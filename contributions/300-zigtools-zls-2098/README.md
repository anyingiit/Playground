# zigtools/zls#2098: add code action that simplifies variable initialization

| 项 | 值 |
|---|---|
| Issue | https://github.com/zigtools/zls/issues/2098 |
| Tier | 高星（zigtools/zls，5.3k★，几乎每日提交） |
| Labels | feature, good first issue |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 19:50 UTC：`is:pr 2098` → 2 个都已关闭：#2586（ddmoney420，2026-01，维护者 leecannon 因提交了 LLM 生成的 markdown 文件 request changes 后被 techatrix 关闭）、#3197（Metbcy，2026-09-28 作者自己以“清理队列”为由当天关闭，无评审）。issue 无 assignee；srijan-paul 2024-11-30 说过“周末没人做我就做”，之后近两年无动静，不算有效认领 |
| AI 政策 | 仓库无 CONTRIBUTING/AGENTS/CLAUDE.md，无 AI 条款；维护者对 #2586 的意见是“LLM markdown 文件不会被接受”（代码本身未否定）。本补丁只改 2 个 .zig 文件，没有任何多余文件 |
| Base | `master` @ 82ba535 |
| DCO / CLA / changelog | 都不需要 |
| 需先认领 | 否 |

## 问题理解
techatrix 提议加一个代码动作：`const foo = @as(T, x);` → `const foo: T = x;`，`const bar = T{};` → `const bar: T = .{};`（mlugg 确认二者等价）。

## 合理性
维护者本人开的 feature + good first issue，代码动作框架里已有同类 refactor（字符串字面量互转），实现自然。

## 改动
- `src/features/code_actions.zig`：新增 `generateSimplifyVariableInitCodeActions`，在 `generateCodeActionsInRange` 里、字符串上下文判断之前调用。用 `ast.nodesOverlappingIndex` 取光标处最内层变量声明；无类型标注且 init 恰为 `@as(T, v)` 或带类型的 struct init 时，生成一个 `refactor` 动作（两个 TextEdit：名字后插入 `: T`；替换 init）。数组类型（`[_]u8{}` 会被解析成 struct init）跳过；被删除的区域里有 `//` 注释时不提供动作（复核建议后加）。
- `tests/lsp_features/code_actions.zig`：4 个测试（@as、struct init、最内层声明、不应出现动作的 9 种情况，含注释），新 helper `testSimplifyVariableInit` 用 `filter_title` 精确匹配。

## 验证（Zig 0.17.0 = build.zig.zon 的 minimum_zig_version）
- 依赖：代理挡了 GitHub tarball，改用 git 拉取对应 commit 后 `zig fetch <dir>`，哈希与 zon 完全一致。
- 红：只回退 src 改动 → `zig build test -Dtest-filter="simplify variable"` 1 pass / 3 fail；去掉数组守卫 → "no action" 测试失败。
- 绿：4/4 pass。
- 全量：`zig build test` → 39/39 steps，586 passed，11 skipped，0 failed。
- `zig fmt --check src tests build.zig` → OK。

## 需要提交者注意
- 维护者对 AI 垃圾 PR 很敏感（#2586 被关）。PR 里不要带任何额外文件；PR 正文按项目习惯简洁，已含披露段。
- 仓库无 PR 模板；pr_body.md 用 chefs-pick 格式。

## 如何提交
```
tools/submit_pr.sh contributions/300-zigtools-zls-2098 zigtools/zls master simplify-var-init contributions/300-zigtools-zls-2098/pr_title.txt contributions/300-zigtools-zls-2098/pr_body.md
```
（手动：fork → `git checkout -b simplify-var-init origin/master` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 20:15 UTC，独立 agent）
- 新浅克隆 master@82ba535，`git am` 干净；只改 2 个 .zig 文件，无模型名。
- 红→绿：只回退 src → 3 个正向测试失败；打补丁 → 全过。全量 `zig build test` 586 passed / 11 skipped；`zig fmt --check` OK。
- 边界试验全部正确：threadlocal/export/comptime/pub、addrspace+linksection、`@"foo bar"`、尾逗号、嵌套 @as、错误参数个数、`[3]u8{}`/`[_:0]u8{}`/`[_]u8{}`、`@Vector(2,u8){}`、union init、解构、`.only=quickfix`。
- 非阻塞建议：①被删区域里的注释会丢 → 已修（有注释时不提供动作，加 2 个测试，重跑 filter 5/5、全量 586 passed）；②大初始化表达式内任何位置都会提供动作（与“最内层声明”设计一致，保留）；③`[N]T{}` 也被跳过（保守，已写进 PR 正文）。
- 上游：#2098 open、无 assignee、无开着的竞争 PR（#2586、#3197 均已关闭）。
- 结论：PASS
