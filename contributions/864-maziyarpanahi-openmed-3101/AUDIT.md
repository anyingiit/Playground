# Malicious-code audit — maziyarpanahi/openmed @ a88fe2feb699fd1945d053859998e54e00237825

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/openmed` (3347 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/conftest.py` (auto-runs under pytest) | Read fully (227 lines): sample fixtures, Mock objects, autouse resets of `OpenMedConfig`, tokenizer cache and a few MLX env vars | Benign |
| `tests/fuzz/conftest.py` | Not used (fuzz suite not run) | n/a |
| `.pre-commit-config.yaml` | Standard upstream hooks (pre-commit-hooks, ruff, bandit, gitleaks) | Benign |
| playwright configs (`web/extension`, `tests/browser/brand`) | JS browser test configs; not run | n/a |
| `android/gradle/wrapper/gradle-wrapper.jar` | Standard Gradle wrapper; not run | n/a |
| env-dump (5) | `dict(os.environ)` copies passed to subprocesses in tests / MedCAT bridge; no exfiltration | Benign |
| pickle round-trips (8) | Tests pickling own objects (`pickle.loads(pickle.dumps(x))`) | Benign |
| long base64 blob | Sigstore bundle test fixture | Benign |
| "powershell-download" (6) | Kotlin `downloadFile` method names in Android model downloader | Benign (false positive) |
| raw IP URL | `127.42.0.1` loopback in Go client test | Benign |
| secret-paths (13) | `.gitignore`/`.gitleaks.toml` patterns and the words "local state" in docstrings | Benign (false positive) |
| `pyproject.toml` | hatchling build backend, no custom build hooks executed | Benign |

Verdict: **no malicious code found**. Only the new module's focused tests plus nearby unit tests and ruff were run, inside a venv in the work dir.
