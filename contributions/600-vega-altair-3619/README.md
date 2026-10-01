# vega/altair#3619 — `PluginRegistry` persists unregistered plugins

| 项 | 值 |
|---|---|
| Issue | https://github.com/vega/altair/issues/3619 |
| Tier | 高星 |
| Labels | bug |
| Status | ✅ ready — patch + PR text 已完成 |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论认领；`/pulls?q=3619` 仅 #4086（作者删除 fork 后关闭，未合并）及无关的 #3618/#3591 |
| AI 政策 | CONTRIBUTING / PR 模板 / labels 均无 AI 相关限制 |

## 问题理解
`PluginRegistry.register(name, None)`（注销）只从 `_plugins` 删除，若该插件正处于激活状态，`_active/_active_name/_options` 仍指向已删除插件；`alt.theme.unregister` 直接 pop `_themes._plugins`，同样问题。结果 `theme.active` 仍返回已注销主题，`theme.enable()` 报 NoSuchEntryPoint。

## 合理性判断
维护者 (dangotbanned) 自己提的 bug，并在 `tests/vegalite/v6/test_theme.py` 留了 `# BUG: #3619` 注释掉的断言；issue 期望“重置为 default”。合理。

## 改动
- `altair/utils/plugin_registry.py`：注销激活插件时调用新 `_reset_active()`：存在 `"default"` 则 enable 它，否则清空 active/options。docstring 加 Notes。
- `altair/theme.py`：`_register(name, None)` 改走 `_themes.register(name, None)`。
- 测试：`tests/utils/test_plugin_registry.py` 新增 2 个测试；`test_theme_unregister` 启用 `theme.active == "default"` 断言。

## 验证（Python 3.11，uv venv + pytest/ruff/mypy/pandas/polars/pyarrow/ipython/ipywidgets/anywidget）
- Red（stash 源码改动）：3 failed（2 新测试 + test_theme_unregister）, 31 passed
- Green：`pytest tests/utils/test_plugin_registry.py tests/vegalite/v6/test_theme.py` → 34 passed
- `pytest -n 3 tests/utils tests/vegalite -m "not slow and not datasets_debug and not no_xdist"` → 520 passed, 11 skipped, 1 xfailed, 1 xpassed
- `-m no_xdist` 在 tests/utils+vegalite 中无用例
- `ruff check` ✓，`ruff format --diff --check` ✓，`mypy altair/utils/plugin_registry.py altair/theme.py tests/utils/test_plugin_registry.py` ✓
- 未运行：完整 `uv run task test`（全量 mypy/ty、tests/ 其他目录、slow 测试；需 vl-convert 等重依赖）

## 需要提交者注意
- 仓库要求 Conventional Commits，已用 `fix: Reset ...`（与仓库首字母大写风格一致）。
- 无 DCO、无 AI trailer 要求；PR body 已含披露段落。
- 行为选择：无 `"default"` 插件时清空 active（`active == ""`, `get() is None`），与新建 registry 的初始状态一致；如维护者偏好其他行为可再调整。
- 曾有 #4086 做同样修复，被作者自行关闭（删库），可在 PR 中提一句（已写）。

## 如何提交
基于 `main`：
```
git clone https://github.com/vega/altair && cd altair
git checkout -b fix/plugin-registry-unregister-active
git am /path/to/600-vega-altair-3619/0001-*.patch
```
或：
```
tools/submit_pr.sh contributions/600-vega-altair-3619 vega/altair main fix/plugin-registry-unregister-active contributions/600-vega-altair-3619/pr_title.txt contributions/600-vega-altair-3619/pr_body.md
```

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。
