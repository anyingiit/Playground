# WeblateOrg/weblate#21853 — Status badges should have blurred shadow to match shields.io

| 项 | 值 |
|---|---|
| Issue | https://github.com/WeblateOrg/weblate/issues/21853 |
| Tier | 高活跃高Star |
| Labels | Area: UX, Waiting for: Implementation, good first issue (Type: Feature) |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01：issue 无评论、无 assignee；PR 搜索 `21853` / `badge shadow` 无相关 PR |
| Base | `main` @ bdc9c3dbc7052408e1ffac3a962225571254fd77 |

## 问题理解
shields.io 在徽章文字后加了模糊阴影（改善 WCAG 对比度），Weblate 的 SVG 状态徽章（`weblate/templates/svg/badge.svg`）仍是旧样式（只有 1px 清晰阴影）。

## 合理性判断
维护者已打 `Waiting for: Implementation` + `good first issue` 并放进 milestone，属于明确接受的需求。参考 shields.io `badge-maker/lib/badge-renderers.js`（flat 风格）：阴影 y+1，模糊文字 `fill-opacity .8` + `filter=url(#blur)`（`feGaussianBlur stdDeviation=16`，因其文字 10× 缩放，等价我们的 1.6），清晰阴影 `fill-opacity .3`，阴影组 `aria-hidden="true"`。
（shields 还有浅色背景用深色文字的逻辑，不在本 issue 范围内，未改。）

## 改动
- `weblate/templates/svg/badge.svg`：加 `<filter id="b"><feGaussianBlur stdDeviation="1.6"/></filter>`；label/value 各加一层模糊阴影，阴影放进 `aria-hidden` 组。尺寸、位置不变。影响 `svg` 状态徽章和 language badge（都用 `BaseSVGBadgeWidget`）。
- `weblate/trans/tests/test_widgets.py`：新增 `WidgetsTest.test_svg_badge_text_has_blurred_shadow`。
- `docs/changes.rst`：2026.10.1 Improvements 增加一条（AGENTS.md 要求用户可见改动写 changelog）。

## 验证
环境：uv 同步 `--group test --extra postgres`（Python 3.13），本地 PostgreSQL 16 + redis。
```
CI_DB_HOST=localhost CI_DB_PASSWORD=postgres DJANGO_SETTINGS_MODULE=weblate.settings_test \
  python -m pytest weblate/trans/tests/test_widgets.py -k svg_badge_text_has_blurred_shadow
```
- 红：改模板前 → `AssertionError: 0 != 1`（无 blur filter），1 failed
- 绿：改模板后 → `pytest -n 3 weblate/trans/tests/test_widgets.py`：**293 passed, 151 subtests passed**
- `ruff check` + `ruff format --check`（0.16.9，与 pre-commit 同版本）通过；`xmllint --noout badge.svg` 通过；codespell 无问题
- 未运行：完整测试套件、整套 pre-commit（只跑了相关子集）；未做像素级渲染比对（本机 ImageMagick 无 SVG delegate）

## 需要提交者注意
- Weblate 的 AI 政策（docs/contributing/issues.rst）只针对 AI 生成的 issue 报告要求披露；未禁止 AI 辅助 PR，且仓库有 AGENTS.md。PR body 已含披露段落。
- 不需要 DCO / Signed-off-by。
- 提交信息遵循 Conventional Commits，含 `Fixes #21853`（AGENTS.md 要求）。
- 建议提交前在浏览器里打开一个渲染后的徽章（如 `/widget/<project>/svg-badge.svg`）目测一下效果。
- `docs/changes.rst` 顶部未发布段落如已变化，`git am` 可能冲突，手动放到当前未发布版本的 Improvements 下即可。

## 如何提交
```bash
git clone https://github.com/anyingiit/weblate.git && cd weblate   # 先在 GitHub 上 fork WeblateOrg/weblate
git remote add upstream https://github.com/WeblateOrg/weblate.git && git fetch upstream
git checkout -b feat/badge-blurred-shadow upstream/main
git am /path/to/0001-feat-widgets-add-blurred-text-shadow-to-SVG-status-b.patch
git push origin feat/badge-blurred-shadow
gh pr create --repo WeblateOrg/weblate --head anyingiit:feat/badge-blurred-shadow \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
feat(widgets): add blurred text shadow to SVG status badges

## PR body
见 `pr_body.md`。
