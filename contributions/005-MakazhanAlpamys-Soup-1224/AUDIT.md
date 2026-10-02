# Malicious-code audit — MakazhanAlpamys/Soup (main @ 54e099b)

Tool: `python3 tools/audit_repo.py` + manual review. **Verdict: no malicious code found.**

| Hit | Location | Reviewed verdict |
|---|---|---|
| `tests/conftest.py` (auto-exec) | shared fixtures | Benign: torch-availability helpers, ANSI-strip regex, tempdir/symlink capability probe; no network or subprocess |
| `.pre-commit-config.yaml` | ruff hooks | Benign (only runs if you install pre-commit) |
| raw IP URLs ×26 (`169.254.169.254`, `8.8.8.8`, `127.0.0.2`) | SSRF-guard tests and docstrings | Benign: tests asserting those endpoints are **rejected** |
| `curl … 169.254.169.254` | `tests/test_v0537.py:1018` | Benign: asserts the reward-bash sandbox **blocks** network (Linux namespaces only) |
| Discord webhook URL ×2 | `tests/test_v0715.py` | Benign: dummy `https://discord.com/api/webhooks/x` input to a validator test |
| `dict(os.environ)` ×6 | subprocess env copies in `shrink.py`, `draft.py`, tests | Benign: passes env to child processes, not exfiltrated |
| `~/.ssh/id_rsa` string | `tests/test_issue764_…py:190` | Benign: fake error message text |
| npm hooks / committed binaries | none | — |

What was executed here: `pip install -e ".[dev]"` and pytest (new file, related suites, full suite without the `[train]` extra).
