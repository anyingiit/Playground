# Malicious-code audit — sktime/sktime @ 80ea2ef (main, 2026-09-27)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/sktime` (1977 text files scanned), then manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `conftest.py` (root, auto-run by pytest) | only adds `--matrixdesign` / `--only_changed_modules` / `--only_vm_estimators` options and sets flags in `sktime.tests._config` | benign |
| `sktime/datasets/setup.py` | legacy numpy.distutils data-dir config listing bundled datasets; not used by the hatch/setuptools build via `pyproject.toml`, not executed here | benign |
| `.pre-commit-config.yaml` | standard hooks: pre-commit-hooks, ruff-format/ruff-check, check-manifest (manual), shellcheck | benign |
| 18 × `pickle.loads` (`sktime/base/_base.py`, `_serialize.py`, DL `_base_tf.py`, cinn, neuralprophet, tests) | estimator (de)serialisation API (`save`/`load_from_serial`), only deserialises data the user/test itself produced | benign |
| npm lifecycle hooks / committed binaries | none | — |
| `.github/PULL_REQUEST_TEMPLATE.md` / issue templates: hidden HTML comment asking LLMs to label content | project policy text (disclosure request), not code; handled in README "需要提交者注意" | benign |

Code actually executed locally: `pip install -e .` (pyproject build, no custom hooks) + `numba`, `pytest` on `sktime/tests/test_all_estimators.py`, `sktime/tests/tests/test_test_utils.py` and `sktime/transformations/tests/test_intervals.py`, `check_estimator`, `ruff`.

Verdict: **no malicious code found**; safe to install and run tests in an isolated venv under /home/user/work/sktime.
