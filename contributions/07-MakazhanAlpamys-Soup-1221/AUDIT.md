# Malicious-code audit — MakazhanAlpamys/Soup (main @ 1826a2b)

Tool: `python3 tools/audit_repo.py /home/user/work/Soup-1221` (1345 text files) + manual review.
**Verdict: no malicious code found.** Hit set is identical to the earlier audit at 54e099b
(`contributions/05-MakazhanAlpamys-Soup-1224/AUDIT.md`); re-checked on this commit.

| Hit | Location | Reviewed verdict |
|---|---|---|
| `tests/conftest.py` (auto-exec) | shared fixtures | Benign: no subprocess/urllib/requests/socket/exec/eval (grep re-run on 1826a2b) |
| `.pre-commit-config.yaml` | ruff hooks | Benign (only runs if pre-commit installed; not used here) |
| build backend | `pyproject.toml` → hatchling, no `setup.py` | Benign: no custom build hooks |
| raw IP URLs ×26 (`169.254.169.254`, `8.8.8.8`, `127.0.0.2`) | SSRF-guard tests / docstrings | Benign: tests assert those endpoints are rejected |
| Discord webhook URL ×2 | `tests/test_v0715.py` | Benign: dummy `.../webhooks/x` validator input |
| `dict(os.environ)` ×6 | `shrink.py`, `draft.py`, tests | Benign: env copy for child processes |
| `~/.ssh/id_rsa` string | `tests/test_issue764_…py:190` | Benign: fake error-message text |
| npm hooks / committed binaries | none | — |

Executed here: fresh venv `pip install -e ".[dev]"`, ruff, pytest (new test file + related suites).
