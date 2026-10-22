# Audit — WeblateOrg/weblate @ bdc9c3dbc7052408e1ffac3a962225571254fd77

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/weblate` (1323 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` hooks | not run via pre-commit install; only individual linters (ruff) run manually | benign |
| `setup.py` | custom build_py / BuildMo compiling .po → .mo with translate-toolkit; no network | benign |
| env-dump `weblate/utils/tasks.py:82` | settings backup writes os.environ into the instance's own DATA_DIR backup (documented feature) | benign |
| env-dump `weblate/api/tests.py` | `patch.dict(os.environ)` in tests | benign |
| raw-ip-url (15) | test fixtures for SSRF/URL validators (1.1.1.1, 93.184.216.34 = example.com, 100.64.0.1) | benign |
| secret-paths `docs/conf.py` | intersphinx link to wiki.gnupg.org | benign |
| npm lifecycle hooks / binaries | none | — |

Verdict: nothing malicious; safe to run targeted tests.
