# maziyarpanahi/openmed#3101 — Diff clinical language-pack coverage manifests across releases

| 项 | 值 |
|---|---|
| Issue | https://github.com/maziyarpanahi/openmed/issues/3101 |
| Tier | 新锐 |
| Labels | P2, feature, good first issue, help wanted, roadmap-v3（milestone v3.3） |
| Status | ✅ ready（2026-10-01 检查；独立复审已修正 Pages 字节预算） |
| Base | `master` @ `a88fe2feb699fd1945d053859998e54e00237825` |
| 重复 PR 检查 | `pulls?q=3101` → 0 条；关键词 `coverage` / `language` 搜索仅见兄弟 issue 的 PR（#3617 readiness matrix → #3100，#3619 locale-pack conformance → #3103），无人做 #3101；issue 无 assignee、无评论、无关联分支/PR |

## 问题理解

Issue（v3.3 roadmap #3195 的一项，自动生成风格）要求：新建 `openmed/core/language_coverage_diff.py`，比较两个版本的语言包 coverage manifest（按 locale、script、identifier classes、surrogate support、evidence digest），确定性地输出 added/removed/improved/regressed 条目；验收：equal、added、removed、changed、alias、reordered 六类 manifest 有稳定 golden 输出；输出中不得含 fixture 文本、模型路径或原始评估样例；单测离线通过。文件：模块、`tests/unit/core/test_language_coverage_diff.py`、`docs/i18n/language-coverage-diffs.md`。

## 合理性判断

- 仓库现有代码里**没有**"language coverage manifest"格式（grep `coverage_manifest`/`surrogate_support`/`identifier_classes` 均无；`language_pack_coherence.py` 只有 pack 级 capability coverage report）。兄弟 issue #3100 的 PR #3617 定义的是 readiness matrix（不同的结构），尚未合并。因此本 PR 自定义了一个最小、封闭的 manifest 格式，并在 PR 描述里说明"可按维护者意见调整"。这是本 PR 最主要的设计风险点。
- 复用了仓库已有的 `openmed.core.locale_tag.normalize_locale_tag`（支持显式 aliases），满足 "alias" 验收项；错误风格仿照 `LocaleTagError`（常量 category、不回显值）。
- 仓库 AGENTS.md 允许 agent 贡献，但要求：**不得在 commit / PR 标题 / PR 正文 / 分支名中出现助手/工具/厂商名（特别是 codex、claude），不加 co-author trailer / 生成脚注**。因此 pr_body.md 的 motivation/disclosure 段落改成了 "an AI coding assistant"，没有写 "Claude Code"。
- 无 DCO 要求；commit 风格为简洁祈使句，部分带 `fix:` 前缀，新增功能常见 "Add ... (#issue)"。

## 改动

- `openmed/core/language_coverage_diff.py`（新）：`parse_language_coverage_manifest`、`diff_language_coverage`、`LanguageCoverageDiff.to_dict/to_json/to_markdown/counts/has_regressions`。
  - manifest 只允许 `version` + `entries`；entry 只允许 `locale`、`script`、`identifier_classes`、`surrogate_support`（none<partial<full）、`evidence_digest`（`sha256:`+64 hex）。未知键直接拒绝 → 保证无 fixture 文本/模型路径。
  - 按规范化 locale 排序，identifier classes 排序 → reordered 输出字节一致。
  - 状态：added / removed / regressed（丢失 identifier class 或 surrogate 等级下降，优先级最高）/ improved / changed（仅 script 或 digest 变化）；完全相同的进 `unchanged`。
- `tests/unit/core/test_language_coverage_diff.py`（新，24 个用例）：golden JSON + Markdown（混合场景）、equal、added-only/removed-only、reordered、alias/大小写、regression 优先、script-only、15 个错误类别参数化、输出键白名单。
- `docs/i18n/language-coverage-diffs.md`（新），并在 `mkdocs.yml` nav 与 `docs/brand/system/publication.yml` 的 `navigated` 中注册（`tests/unit/test_docs_publication.py` 强制两者一致且覆盖每个 md 页面）。
- `CHANGELOG.md`：Unreleased / Added 加一条。
- `tests/browser/brand/budgets.json`（复审追加）：新文档页让 Pages 产物增加约 238 KB（新页面 136 KB + 所有页面导航中多一项、sitemap/llms feed 等），超过现有预算余量（115486 字节总量、5792 字节搜索索引），`pages.yml` CI 的 "staged artifact respects recorded byte budgets" 会失败。按维护者在该文件中的既有做法：记录实测值 + 保留原有余量，新增一条 note。

## 验证

环境：`uv venv .venv -p 3.11` + `uv pip install -e . pytest pytest-timeout ruff==0.15.22 mypy==2.3.0 pyyaml`（未装完整 `.[dev]`，未装 torch）。

| 命令 | 结果 |
|---|---|
| 红：模块未添加时 `.venv/bin/python -m pytest tests/unit/core/test_language_coverage_diff.py -q` | ❌ collection error（ImportError） |
| 绿：`.venv/bin/python -m pytest tests/unit/core/test_language_coverage_diff.py -q` | ✅ 24 passed |
| `.venv/bin/python -m pytest -q tests/unit/core/test_language_coverage_diff.py tests/unit/test_docs_publication.py tests/unit/core/test_locale_tag.py` | ✅ 106 passed, 2 skipped（skip 为需 mkdocs 的 hook 测试） |
| `.venv/bin/python -m pytest -q tests/unit/test_docs_publication.py tests/unit/processing/test_zh_segmentation_docs.py` | ✅ 39 passed, 2 skipped |
| `.venv/bin/python -m pytest -q tests/unit/core -k "language or locale" --continue-on-collection-errors` | ✅ 664 passed, 1 skipped；11 个模块因缺可选依赖（numpy/jsonschema 等，未装 dev extra）无法收集，与本改动无关 |
| `ruff check .` / `ruff format --check .`（0.15.22，= `make lint` / `make format-check`） | ✅ All checks passed / 2663 files already formatted |
| `mypy`（仓库 scoped 配置）及 `mypy openmed/core/language_coverage_diff.py` | ✅ no issues |
| 文档中的 python 示例代码块实际执行 | ✅ |
| `git am` 到干净 base `a88fe2f` | ✅ 可直接应用 |

独立复审补充（2026-10-01）：

| 命令 | 结果 |
|---|---|
| 红：删除模块后 `pytest tests/unit/core/test_language_coverage_diff.py -q` | ❌ 1 error during collection |
| 绿：`pytest tests/unit/core/test_language_coverage_diff.py tests/unit/test_docs_publication.py tests/unit/core/test_locale_tag.py -q` | ✅ 106 passed, 2 skipped |
| `uv export --frozen --extra docs` 锁定版本装入 venv 后 `pytest tests/unit/test_docs_publication.py tests/unit/core/test_language_coverage_diff.py -q` | ✅ 36 passed（mkdocs hook 测试不再 skip） |
| base `a88fe2f`：`python scripts/docs/stage_pages.py --output-dir site-base` | ✅ total 92338263 / unique 91973750 / search 4437049 字节（低于预算） |
| 原补丁：`python scripts/docs/stage_pages.py --output-dir site-new` | ✅ 构建成功，但 total 92576423 > 预算 92448657、unique 92211910 > 92084144、search 4442825 > 4442708 → **CI 预算会失败** |
| 用 brand.spec.ts 的同等逻辑（Python 复刻）检查 site-new 对新 budgets.json | ✅ 全部 artifact / largest_file / governed 检查通过 |
| `ruff check .` / `ruff format --check .` | ✅ |
| `git am` 到 `a88fe2f` | ✅ |

未运行：完整 `pytest tests/`、`make brand-check`、Playwright 浏览器矩阵（route transfer 字节，仅新增一个 nav 项，预计影响很小）。

## 如何提交

```bash
git clone https://github.com/<you>/openmed.git && cd openmed
git remote add upstream https://github.com/maziyarpanahi/openmed.git
git fetch upstream && git checkout -b language-coverage-diff-3101 upstream/master
git am /path/to/0001-Add-deterministic-language-coverage-manifest-diffs-3.patch
uv run --frozen --extra dev pytest tests/unit/core/test_language_coverage_diff.py tests/unit/test_docs_publication.py -q
git push origin language-coverage-diff-3101
# PR 标题见 pr_title.txt，正文见 pr_body.md，目标分支 master
```

## 需要提交者注意

- **AGENTS.md 禁止在 PR 标题/正文/commit/分支名中出现 claude/codex 等工具名**：pr_body.md 已用 "an AI coding assistant" 代替；分支名不要带 claude。不要加 Co-Authored-By。
- manifest 格式是本 PR 自定的（仓库中尚无），维护者可能希望与 #3100（PR #3617 readiness matrix）或 #3103 的结构对齐；若 #3617 先合并，可能需要调整。
- 若 master 在提交前又改了 `mkdocs.yml` nav 或 `publication.yml` 的 locale-tags 附近，可能需要手动解决小冲突（两处顺序必须一致）。
- `tests/browser/brand/budgets.json` 已按本地实测值调整（本地 base 构建比维护者记录值多约 5 KB，属环境差异，新上限仍有约 110 KB 余量）。若 master 先合并了其它文档改动导致冲突，需要按同样方式（实测值 + 115486 / 5792 余量）重新计算这三个数字并更新 note。
- 自动生成 roadmap 风格的 issue，作者是维护者本人；兄弟 issue 的外部 PR（kokokoXUY）仍 open 未合并，说明维护者对外部 PR 的接受度未知。
