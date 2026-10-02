## Description

`Hist.plot()` used to have the one-line docstring "Plot method for BaseHist object.", so `help(h.plot)` and the API docs did not say which options it takes. All of those options are forwarded to `mplhep.histplot` / `mplhep.hist2dplot`.

For #237, this adds a numpy-style docstring to `BaseHist.plot` instead of copying the whole mplhep docstring, which would be long and would drift out of date across the supported mplhep versions. It covers:

- how `plot()` chooses between `plot1d` (wraps `mplhep.histplot`) and `plot2d` (wraps `mplhep.hist2dplot`), and when it raises `NotImplementedError`
- `overlay`, `*args` and `**kwargs`, including the `ls`/`*_ls` linestyle aliases
- a short list of the most used `mplhep.histplot` options (`histtype`, `yerr`, `w2method`, `stack`, `density`/`binwnorm`, `flow`, `label`, `sort`) and `mplhep.hist2dplot` options (`cbar`, `cmin`/`cmax`, `labels`, `flow`), with a pointer to the mplhep docs for the full list
- Returns and Raises sections

It also fills in the `plot2d` docstring and makes the `**kwargs` entry of `plot1d` name `mplhep.histplot`. The mplhep functions are referenced with double backticks rather than `:func:` because `docs/conf.py` has no mplhep intersphinx mapping. Every option listed was checked against the signature of the installed mplhep (1.3.3). The `histtype` and `flow` values are worded so they also make sense for older mplhep versions within the `>=0.3.33` range. This is a docstring-only change.

While testing I noticed a separate, existing bug that this PR does not change: `h.plot(histtype="errorbar")` on a 2D histogram with a categorical axis, called without `ax=`, fails with `AttributeError: 'ErrorBarArtists' object has no attribute 'stairs'`. The error comes from the legend code in `plot1d`, and it also happens on `main`. I'm happy to open a separate issue or PR for it if that's useful.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #237

## Checklist

- [x] Tests pass locally (`pytest -q --mpl`: 315 passed, 1 skipped (uproot not installed); `prek run --files src/hist/basehist.py`: all hooks pass, including ruff, ruff-format, mypy, codespell and blacken-docs)
- [x] Docstrings render: `help(hist.Hist.plot)`, napoleon `NumpyDocstring` and a minimal `sphinx-build -W` with `automethod` for `plot`/`plot1d`/`plot2d` all succeed with no warnings. The full `nox -s docs` was not run (it needs pandoc/graphviz and executes notebooks).
- [x] Every listed kwarg was exercised in a smoke script (`histtype`, `yerr`, `w2method`, `flow`, `ls`, `stack`, `sort`, `label`, `binwnorm`, `cbar`, `cmin`/`cmax`, `labels`), and the >2D `NotImplementedError` was checked
- [ ] `docs/changelog.md` is updated (if applicable). Not done: the entries reference PR numbers, so I can add a "Documentation" line once this PR has a number, if you'd like one.
- [x] Documentation is updated (if applicable): this PR is the docstring update.
