# xtermjs/xterm.js #4296 — Issue in Linkifier2._removeIntersectingLinks

| 项 | 值 |
|---|---|
| Issue | https://github.com/xtermjs/xterm.js/issues/4296 |
| Tier | 高星（~20k stars，非常活跃） |
| Labels | area/links, help wanted, type/bug |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论（无人认领）。`pulls?q=4296` 只有 #4288（来源 PR，已合并）；`pulls?q=_removeIntersectingLinks` 0 条；`intersecting links` 只有 2020 年的 #2916（引入该函数）。anyingiit 在该仓库无 PR。 |
| Base | `master` @ c58ea363（2026-08-30） |

## 问题理解
`Linkifier._removeIntersectingLinks`（现位于 `src/browser/Linkifier.ts`，类已从 Linkifier2 改名为 `Linkifier`，测试 describe 仍叫 Linkifier2）只用 x 坐标记录已占用的单元格，并且把起点或终点不在当前行 y 上的链接扩展到 `0..cols`。软换行合并后的一条逻辑行里有多个链接时（web-links provider 会对整条换行行返回链接），不同物理行上的链接仅因 x 区间重叠就被误删。例：A 为 (5,1)..(10,2)，B 为 (20,2)..(30,2)，悬停 y=1 时 A 占用 x 5..cols，B 被删除。

## 合理性判断
- issue 由核心维护者 jerch 提出，带 help wanted + type/bug 标签，修复方向明确（按 (x, y) 记录占用单元格），无需设计讨论。
- AI 政策：仓库有 AGENTS.md（Copilot 说明）、.agents/skills，对 AI 辅助友好，无禁止条款，不需要 AI trailer；无 PR 模板，无 DCO/CLA/changelog 要求。CONTRIBUTING 要求一个 PR 只修一件事并附测试。

## 改动
- `src/browser/Linkifier.ts`：`_removeIntersectingLinks` 改为用绝对偏移 `y * cols + x` 作为单元格 key，覆盖链接从 start 到 end 的完整范围（end 仍为闭区间，与原实现一致）。这和同文件 ~371 行已有的线性索引写法一致。不再需要悬停行 y，所以删除了 `y` 参数，并同步修改唯一调用点。
- `src/browser/Linkifier.test.ts`：在 wrapped links 测试旁新增 `should keep links on different wrapped rows that share x ranges`。注册两个 link provider：provider 0 返回跨两行的链接 A，provider 1 返回第二行上的 B（只与 A 第一行的 x 重叠）和 C（真正与 A 重叠）。测试走 `_askForLink({x:1,y:1}, false)` 的正常流程（不直接调用 `_removeIntersectingLinks`，因此不依赖其签名），然后检查 `_activeProviderReplies`：A、B 保留，C 被删除。

## 验证（Node v22，与 .nvmrc 一致）
```bash
npm ci --ignore-scripts
npm run build && npm run esbuild
npm run test-unit -- out-esbuild/browser/Linkifier.test.js
```
- Red（只把 `src/browser/Linkifier.ts` 还原为 base，`git checkout c58ea363 -- src/browser/Linkifier.ts`，保留新测试）：`4 passing, 1 failing`，`AssertionError: expected [] to deeply equal [ { text: 'foo', … } ]`，即第二行的链接 B 被误删。
- Green（修复后）：5 passing。
- 复审修订（review 阶段）：原测试直接调用 `_removeIntersectingLinks(replies)`，在 base 代码上因签名不同（少了 y）而不会失败，无法证明 red。已改为通过注册 provider + `_askForLink` 驱动，red/green 均已由复审者重新验证。
- `npm run test-unit`（全部 unit test）：2408 passing，无失败。
- `npm run lint-changes`（在提交前的工作区改动上运行，oxlint type-aware + eslint naming）：exit 0；`git apply --check` 到干净的 c58ea363：通过；`npx eslint` 两个文件：exit 0。
- **没有运行**：Playwright 集成测试（`npm run test-integration`），需要下载浏览器，本环境磁盘预算不允许；改动只涉及 Linkifier 内部逻辑，unit test 已覆盖。

## 需要提交者注意
- 删除 `y` 参数是一个小的私有签名调整；如果维护者偏好最小 diff，可以保留参数但不使用（eslint 配置 `args: 'none'` 不会报错）。
- 单元格 key 假设 link range 的 x 是 1-based（1..cols），与 `_linkHover` 里 `x1 = start.x - 1` 的用法一致，不同行之间不会产生 key 冲突。
- PR 正文使用 `Fixes #4296`。

## 如何提交
```bash
git clone https://github.com/xtermjs/xterm.js && cd xterm.js
git checkout -b fix/linkifier-wrapped-intersecting-links origin/master
git am /home/user/Playground/contributions/102-xtermjs-xterm.js-4296/0001-Fix-intersecting-link-removal-for-links-on-wrapped-r.patch
npm ci && npm run build && npm run esbuild && npm run test-unit -- out-esbuild/browser/Linkifier.test.js && npm run lint-changes
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/102-xtermjs-xterm.js-4296 xtermjs/xterm.js master fix/linkifier-wrapped-intersecting-links contributions/102-xtermjs-xterm.js-4296/pr_title.txt contributions/102-xtermjs-xterm.js-4296/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
