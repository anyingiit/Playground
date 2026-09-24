# mloda-ai/mloda#1642 — Add the ratio column to Spark's nullable filter fixture

| | |
|---|---|
| Issue | https://github.com/mloda-ai/mloda/issues/1642 |
| Tier | 新锐项目（mloda，~89★，每日活跃提交，社区驱动） |
| Labels | `bug`, `good first issue`, `help wanted` |
| Status | ✅ 实现 + 全量 `tox` 通过 + `pytest` spark 目标测试通过；无重复 PR |

## 问题理解
[mloda-ai/mloda#1604](https://github.com/mloda-ai/mloda/pull/1604)（已合并）给 `FilterEngineTestMixin` 引入了 float `ratio`
列（含 NaN 与 null）来统一各引擎的 NaN 语义，并更新了 pandas/polars/DuckDB 等 consumer 的 fixture，
但 Spark consumer 的 `nullable_category_sample_data` 仍只有 `id, category, score`。
Spark 不在 CI（`tox.ini` 注明 "This test suite is not tested in CI"），因此 4 个 Spark 测试在
`tox -e spark` 下以 `PySparkKeyError: [KEY_NOT_EXISTS] Key 'ratio'` 失败而没被发现。

## 合理性判断
mixin 的 docstring 已声明 `ratio: [1.0, NaN, 2.0, None, 3.0]` 是 fixture 契约；缺列纯属遗漏，issue 的修复步骤与验收标准都很明确。

## 改动
仅 1 个测试文件：fixture 增加 `ratio double` 列，值按 id 顺序为 `1.0, float("nan"), 2.0, None, 3.0`。

## 验证
- `pytest tests/.../spark/test_spark_filter_engine.py`（JDK 21 + pyspark）：修复前 **4 failed / 51 passed**（正是 issue 列出的 4 个）→ 修复后 **55 passed** ✅
- 整个 spark 目录：修复前 13 failed → 修复后 9 failed；剩余 9 个（`test_spark_integration`、`allow_empty_result`、`asof_merge`）在 `main` 上同样失败，与本改动无关（本地 pandas 3 / JDK 21 环境相关，spark 套件不在 CI）
- 默认 `tox -e python311`（CONTRIBUTING 要求）：**11724 passed, 280 skipped（= EXPECTED_SKIP_COUNT，未变化）**，ruff format/check、`mypy --strict`、bandit 全部通过 ✅
- 遵守规范：Conventional Commits（`fix:`）、从 `main` 开分支、无需文档改动

## 如何提交
```bash
git clone https://github.com/<you>/mloda && cd mloda
git checkout -b fix/spark-ratio-fixture origin/main
git am /path/to/0001-fix-add-the-ratio-column-to-Spark-s-nullable-filter-.patch
git push -u origin HEAD   # base: main
```

### PR — chefs-pick-oss-starter 格式
**Title:** `fix: add the ratio column to Spark's nullable filter fixture`

```markdown
## Description

`FilterEngineTestMixin.nullable_category_sample_data` documents a float `ratio` column
(`[1.0, NaN, 2.0, None, 3.0]`, added with #1604) that several mixin tests filter on, but the Spark
consumer's fixture only built `id`, `category` and `score`. Under `tox -e spark` four tests failed with
`PySparkKeyError: [KEY_NOT_EXISTS] Key 'ratio' is not exists`.

This adds `ratio double` to the Spark fixture with `1.0, float("nan"), 2.0, None, 3.0` in id order,
so the NaN sits at id 2 and the null at id 4, as the mixin docstring describes. Test-only change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1642

## Checklist

- [x] Tests pass locally
  - `pytest tests/test_plugins/compute_framework/base_implementations/spark/test_spark_filter_engine.py`:
    4 failed → 55 passed (the four tests listed in the issue now pass)
  - default `tox`: 11724 passed, 280 skipped (`EXPECTED_SKIP_COUNT` unchanged); ruff, mypy --strict and bandit clean
  - rest of the Spark directory: 9 failures in `test_spark_integration` / `test_spark_allow_empty_result_run_all` /
    `test_spark_asof_merge_engine` fail identically on `main` in my environment (pandas 3, JDK 21), unrelated to this change
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, test-only change
- [ ] Documentation is updated (if applicable) — n/a
```
