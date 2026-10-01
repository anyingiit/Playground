# Audit — plotly/plotly.py @ d586d225b8577fa3a4ff8954bdd47ef3b9cc0c07

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/plotly.py` (1712 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/test_optional/test_px/conftest.py` (auto-runs under pytest) | Read in full: only defines dataframe-constructor fixtures (pandas / polars / pyarrow) and a `backend` fixture | benign |
| `tests/test_io/test_deepcopy_pickle.py:90,97,111` `pickle.loads(pickle.dumps(...))` | Round-trips locally built figures in-memory; no external data | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| Build backend | `hatchling` (pyproject.toml); no custom setup.py hooks run for `pip install -e .` beyond hatch build | benign |

Verdict: nothing suspicious; safe to install and run the px tests.
