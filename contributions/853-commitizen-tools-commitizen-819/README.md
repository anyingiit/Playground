# commitizen-tools/commitizen#819 — FAQ：依赖版本与项目版本相同时被 version_files 误改

| 项 | 值 |
|---|---|
| Issue | https://github.com/commitizen-tools/commitizen/issues/819 |
| Tier | 自由 |
| Labels | good first issue, issue-status: wait-for-implementation, type: documentation |
| Status | ✅ ready — patch + PR text done (not submitted)；独立复审 2026-10-01：red→green（变异 bump.py 后 1 failed → 恢复后 2 passed）、ruff、mkdocs --strict 均复现通过，无新的重复 PR |
| Base | `master` @ 642b8beb81a8fe5d50a805b168bede25a3563eea (2026-09-25) |
| Duplicate-PR check | 2026-10-01：`pulls?q=819` 仅有 #1910（作者自己于 2026-04-15 关闭，未合并、无 review 评论）；`faq dependency`、open `version_files` 关键词搜索无相关 PR；issue 无评论、未指派 |

## 问题理解

维护者 Lee-W 开的 issue：把 #496 中的解答（依赖恰好和项目同版本时，`version_files` 的正则替换会把依赖版本一起改掉；可用 `^` 锚定正则或改用 `version_provider`）写进 FAQ，并链接到文档其它部分。`docs/faq.md` 目前没有这一条。

核对代码 `commitizen/bump.py::update_version_in_files`：逐行读取文件，`pattern.search(line)` 命中的行上 `line.replace(current_version, new_version)`；没有给 pattern 时用 `re.escape(version)`。所以：
- `pyproject.toml:version` 会改到 `foo = { version = "1.2.3", ... }` 这种依赖行；
- 因为是逐行匹配，`^version` 确实只匹配行首为 `version` 的行（不需要 MULTILINE）；但 `[tool.poetry.dependencies.foo]` 子表下的 `version = "1.2.3"` 仍会命中——#1910 的文案说“只匹配项目版本”不够准确，本补丁注明了这个限制。
- `version_provider = "poetry"/"pep621"/...` 通过 tomlkit 只写项目自身的版本字段。

#1910 关闭原因：作者本人关闭，页面上没有任何说明或 review 意见（推测是久未 review 后自行清理）。本补丁避免其问题：说明根因（逐行匹配）、注明 `^` 锚定的残留情况、文案更短、并加测试佐证；没有用 `###` 小标题（FAQ 页其它条目都是单个 `##`）。

## 合理性判断

- 维护者自己提出、标 `good first issue` + `wait-for-implementation`，纯文档，无需设计讨论。
- AI 政策：仓库有 `AGENTS.md`（面向 agent），`docs/contributing/pull_request.md` 欢迎 AI 辅助，但要求：PR 描述中声明 AI 使用、贡献者能解释每一行、不要复制粘贴 AI 回复到评论。PR 模板有 “Was generative AI tooling used” 勾选 + `Generated-by:` 行，已填写。

## 改动

- `docs/faq.md`：新增 “How to avoid bumping a dependency that has the same version as my project?”，解释逐行匹配行为，给出两种方案（推荐 version provider；或 `^` 锚定）并注明锚定的局限，链接 `config/bump.md#version_files`、`config/version_provider.md`、#496。
- `tests/test_bump_update_version_in_files.py`：新增参数化测试 `test_anchored_regex_skips_dependency_with_same_version`（`version` → 依赖被改；`^version` → 依赖不变）。

## 验证

环境：`uv sync --frozen --group base --group test --group linters --group documentation`（UV_CACHE_DIR / venv 在 clone 内，已删除）。

| 命令 | 结果 |
|---|---|
| `pytest -q tests/test_bump_update_version_in_files.py` | 18 passed |
| red：临时把 `bump.py` 中 `if pattern.search(line)` 改成 `if current_version in line`（即忽略正则），`pytest -k anchored` | **1 failed**（`^version-False`），1 passed |
| green：恢复 `bump.py`，`pytest -k anchored` | 2 passed |
| 说明 | 这是文档类改动，测试是对文档所述行为的“行为锁定”，在 master 上本来就通过；red 通过变异证明测试确实能捕获“正则不起作用”的情况 |
| 手动：临时 git 仓库 + `cz bump --yes --files-only 2.0.0`，`version_files = ["pyproject.toml:^version"]` | `tool.poetry.version` → 2.0.0，依赖 `foo` 保持 1.2.3 |
| 同上，改成 `pyproject.toml:version` | 依赖 `foo` 也被改成 2.0.0（复现问题） |
| 同上，`version_provider = "poetry"`、无 version_files | 仅 `tool.poetry.version` 变化 |
| `ruff check .` / `ruff format --check .` / `mypy` | All checks passed / 118 files already formatted / no issues in 116 files |
| `uvx codespell docs/faq.md tests/test_bump_update_version_in_files.py` | 无输出（通过） |
| `mkdocs build --strict`（`poe doc:build`） | 成功，无 warning；faq 页面中三个链接均解析正确 |
| `pytest -n 2 --dist=loadfile -q`（CI 用 `-n auto`） | 1318 passed, 2 xfailed, 1 failed：`tests/test_git.py::test_get_commits_with_signature` —— 在不含补丁的 master 上同样失败（浅克隆缺历史，`Invalid revision range bec20eb..9eae518`），与本补丁无关 |
| `cz check --message "$(git log -1 --format=%B)"` | Commit validation: successful! |

## 如何提交

```bash
git clone https://github.com/commitizen-tools/commitizen && cd commitizen
git checkout -b docs/faq-dependency-same-version origin/master
git am /path/to/0001-docs-faq-explain-how-to-avoid-bumping-a-dependency-w.patch
git push <your-fork> docs/faq-dependency-same-version   # PR 目标分支: master
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`（已按仓库 `.github/pull_request_template.md` 填写）。

### 需要提交者注意
- 提交信息为 Conventional Commits（`docs(faq): ...`，`docs` 不触发发版），PR 标题与之相同（squash 时作为提交信息）。无 DCO；CHANGELOG 由 `cz bump` 自动生成，无需手改。
- 仓库要求 AI 辅助的 PR：在描述中声明（已写，并勾选模板的 AI 项 + `Generated-by: Claude Code`）；**提交者需亲自读懂并能解释改动**，回复 review 时不要直接粘贴 AI 生成的回复（`docs/contributing/pull_request.md`）。
- 维护者的 AGENTS.md / 模板要求本地跑 `uv run poe all`；这里分开跑了 ruff/mypy/pytest/mkdocs（`poe all` 中的 `check-commit` 需要 `origin/master`，提交前在完整 clone 中可再跑一次）。
- 前一个 PR #1910 由作者自行关闭、无说明；如维护者在 issue 中另有意见，请先看 issue 最新状态。
