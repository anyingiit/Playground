# AUDIT — BSC-ES/autosubmit @ 5919cd9

`python3 tools/audit_repo.py` (730 text files): no npm hooks, no committed binaries.

| Hit | Reviewed | Verdict |
|---|---|---|
| 9 × `conftest.py` (test/, test/unit/…, test/integration/…, test/regression/…) | Skimmed test/conftest.py (tmp dirs, .autosubmitrc in tmp, a session fixture that redirects HOME away from the user's home, mocked config); grep of all unit conftests for subprocess/os.system/requests/urlopen/socket/exec/eval/docker found nothing | benign |
| secret-paths in `docker/docker-compose.yml`, `docker/test.sh` | Mounts a local `id_rsa` into a dev container; not run | benign |
| "webhook/paste/tunnel" (`TRANSFER.sh`, `transfer.sh`) | Job template file names in YAML examples, not transfer.sh uploads | benign |

Only `uv pip install -e .[tests,lint]` (PyPI deps), `pytest test/unit` and `ruff` were run. Verdict: nothing suspicious.
