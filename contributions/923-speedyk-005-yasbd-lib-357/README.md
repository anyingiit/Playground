# speedyk-005/yasbd-lib#357 — base rules 缺少 `c.d.f.` / `w.r.t.`

| 项 | 值 |
|---|---|
| Issue | https://github.com/speedyk-005/yasbd-lib/issues/357 |
| Tier | 自由 |
| Labels | bug, edge-cases, good first issue |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01：issue 无评论、无 assignee、无关联 PR；`is:pr 357` 搜索 0 结果 |
| AI 政策 | CONTRIBUTING / .github / labels 都没有禁止 AI 贡献（README 里还说规则维护本身也用了 AI/LLM 辅助）|
| Base | `main` @ 60c9c48 |

## 问题理解
`c.d.f.`（累积分布函数）和 `w.r.t.`（关于）不在 base 缩写表里，所以 `The model estimates the c.d.f. F.` 会被切成 `…c.d.f.` + `F.`，`discussed w.r.t. V-TSMixer.` 也会在 `w.r.t.` 后面被切开。

## 合理性判断
维护者自己给的 issue 已经写明修法（`c.d.f` 放进 `REFERENCE_ABBRVS`，`w.r.t` 放进 `INLINE_ONLY_ABBRVS`），而且有 good first issue 标签。CHANGELOG 里有很多同类的"补缩写"修复，所以这个改动合理、范围也小。

## 改动
- `src/yasbd/rules/base.py`：`REFERENCE_ABBRVS` 加 `"c.d.f"`，`INLINE_ONLY_ABBRVS` 加 `"w.r.t"`
- `tests/test_data/english.py`：加 issue 里的原句，再加一个 `w.r.t.` 后接小写词的防护用例（CONTRIBUTING 要求优先扩展现有的测试数据）
- `CHANGELOG.md`：Unreleased/Fixed 下加一条，链接先写成 `pull/NNN` 占位
- `CONTRIBUTORS.md`：按字母序加 `@anyingiit` 一行（CONTRIBUTING 要求）

## 验证
```
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]" spacy langcodes py3langid   # 与 CI 一致
.venv/bin/pytest -q                     # 修复后：128 passed, 1081 subtests passed
git stash push src && pytest -k "en-" tests/test_boundary_detector.py
  # 没有修复时：en 失败 'The model estimates the c.d.f.' != 'The model estimates the c.d.f. F.'（red）
ruff format --check / ruff check src/yasbd/rules/base.py   # 通过
```
- `ruff format --check tests/test_data/english.py` 在 main 上本来就报格式问题（因为数据文件里有分组空行），我没去动；
  仓库全量 `ruff check` / `ruff format --check` 只在 `benchmarks/bench_warm_cases.py` 和 `examples/query_summary.py` 上报错，也是 main 上原有的问题。
- 按 CONTRIBUTING 跑了 `scripts/reformat_sets.py`，它会顺带改到无关的 `en.py` / `fa.py`，所以那些改动已经还原（保持 PR 原子性）。`base.py` 的格式不受影响。
- 已知限制：`c.d.f.` 在句尾、后面跟大写词（`…the c.d.f. It is…`）时不会切分。所有 REFERENCE_ABBRVS 都是这样（`fig.`、`approx.` 也一样），本 PR 不处理，PR 正文里已经说明。

## 需要提交者注意
- **CHANGELOG 里的 `#NNN` / `pull/NNN` 要在开 PR 后换成真实的 PR 号**（CONTRIBUTING 要求链接写 PR 而不是 issue），可以开 PR 后 amend 再 force-push。
- 不需要 DCO（仓库没有要求 sign-off）。
- CONTRIBUTING 规定同一个人最多同时开 2 个 PR，提交前先确认自己在这个仓库已开的 PR 数。
- PR 正文用的是仓库自己的模板（Objective/Changes/Types/Verification/Related Issues），已经加入 disclosure 段落。
- 分支名按 CONTRIBUTING 用 `bugfix/357-cdf-wrt-abbreviations`。

## 如何提交
```bash
gh repo fork speedyk-005/yasbd-lib --clone && cd yasbd-lib
git checkout -b bugfix/357-cdf-wrt-abbreviations origin/main
git am /path/to/0001-fix-add-c.d.f.-and-w.r.t.-to-base-abbreviation-rules.patch
git push -u origin bugfix/357-cdf-wrt-abbreviations
gh pr create --repo speedyk-005/yasbd-lib --head anyingiit:bugfix/357-cdf-wrt-abbreviations \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
# 拿到 PR 号后：把 CHANGELOG 的 NNN 替换掉，然后 git commit --amend --no-edit && git push -f
```

## PR title
fix: add c.d.f. and w.r.t. to base abbreviation rules

## PR body
见 `pr_body.md`。
