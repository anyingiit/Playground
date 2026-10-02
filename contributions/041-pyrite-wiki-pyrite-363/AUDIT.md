# AUDIT — pyrite-wiki/pyrite @ 547a8eb (dev)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pyrite` (734 text files), then manual review of every hit and every auto-executing file.

| Hit | Reviewed | Verdict |
|---|---|---|
| `conftest.py` (root, runs every session) | read in full | Benign: strips `GIT_*` env vars, points `GIT_CONFIG_GLOBAL` at a temp gitconfig, disables auto-embedding via monkeypatch. No network. |
| `tests/conftest.py` | read fixture section | Benign: temp config dir, rate-limiter reset, wraps `subprocess.run` only to *block* non-local `git clone` in tests. |
| `tests/backends/conftest.py` | skimmed | Benign: backend (sqlite/postgres) parametrisation; postgres skipped without a DSN. |
| `tests/e2e/conftest.py` (socket, Popen, `dict(os.environ)`) | read | Benign: binds 127.0.0.1:0 to find a free port, spawns the locally installed `pyrite-server`, sets `HF_HUB_OFFLINE=1`. Not run here (not needed). |
| `web/e2e/global-setup.ts`, `web/playwright.config.ts` | skimmed | Frontend e2e (lsof on local port). Not run; no npm install performed. |
| `.pre-commit-config.yaml` | read | Standard ruff / pre-commit-hooks + local hooks; not installed here. |
| env-dump in `scripts/release.py`, `scripts/run_tutorial.py`, tests | grep context | Copy env to pass to child processes; nothing is sent anywhere. |
| pipe-to-shell in `deploy/*/setup.sh` | read lines | Docs/deploy scripts installing Docker via get.docker.com; never run by build or tests. |
| raw-ip URLs in `tests/test_clipper.py` | read | SSRF-protection tests asserting 169.254.169.254 is *rejected*. |
| secret-paths in `config.example.yaml`, `web/src/lib/stores/auth.svelte.ts` | read | A comment mentioning `~/.ssh/id_rsa` for git auth; a code comment. Benign. |
| Build backend | `pyproject.toml` | setuptools, no `setup.py`, no custom build hooks. No npm lifecycle hooks, no committed binaries. |

**Verdict: no malicious code found. Safe to install (`.[server,cli,dev]`, no semantic/AI extras) and run pytest.**
