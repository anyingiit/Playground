# scikit-hep/hist #237 — docs: copy mplhep.histplot docstring to .plot()?

| 项 | 值 |
|---|---|
| Issue | https://github.com/scikit-hep/hist/issues/237 |
| Tier | 自由 |
| Labels | enhancement, good first issue |
| Status | ✅ ready — 已通过独立复审（2026-10-01），patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=237+is:pr` 只搜到无关的 #710（依赖升级）。issue 没有 linked PR，无人分配，没有评论。 |
| Base | scikit-hep/hist `main` @ 52303af |

## 问题理解
`Hist.plot()` 的 docstring 只有一句 "Plot method for BaseHist object."。用户从 `help()` 或 API 文档里看不出可以传哪些参数（这些参数实际都转发给 mplhep.histplot / hist2dplot）。mplhep 维护者 @andrzejnovak 开了这个 issue，建议把 histplot 的说明带到 `.plot()` 上。

## 合理性判断
- issue 带 good first issue 标签，属于 PyHEP 2022 Hackashop 项目，至今没人做。
- 没有逐字复制 mplhep 的整段 docstring：那样太长，而且会随 mplhep 版本变化而过时（hist 要求 mplhep>=0.3.33，最新是 1.3.3，中间参数变化很大）。改为写一个精简的 numpy 风格 docstring，列出常用参数，完整列表指向 mplhep 文档。PR 正文里说明了这样取舍的原因。
- 只改 docstring，没有改任何运行时代码。

## 改动
只改了 `src/hist/basehist.py`：
- `BaseHist.plot`：新写 numpy 风格 docstring，内容包括：
  - 分派规则：1D、"1 连续 + 1 分类"的 2D、或给了 overlay 时走 plot1d/histplot；其它 2D 走 plot2d/hist2dplot；>2D 抛 NotImplementedError
  - `*args`、`overlay`、`**kwargs`（含 `ls`/`*_ls` 别名）
  - 常用 histplot 参数：histtype、yerr、w2method、stack、density/binwnorm、flow、label、sort
  - 常用 hist2dplot 参数：cbar、cmin/cmax、labels、flow
  - Returns 和 Raises 两节
- `plot1d`：`**kwargs` 的说明改为明确转发给 `mplhep.histplot`。
- `plot2d`：补上 Parameters 和 Returns 两节。
- mplhep 函数用双反引号引用，没有用 `:func:`，因为 docs/conf.py 的 intersphinx 里没有配置 mplhep。

## 验证
纯文档改动，不存在 red→green。下面证明全部检查通过，并且文档里写到的参数都真实存在、可以运行：
```bash
cd /home/user/work/hist; export UV_CACHE_DIR=$PWD/.uvcache UV_PROJECT_ENVIRONMENT=$PWD/.venv
uv sync --group test                                   # mplhep 1.3.3, matplotlib
.venv/bin/python -c "import mplhep,inspect; print(inspect.signature(mplhep.histplot)); print(inspect.signature(mplhep.hist2dplot))"  # 逐个核对参数名
uv run pytest -q --mpl                                 # 315 passed, 1 skipped (uproot 未安装)
uv run pytest tests/test_plot.py tests/test_general.py -q --mpl   # 84 passed
uv run python -c "import hist; help(hist.Hist.plot)"   # 渲染正常
uv run --with sphinx python -c "...NumpyDocstring(inspect.getdoc(hist.Hist.plot))..."  # napoleon 解析正常（plot/plot1d/plot2d）
uv run --with sphinx sphinx-build -W -b html <scratch>  # 最小工程：autodoc+napoleon，automethod plot/plot1d/plot2d，-W 下 0 警告
uvx prek run --files src/hist/basehist.py              # ruff/ruff-format/mypy/codespell/blacken-docs 等全部 Passed
```
冒烟脚本（warnings 视为 error）逐个调用了文档列出的参数：histtype=errorbar/fill/step、yerr=True、w2method="sqrt"、flow="none"/"hint"、ls="--"、stack、sort="yield"、label=[...]、binwnorm=1、cbar=False、cmin/cmax、labels=True。3D 直方图调用 plot() 抛 NotImplementedError。结果 SMOKE_OK。

**没有运行**：完整的 `nox -s docs`。它需要 pandoc、graphviz，并会执行 notebook。

## 需要提交者注意
- 独立复审：原 patch 把 `plot1d` 的 `overlay` 说明从 "Name or index" 改成了 "Name"，但整数下标实际可用（`h.plot1d(overlay=1)`、`h.plot(overlay=1)` 都能运行），所以复审时撤回了这一处改动。复审在 base 上 `git am` 干净应用；`pytest -q --mpl` 315 passed / 1 skipped；`prek run --files src/hist/basehist.py` 全部通过。
- AI 政策：AGENTS.md 只是给 agent 的说明，没有禁止 AI，只要求 agent 未经要求不 commit/push（这里只在本地生成 patch）。CONTRIBUTING 没有 AI 条款。没有 PR 模板，不需要 DCO，也不需要 Assisted-by。
- changelog：docs/changelog.md 的条目带 PR 编号（有 "Documentation:" 分节）。这次没有改，PR checklist 里说明了可以等拿到 PR 号后补一行。
- 发现一个已有 bug（没有修，PR 正文里提到了）：2D 带分类轴的直方图调用 `h.plot(histtype="errorbar")` 且不传 `ax` 时，报 `AttributeError: 'ErrorBarArtists' object has no attribute 'stairs'`（basehist.py plot1d 的 legend 分支）。base 上同样能复现。可以另开 issue 或 PR。

## 如何提交
```bash
git clone https://github.com/scikit-hep/hist && cd hist
git checkout -b docs/plot-docstring origin/main
git am /home/user/Playground/contributions/114-scikit-hep-hist-237/0001-docs-document-plot-dispatch-and-common-mplhep-kwargs.patch
pytest -q && prek run --files src/hist/basehist.py
```
或者：
```bash
tools/submit_pr.sh contributions/114-scikit-hep-hist-237 scikit-hep/hist main docs/plot-docstring contributions/114-scikit-hep-hist-237/pr_title.txt contributions/114-scikit-hep-hist-237/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
