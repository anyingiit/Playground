# AUDIT — mitmproxy/pdoc @ 00e18eb

`python3 tools/audit_repo.py` (104 text files): no auto-executing hooks, no npm hooks, no binaries, no pattern findings.

| Item | Reviewed | Verdict |
|---|---|---|
| pyproject.toml (hatch build, tox config, dev deps) | standard: pytest, hypothesis, ruff, mypy, tox-uv | benign |
| uv.lock (`uv run --frozen`) | resolves from PyPI only | benign |
| test/ (snapshot tests import test/testdata modules) | plain Python modules used as documentation fixtures | benign |

Verdict: nothing suspicious.
