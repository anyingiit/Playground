## Description

The import-graph cross-reference (`xref-*.html`) and the GraphViz graph (`graph-*.dot`) in the work directory were named after the spec file (`CONF['specnm']`). When a spec file contains several `Analysis` instances (for example a multipackage bundle using `MERGE`), every `Analysis` wrote to the same two files, so only the graph of the last one survived.

As proposed in the issue, `Analysis._write_graph_debug()` now names the files after the (first) script of that `Analysis`: `build/<specname>/xref-<script>.html` and `build/<specname>/graph-<script>.dot`.

- For the usual case (`pyinstaller foo.py` → `foo.spec`), the script and spec names are the same, so the file names do not change. They only change when the spec name differs from the script name (e.g. `--name`), or when the spec has several `Analysis` instances.
- The `CONF['xref-file']` / `CONF['dot-file']` entries are no longer used and are removed. The two existing regression tests that set them in their fake `CONF` are updated.
- `doc/when-things-go-wrong.rst` documents the new names, and `news/5502.feature.rst` is added. I used the issue number for the fragment; I can rename it to the PR number if you prefer.
- Not changed: `warn-<specname>.txt` is still per spec file. The issue only asks about the xref/dot files, and the warn file name is also passed to the bootloader via `WARNFILE`.

With the example from the issue (two `Analysis` + `MERGE`, `--log-level DEBUG`), the build directory now contains `xref-a.html`, `xref-b.html`, `graph-a.dot` and `graph-b.dot`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #5502

## Checklist

- [x] Tests pass locally (Linux, Python 3.11)
  - New `tests/functional/test_regression.py::test_issue_5502` runs two `Analysis` instances in one work directory and checks that each gets its own xref/dot file. It fails on `develop` and passes with this change.
  - `pytest -n 2 tests/functional/test_multipackage.py tests/functional/test_regression.py`: 13 passed
  - `pytest -n 2 tests/unit`: 324 passed, 22 skipped, 11 xfailed, 1 failed. The failure is `test_pyimodulegraph.py::test_metadata_searching` (`PackageNotFoundError: pyinstaller`). It fails the same way on `develop` because I ran from the source tree without installing the package.
  - `yapf --recursive --parallel --diff .` (no diff), `flake8 .` (clean)
- [x] `CHANGELOG.md` is updated (if applicable) — `news/5502.feature.rst`
- [x] Documentation is updated (if applicable) — `doc/when-things-go-wrong.rst`
