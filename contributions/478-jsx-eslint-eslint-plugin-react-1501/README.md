# 478 — jsx-eslint/eslint-plugin-react#1501: `jsx-closing-tag-location` 自动修复保留尾随空格

| 项 | 内容 |
|---|---|
| Issue | https://github.com/jsx-eslint/eslint-plugin-react/issues/1501 |
| 层级 | 高星（~9k★） |
| Labels | bug, help wanted |
| 维护者态度 | ljharb（2017-10-26）："No, we can't justify that - you're correct."（自动修复不该改变渲染结果），随即标 bug + help wanted。 |
| Base 分支 | `master`（补丁基于 b6ba4e1） |
| 状态 | 🚧 待独立复核 |
| 重复检查 | 2026-10-22：issue 无指派、无关联 PR。Moong0122 在 2020-10 说过 "I will take a look"，6 年无后续，视为放弃。 |
| AI 政策 | 无 |
| CLA/DCO | 无 |
| 同仓库 | 本仓库今晚第 2 个（另一个 477），已到上限 |

## 问题理解
issue 标题写的是 jsx-closing-bracket-location，但例子 `foo </div>` 实际由 jsx-closing-tag-location 修复：它在 `</div>` 前插入换行，`foo ` 的尾随空格被 JSX 丢掉，渲染从 "foo " 变成 "foo"。master 上已复现。

## 改动
- `lib/rules/jsx-closing-tag-location.js`：插入换行的分支里，如果最后一个子节点是文本且以空格/制表符结尾，把这些空白替换成 `{' '}`（原样空白放进字符串），再换行。
- 测试：`foo </App>`、`{foo} </App>` 两个用例。
- CHANGELOG：Unreleased / Fixed 加一条（放在 jsx-closing-bracket-location 条目后，避免与 477 同一行冲突）；链接定义引用 issue。

## 验证
- 红：去掉修复 → 52 passing / 6 failing；绿：58 passing。
- 全量 mocha 18298 passing；`eslint .`、`tsc`、`npm run lint:docs` 通过。

## 需要提交者注意
- 和 477 都在 CHANGELOG 的 Unreleased 链接定义末尾加了一行，后合并的那个会有一行小冲突；按维护者要求 rebase 即可。
- PR 标题格式 `[Fix] \`rule\`: ...`。提交信息带 `Assisted-by: Claude Code`。

## 如何提交
```
git clone https://github.com/jsx-eslint/eslint-plugin-react && cd eslint-plugin-react && git checkout -b fix-1501 origin/master
git am /path/to/0001-*.patch
```
