# 476 — sql-formatter-org/sql-formatter#773: DB2i 的 JSON_OBJECT 支持 `'key' : value`

| 项 | 内容 |
|---|---|
| Issue | https://github.com/sql-formatter-org/sql-formatter/issues/773 |
| 层级 | 高星（~2.9k★） |
| Labels | bug, db2 |
| 维护者态度 | nene（2024-09-01）复现并确认解析错误；2 年无人处理。 |
| Base 分支 | `master`（补丁基于 223a6ce） |
| 状态 | ✅ 可提交（独立复核 PASS，已按复核意见补 denseOperators 防护） |
| 重复检查 | 2026-10-22：issue 无人指派、无关联 PR；18 个开着的 PR 无 db2i/JSON 相关。 |
| AI 政策 | 无 |
| CLA/DCO | 无 |
| 同仓库 | 本仓库今晚第 2 个（另一个是 475），已到上限 |

## 问题理解
db2i 方言 tokenizer 没有 `:` 运算符（`:` 只作为命名参数前缀），`JSON_OBJECT('key':'val')` 直接报 Parse error。IBM i 文档确认冒号形式合法，且冒号形式的 key 必须是字符串字面量。

## 改动
- `src/languages/db2i/db2i.formatter.ts`：operators 加 `':'`。ExpressionFormatter 已有 `:` 的排版规则（前不空格、后空一格）。
- `src/dialect.ts` + `src/formatter/ExpressionFormatter.ts`：方言把 `:` 当命名参数前缀时，denseOperators 下 `:` 后保留空格（否则 `'k':v` 回读成宿主变量 `:v`）。
- `test/db2i.test.ts`：JSON_OBJECT 冒号形式、denseOperators、`:id` 宿主变量三个测试。

## 验证
- 红：去掉源码改动 → `jest test/db2i.test.ts` 1 failed, 270 passed（宿主变量测试在基线也通过，属保护性测试）。
- 绿：271 passed。
- denseOperators 测试：去掉防护 → 1 failed；加上 → 272 passed。
- 全量：tsc OK、prettier OK、eslint OK、jest 27 suites 5888 passed / 1 skipped。
- 已知边界：`'id':id`（冒号后无空格）仍被读成 `'id'` + 宿主变量 `:id`，与修改前相同，PR 正文已说明。

## 需要提交者注意
- 与 475 同仓库；建议先提交 475，间隔提交即可，两者改不同文件，无冲突。
- 提交信息带 `Assisted-by: Claude Code`；PR 正文含声明段落。

## 如何提交
```
git clone https://github.com/sql-formatter-org/sql-formatter && cd sql-formatter && git checkout -b fix/db2i-json-colon origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 新克隆 223a6ce，`git am` 干净；红→绿成立；全量通过。
- db2i 回归：`INTO :a, :b`、`:rec.field`、`x=:y`、时间字符串、KEY...VALUE 形式均不变；原本报错的 JSON_OBJECTAGG 冒号形式、`lbl: BEGIN` 现在能格式化。
- 发现 denseOperators 下 `'k':v` 会回读为宿主变量 → 已修（见改动）。无竞争 PR（`is:pr db2i`、`is:pr JSON_OBJECT` 均无相关）。
