# Malicious-code audit — pasteurlabs/tesseract-core (main @ a8d7801, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/tesseract-core` (434 text files), then manual review of every hit and of all auto-executing surfaces.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` | standard pre-commit-hooks, ruff, prettier (org mirror), local hooks that run `uv lock` / `uv export` to regenerate lock/requirements only when pyproject changes | benign (not run by us except ruff) |
| `tests/conftest.py` subprocess calls (L103, 272, 428, 762–843) | `nvidia-smi -L` GPU probe; spawning `tesseract_core.runtime.serve` on localhost for tests; `docker network rm` cleanup of test-created networks; docker compose for an MLflow fixture (end-to-end only) | benign |
| `tests/conftest.py` network (L251, 293, 823) | free-port probe on 127.0.0.1; health polling of localhost test servers | benign |
| `tests/sdk_tests/conftest.py:52` | `uv venv` / install for foreign-interpreter tests (skips if uv missing) | benign |
| `benchmarks/conftest.py:75` | benchmark helper, not run | benign |
| `tesseract_core/sdk/local_client.py:258` env-dump | copies `os.environ` to build a child process env for in-process/subprocess Tesseracts; not sent anywhere | benign |
| `docs/downloads/create-vm-azure.sh:119` ssh | documented helper script for users provisioning an Azure VM; not executed by build/tests | benign |
| 2 committed `.bin` files (108 B each) | binref test data for examples | benign |
| Build backend | hatchling + hatch-vcs, no custom build hooks | benign |

**Verdict: no malicious code found. Safe to install and run the fast (non-Docker) test suite.**
