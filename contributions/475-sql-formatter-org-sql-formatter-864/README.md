# 475 — sql-formatter-org/sql-formatter#864: PostgreSQL `SELECT ... INTO` 的 INTO 单独成行

| 项 | 内容 |
|---|---|
| Issue | https://github.com/sql-formatter-org/sql-formatter/issues/864 |
| 层级 | 高星（~2.6k★，npm 周下载量很大；维护者 nene 9 月仍在合并外部 PR） |
| Labels | bug, postgresql, transactsql |
| 维护者态度 | nene（2025-05-09）：SELECT INTO 可以"用不大的工作量"支持，但要检查 INTO 出现的其他位置；随后把标签从 feature 改成 bug。 |
| Base 分支 | `master`（补丁基于 223a6ce） |
| 状态 | ✅ 可提交（待独立复核） |
| 重复检查 | 2026-10-22：issue 无人指派、无关联 PR；18 个开着的 PR 中没有改 INTO 的。#993（MERGE for PostgreSQL）也加了 `'MERGE INTO'`，与本补丁同一个列表，可能有很小的文本冲突。 |
| AI 政策 | 仓库内无（CONTRIBUTING 只说项目基本处于维护模式、需加测试） |
| CLA/DCO | 无 |

## 问题理解
PostgreSQL 方言没有把 `INTO` 当子句，`SELECT a, b INTO t FROM x` 格式化成 `b INTO t` 挂在最后一列后面。transactsql/db2 方言已经把 `INTO` 列为 reservedClauses。

## 改动
- `src/languages/postgresql/postgresql.formatter.ts`：reservedClauses 加 `'INTO'`；另加 `'MERGE INTO'`，否则 MERGE INTO 会被拆成两行（基线是一行）。
- `test/postgresql.test.ts`：两个测试（SELECT INTO TEMP TABLE、MERGE INTO 不拆开）。
- 手工检查过：INSERT INTO 不变；`RETURNING id INTO v`、`INTO STRICT`、`IMPORT FOREIGN SCHEMA ... INTO` 中 INTO 也单独成行（PR 正文已说明）。

## 验证
- 红：去掉源码改动，`jest test/postgresql.test.ts` → 2 failed, 461 passed。
- 绿：→ 463 passed。
- 全量：`tsc --noEmit` OK、`prettier --check .` OK、`eslint .` OK、`jest` 27 suites，5887 passed / 1 skipped。

## 需要提交者注意
- PR 正文含 AI 声明段落；提交信息带 `Assisted-by: Claude Code`。
- 本地 pnpm v10 会改写 pnpm-lock.yaml，补丁里没有带。

## 如何提交
```
git clone https://github.com/sql-formatter-org/sql-formatter && cd sql-formatter && git checkout -b fix/postgresql-select-into origin/master
git am /path/to/0001-*.patch
```
PR 标题见 pr_title.txt，正文见 pr_body.md。
