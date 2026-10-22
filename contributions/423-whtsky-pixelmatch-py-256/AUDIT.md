# AUDIT — whtsky/pixelmatch-py @ 669c3c7

`python3 tools/audit_repo.py` (17 text files): no auto-executing hooks (no conftest.py, no setup.py; poetry-core build backend), no npm hooks, no committed binaries (PNG fixtures are Git LFS pointers), no pattern findings.

Fixtures: Git LFS fetch through the proxy was denied, so the 33 PNGs were downloaded from media.githubusercontent.com and **every file's sha256 was verified against the oid in its LFS pointer** before use. They are test data only (opened with Pillow).

Ran only: `uv pip install -e .` + pinned dev deps from PyPI (pytest, pytest-cov, pillow, pytest-benchmark, pytest-mypy, mypy, black), `pytest`, `black --check`. Verdict: nothing suspicious.
