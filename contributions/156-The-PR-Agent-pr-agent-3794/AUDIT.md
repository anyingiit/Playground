# Malicious-code audit: The-PR-Agent/pr-agent @ 2b73b36

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pr-agent-3794` (515 text files scanned), run before installing or executing anything.

| Hit | Reviewed | Verdict |
|---|---|---|
| `setup.py` (runs on sdist install) | Read in full: custom `build_py` that copies `docs/docs/**/*.md(x)` into `pr_agent/_help_docs`; uses only `pathlib`, `shutil.rmtree` on its own build output, `setuptools` | Benign |
| `tests/unittest/conftest.py` (runs every pytest session) | Read in full: sets `LITELLM_LOCAL_MODEL_COST_MAP=True` by default and an autouse fixture that resets a ContextVar | Benign |
| `.pre-commit-config.yaml` | Pinned (by SHA) `pre-commit-hooks` v6.0.0 and `actionlint` v1.7.12, plus a local `uv run --frozen ruff check` hook | Benign, well-known hooks |
| env-dump x6 (`tests/unittest/test_litellm_api_key_guard.py`) | `dict(os.environ)` is snapshotted and compared to assert the API-key guard leaves the environment unchanged; nothing is sent anywhere | Benign (test assertions) |
| raw-ip-url x4 (`169.254.169.254` in `test_mosaico_router.py`, `test_litellm_api_key_guard.py`) | Cloud-metadata URLs used as **inputs** to tests that check SSRF/credential-source blocking; fetches are mocked or rejected | Benign (security tests) |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | n/a |

Also checked: `.github/workflows/build-and-test.yaml` (uv lock check, pytest of the unit and packaging suites, Docker test/smoke images hitting localhost) and `pre-commit.yml`. No downloads of external scripts or obfuscated code on the install/test path.

**Verdict: no malicious code found; safe to install (`uv sync --frozen`) and run the unit tests.**
