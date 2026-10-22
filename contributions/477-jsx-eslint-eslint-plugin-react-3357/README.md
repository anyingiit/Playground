# 477 — jsx-eslint/eslint-plugin-react#3357: `jsx-no-leaked-render` 三元自动修复保留右侧括号

| 项 | 内容 |
|---|---|
| Issue | https://github.com/jsx-eslint/eslint-plugin-react/issues/3357 |
| 层级 | 高星（~9k★，ljharb 持续合并外部 PR） |
| Labels | bug, help wanted |
| 维护者态度 | ljharb（2022-08-15）："shouldn't be removing these parens"，并标 help wanted；报告人后来放弃。 |
| Base 分支 | `master`（补丁基于 b6ba4e1） |
| 状态 | ✅ 可提交（独立复核 PASS） |
| 重复检查 | 2026-10-22：issue 无指派、无关联 PR；`is:pr leaked` 中没有开着的相关 PR（#3502/#3623 已合并，只修了 coerce 分支）。master 上仍可复现。 |
| AI 政策 | 无（CONTRIBUTING 只讲文档格式；无 PR 模板） |
| CLA/DCO | 无 |

## 改动
- `lib/rules/jsx-no-leaked-render.js`：ternary 分支里，右侧被括号包着时，取从左括号到右括号的原文（保留换行）。
- 测试：两个 ternary 无效用例（多行 JSX、括号里的条件表达式）。
- CHANGELOG：Unreleased / Fixed 加一条，链接引用 issue #3357（CHANGELOG 里已有引用 issues/ 链接的先例）。

## 验证
- 红：去掉修复 → 规则测试 243 passing / 6 failing（2 个用例 × 3 个 parser）。
- 绿：249 passing。
- 全量 mocha（tests/lib、tests/util、tests/index.js）18298 passing；`eslint .`、`tsc`、`npm run lint:docs` 通过。

## 需要提交者注意
- PR 标题格式 `[Fix] \`rule\`: ...`（仓库惯例）。
- 仓库 89 个开着的 PR，审核可能慢；ljharb 有时要求把 CHANGELOG 条目改成 PR 号，届时按要求改。
- 提交信息带 `Assisted-by: Claude Code`。

## 如何提交
```
git clone https://github.com/jsx-eslint/eslint-plugin-react && cd eslint-plugin-react && git checkout -b fix-3357 origin/master
git am --keep-non-patch /path/to/0001-*.patch   # 保留提交标题里的 [Fix]
```

## 独立复核（2026-10-22）
- 新克隆 b6ba4e1，`git am --keep-non-patch` 干净（普通 `git am` 会丢掉标题里的 `[Fix]`）。红 243/6 failing → 绿 249；全量 18298 passing；eslint/tsc/lint:docs 通过。
- 三种 parser 下反复修复到稳定：括号内注释、嵌套括号、属性内、TS `as`/`satisfies`/`!` 等都生成合法代码。
- 无竞争 PR（`jsx-no-leaked-render` 开着的 PR 为 0，`3357` 搜索为 0）。
- 范围外发现（未修，可作后续）：coerce 分支 `a && (() => 1)` → `!!a && () => 1` 语法错误；`a && (b, c)` 语义改变。
