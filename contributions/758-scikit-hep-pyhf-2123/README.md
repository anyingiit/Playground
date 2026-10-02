# scikit-hep/pyhf #2123 — Migrate tbump.toml to pyproject.toml

| 项 | 值 |
|---|---|
| Issue | https://github.com/scikit-hep/pyhf/issues/2123 |
| Tier | 自由 |
| Labels | chore, feat/enhancement, good first issue, packaging |
| Status | ✅ ready — patch + PR 文本已就绪（2026-10-01） |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论、无关联 PR；`pulls?q=2123` 0 结果；`pulls?q=tbump` 只有 matthewfeickert 的 6 个已关闭 PR（最新 #2743 release 流程加固，2026-08-14 合并，保留了 tbump.toml，未提及 #2123）。anyingiit 在该仓库无 PR。 |
| Base | `main` @ efa6eb09（2026-09-17） |

## 问题理解
维护者 kratsg 开的 issue，正文只有 "See title. Just migrate over."：把根目录 `tbump.toml` 的配置迁到 `pyproject.toml` 的 `[tool.tbump]` 下，然后删掉 `tbump.toml`。

## 合理性判断
- tbump 6.x 原生支持 `[tool.tbump]`（本地 tbump 6.11.0 已验证，仓库 dev 组要求 `tbump>=6.7.0`）。release-prepare 用的是 `uvx tbump`，会自动读取 pyproject，workflow 命令本身不用改。
- #2743（2026-08 合并）重写了发布流程，`ci/validate-version.py` 和 `release-tag.yml` 直接读 `tbump.toml`。只搬配置不改这两处的话，下次发布会直接 `FileNotFoundError`，所以这两处也一起改了。
- 不涉及运行时代码，也不影响 hatch 打包：sdist 只包含 `/src` 和 `CITATION.cff`，hatchling 本来就会带上 pyproject。

## 改动
- `pyproject.toml`：在 `[tool.hatch.build.targets.wheel]` 后面新增 `[tool.tbump]`、`[tool.tbump.version]`、`[tool.tbump.git]`、7 个 `[[tool.tbump.file]]` 和 `[[tool.tbump.field]]`，内容和注释原样迁移。自引用的 `src = "tbump.toml"` 改成 `src = "pyproject.toml"`，并保留 `search = "Bump version: {current_version} → "`，确保 pyproject 里只有 message_template 这一行会被 bump。注释 "relative to the tbump.toml location" 改为 pyproject.toml。
- 删除 `tbump.toml`。
- `ci/validate-version.py`：改为读取 `pyproject.toml` 的 `["tool"]["tbump"]["version"]`，错误信息改成 "tbump release version format"。
- `.github/workflows/release-tag.yml`：头部注释、步骤名 "Read version from pyproject.toml"，以及 tomllib 单行命令。
- `.github/workflows/release-prepare.yml`：自动生成的 PR 正文措辞。
- `docs/development.rst`（4 处，含链接）和 `.github/ISSUE_TEMPLATE/~release-checklist.md`（patch release forward-port 一项）。
- 改完后 `git grep tbump.toml` 没有任何结果。

## 验证（venv：tbump 6.11.0、prek、packaging；Python 3.12）
这是纯配置迁移，pyhf 的 pytest 体系里没有合适放配置测试的位置（加一个读 pyproject 的测试反而显得多余），所以没有往仓库里加测试文件。改为用下面的前后对比证明 red→green：
- **前后等价**：在 base 上运行 `tbump current-version` → `0.7.6`，再运行 `tbump --only-patch --non-interactive 0.7.7` 并保存 `git diff`。在本分支上做同样操作。结果都是 7 个文件、19+/19−，内容完全一致，只是两行自 bump（`current`、`message_template`）从 tbump.toml 移到了 pyproject.toml。pyproject 里没有其他行被改（例如 `tbump>=6.7.0` 没动）。`0.8.0rc1` 的结果相同。
- **Red**：在迁移后的树上运行旧版 `ci/validate-version.py 0.7.7`，以及旧的 release-tag 单行命令，都报 `FileNotFoundError: 'tbump.toml'`。在 base 的 pyproject 上、没有 tbump.toml 时运行 tbump，报 `Invalid config: 'Key "tbump" does not exist.'`。
- **Green**：`uv run ci/validate-version.py 0.7.7` → `Bumping version: 0.7.6 -> 0.7.7`；`0.8.0rc1` 通过；`v0.7.7` → "does not match the tbump release version format"；`0.7.6` → not newer；`0.7.07` → not canonical。新的单行命令 `python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["tool"]["tbump"]["version"]["current"])'` 输出 `0.7.6`。
- **Lint**：`PREK_HOME=... prek run --files <改动的文件>` 全部 Passed（check-toml/yaml、codespell、rst-*、ruff、blacken-docs、check-github-workflows）。zizmor 的在线审计访问 api.github.com 时 403（环境原因）。改用 `zizmor --offline` 跑两个 workflow，HEAD 和 base 都是 "No findings"。
- `git am` 在干净的 base 上能干净应用（已用 worktree 验证）。
- **没有运行**：完整 pytest（与改动无关），Sphinx 文档构建（rst 由 prek 的 rst 钩子检查过）。

## 需要提交者注意
- 仓库没有 AI 政策，不需要 DCO/CLA，没有 changelog fragment（release notes 每次发布手写）。
- PR 正文按仓库自己的 PR 模板组织（Description / Checklist Before Requesting Reviewer / Before Merging），同时插入了 disclosure 段落、Closes #2123 和 changelog/docs 两项。"Selected an Assignee" 外部贡献者勾不了，保持未勾。
- CONTRIBUTING 要求单 commit 的 PR，这里就是一个 commit。标题符合 semantic PR 检查（`chore:`）。
- 如果维护者已经有正在进行中的 release 分支（`release/vX.Y.x`），那个分支上仍然是 tbump.toml。之后 forward-port 时要注意，正文里不用特别说明。

## 如何提交
```bash
git clone https://github.com/scikit-hep/pyhf && cd pyhf
git checkout -b chore/migrate-tbump-to-pyproject origin/main
git am /home/user/Playground/contributions/758-scikit-hep-pyhf-2123/0001-chore-Migrate-tbump-configuration-to-pyproject.toml.patch
uvx tbump current-version   # 应输出 0.7.6
uvx prek run --files $(git diff --name-only HEAD~1)
git push -u <your-fork> chore/migrate-tbump-to-pyproject
gh pr create --repo scikit-hep/pyhf --head anyingiit:chore/migrate-tbump-to-pyproject \
  --title "$(cat /home/user/Playground/contributions/758-scikit-hep-pyhf-2123/pr_title.txt)" \
  --body-file /home/user/Playground/contributions/758-scikit-hep-pyhf-2123/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`

## 独立复审（r2 review，2026-10-01）
- upstream `main` 仍为 efa6eb09；`pulls?q=tbump` 仍只有 matthewfeickert 的已关闭 PR，无重复。
- `git apply --check` 在干净 base worktree 上通过；commit 作者为 anyingiit，无 AI 模型名。
- 复现：`uvx --from tbump==6.11.0 tbump --only-patch --non-interactive 0.7.7` 在 base 与打补丁后均为 7 files 19+/19−，除自 bump 的两行（`current`、`message_template`）从 tbump.toml 移到 pyproject.toml 外其余 diff 完全相同；pyproject 中无其他行被改动。
- `python3 ci/validate-version.py 0.7.7` → `Bumping version: 0.7.6 -> 0.7.7`；`v0.7.7` 被拒。
- `git grep tbump.toml` 无残留。结论：无需修改，保持 ✅ ready。
