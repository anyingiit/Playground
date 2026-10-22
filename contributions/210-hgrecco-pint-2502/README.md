# 210 — hgrecco/pint#2502: pytest-subtests 已并入 pytest 9

| 项 | 内容 |
|---|---|
| Issue | https://github.com/hgrecco/pint/issues/2502 |
| 层级 | 自由（约 2.5k stars，近期每天都有合并） |
| Labels | 无（2026-10-19 由 rffontenelle 提出，无评论） |
| Base 分支 | `master`（补丁基于 c603d6d） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：issue 无评论、无指派、无关联 PR；`/pulls?q=is:pr subtests` 无相关 PR |
| AI 政策 | CONTRIBUTING / PR 模板 / docs 均无 AI 条款；PR 正文含声明段即可 |
| CLA/DCO | 无 |

## 问题理解
pytest 9.0 已内置 `subtests` fixture，pytest-subtests 仓库已归档。pint 的 `test` extra 仍依赖 pytest-subtests。

## 合理性判断
issue 陈述属实；testsuite 有多处使用 `subtests` fixture。去掉插件必须同时把 pytest 下限提到 9，否则旧 pytest 下 fixture 缺失。pint 要求 Python>=3.12，pytest 9 支持，无兼容问题。pixi 环境通过 `pint[test]` extra 取依赖，无需改 pixi 配置；仓库无 lock 文件。

## 改动
- `pyproject.toml`：`test = ["pytest>=9", "pytest-cov", "pytest-benchmark"]`
- `CHANGES`：0.26.3 (unreleased) 加一行

## 验证
- 新 venv（Python 3.13）`uv pip install -e ".[test]"` → pytest 9.1.1，未装 pytest-subtests；`pytest --benchmark-skip` → 1926 passed, 1171 skipped, 8 xfailed, 288 subtests passed。
- 红：同 venv 降到 pytest<9（无插件）→ `fixture 'subtests' not found`，说明 `>=9` 下限必需。
- pytest 9 + pytest-subtests 0.15 共存也能跑（旧环境不受影响）。
- `taplo fmt --check pyproject.toml` 通过。没跑 pixi（本机无 pixi）、没跑 mpl/numpy 全量环境。

## 需要提交者注意
- 仓库近期涌入大量 PR，提交前再查一次 `/pulls?q=subtests` 和 issue 页。
- PR 模板是 checklist，pr_body.md 已按模板把 checklist 放最前。

## 如何提交
```
git clone https://github.com/hgrecco/pint && cd pint && git checkout -b drop-pytest-subtests origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
另一 agent 在新克隆上 `git am` 成功；新 venv 全量测试结果与上文一致（1926 passed, 288 subtests passed）；全仓再无 pytest-subtests 引用；issue 与 PR 列表无竞争。结论：OK。
