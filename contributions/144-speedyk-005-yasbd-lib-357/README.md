# speedyk-005/yasbd-lib#357 — 基础规则缺少 `c.d.f.` / `w.r.t.` 缩写

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/speedyk-005/yasbd-lib/issues/357 |
| Tier | 自由 |
| Labels | bug, edge-cases, good first issue |
| Status | ✅ ready（patch + PR 文本已就绪） |
| 重复 PR 检查 | 2026-10-01：issue 仍为 open，无 assignee，无评论，没有关联 PR；PR 搜索 `357`、`w.r.t` 都是 0 条结果；当前 open 的 PR（#355、#353、#335）与本 issue 无关 |
| AI 政策 | CONTRIBUTING、.github 和 labels 里都没有禁止 AI 的规定（README 自己写了规则构建时用 AI/LLM 辅助） |
| Base | `main` @ 60c9c48 |

## 问题理解
英文文本 `The model estimates the c.d.f. F. The results are discussed w.r.t. V-TSMixer.` 被切成了 4 句（复现结果：`['The model estimates the c.d.f.', 'F.', 'The results are discussed w.r.t.', 'V-TSMixer.']`），正确结果应为 2 句。

## 合理性判断
这是维护者自己开的 issue，并且已经给出方案：把 `c.d.f` 加进 `REFERENCE_ABBRVS`，把 `w.r.t` 加进 `INLINE_ONLY_ABBRVS`，再补测试。本改动与现有的点号缩写（`e.g`、`i.e`、`a.k.a`）写法一致。

## 改动
- `src/yasbd/rules/base.py`：在 `REFERENCE_ABBRVS` 的 Scientific/Technical 组加入 `"c.d.f"`，在 `INLINE_ONLY_ABBRVS` 的 Bridge/connectors 组加入 `"w.r.t"`。
- `tests/test_boundary_detector.py`：在 `test_universal_regression` 里新增 3 条用例（fix for #357）。
- `CHANGELOG.md`：在 Unreleased / Fixed 下新增条目，PR 链接暂用占位符 `NNN`。
- `CONTRIBUTORS.md`：新增 @anyingiit 一行（CONTRIBUTING 要求在同一个 PR 里加）。

## 验证
环境：`python3 -m venv .venv && .venv/bin/pip install -e ".[dev]" langcodes py3langid`。CI 还会装 spacy，本地没装（体积大）。
- 红：只回滚 `src/` 的改动，运行 `pytest tests/test_boundary_detector.py -k "test_universal_regression and (c.d.f or w.r.t)"`，结果 **3 failed**。
- 绿：加上修复后同一命令通过；`test_universal_regression` 结果为 42 passed。
- 全量：`pytest` 结果为 **127 passed, 2 skipped, 1079 subtests passed**。2 个 skip 是 spaCy 组件测试，因为本地没装 spaCy。
- Lint：`ruff format --check src tests` 结果为 58 files already formatted；`ruff check src tests` 结果为 All checks passed。
- `scripts/reformat_sets.py` 不会改动 `base.py`。它在 main 上会重排无关的 `en.py`/`fa.py`，这部分已还原，没有放进本次 patch。

## 需要提交者注意
- **CHANGELOG 里的 PR 号是占位符**：开 PR 拿到编号后，把 `CHANGELOG.md` 里的两处 `NNN` 改成真实 PR 号。CONTRIBUTING 要求链接写 `pull/NNN`，不能写 issue 链接。改完 amend 再 force-push。
- CONTRIBUTING 规定同一作者最多同时开 2 个 open PR。
- 仓库不要求 DCO 签名，所以没有加 Signed-off-by。
- PR body 用的是仓库自己的 PR 模板（Objective/Changes/Types/Verification/Related Issues），并加入了 disclosure 段落。
- 分支名按 CONTRIBUTING 约定：`bugfix/357-cdf-wrt-abbreviations`。

## 如何提交
```bash
gh repo fork speedyk-005/yasbd-lib --clone && cd yasbd-lib
git checkout -b bugfix/357-cdf-wrt-abbreviations origin/main
git am /path/to/0001-Add-c.d.f-and-w.r.t-to-base-abbreviations.patch
pip install -e ".[dev]" langcodes py3langid && pytest -q && ruff format --check src && ruff check src
git push -u origin bugfix/357-cdf-wrt-abbreviations
gh pr create --repo speedyk-005/yasbd-lib --head anyingiit:bugfix/357-cdf-wrt-abbreviations \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
# 拿到 PR 号后：sed -i 's/NNN/<号>/g' CHANGELOG.md && git commit -a --amend --no-edit && git push -f
```

## PR 标题
见 `pr_title.txt`：Add `c.d.f` and `w.r.t` to the base abbreviations

## PR 正文
见 `pr_body.md`。
