# AUDIT — plotly/plotly.py (clone of main @ 0de8a381c36511a23b2ca7b6295f1a4bc72af434, 2026-10-22)

`python3 -I tools/audit_repo.py <clone>` → 1713 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Build backend | `pyproject.toml`: hatchling, only include/exclude + wheel shared-data (labextension files); no setup.py, no custom build hooks | benign |
| `tests/test_optional/test_px/conftest.py` (auto-runs) | only defines dataframe-constructor fixtures (pandas / polars / pyarrow); no I/O, network or subprocess | benign |
| npm lifecycle hooks | none flagged (js/ is not built or installed for these tests) | benign |
| Committed binaries | none | benign |
| `pickle.loads(pickle.dumps(fig))` in `tests/test_io/test_deepcopy_pickle.py` | round-trips an in-memory figure in a test; no external data | benign |
| `tests/utils.py` | plain dict/number comparison helpers | benign |

Verdict: nothing suspicious; safe to `pip install -e .` and run the px tests.
