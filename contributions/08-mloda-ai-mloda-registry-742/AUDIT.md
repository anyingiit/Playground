# Malicious-code audit — mloda-ai/mloda-registry @ 0bdee17 (main, shallow clone)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/mloda-registry` (618 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| `tox.ini` (auto-exec) | Read fully: default env runs pytest, ruff, mypy, bandit; other envs run in-repo scripts (build verification, pip-audit). No downloads beyond uv/PyPI. | benign |
| root `conftest.py` | Only a module-scoped `flight_server` fixture from `mloda.core` (local Arrow Flight server for multiprocessing tests). No network egress / subprocess / eval. | benign |
| 6× `mloda/community/.../tests/conftest.py` | 1–10 lines each: docstring and/or re-export of `make_feature_set` helpers. | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| env-dump `mloda/testing/extenders/openlineage.py:169` | `patch.dict(os.environ)` to temporarily pop `OPENLINEAGE_*` vars before constructing a test client; nothing is read out or sent. | benign |
| marshal/pickle-exec ×25 | All `pickle.loads(pickle.dumps(obj))  # nosec` round-trips in tests/test-helpers checking picklability of in-process objects; no external data. | benign |
| secret-paths `.gitignore:184,199` | Ignore-rules for credentials / `.pypirc`. | benign |
| `uv.lock` sources | 140× `registry = "https://pypi.org/simple"`, rest are local editable workspace members; no git/url sources. | benign |
| `pyproject.toml` build-system | `setuptools>=82.0.1`, standard backend. | benign |

Also: an older partial clone at the same path (with a pre-existing `.tox` and a leftover `.claude/worktrees/probe` worktree from an interrupted run) was deleted and replaced with a fresh `git clone --depth 1`.

**Verdict: no malicious code found; safe to run `tox`.**
