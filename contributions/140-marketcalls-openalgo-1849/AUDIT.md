# Audit — marketcalls/openalgo @ ad2a3f5 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/openalgo` (2442 text files).
Only the frontend is executed for this contribution (`npm ci --ignore-scripts`, biome, vitest, tsc). No Python code, conftest, or install scripts are run.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-exec: `frontend/vitest.config.ts`, `frontend/src/test/setup.ts` | Read fully: react plugin, jsdom, alias; setup only mocks matchMedia / ResizeObserver / IntersectionObserver and calls RTL cleanup | Benign |
| Auto-exec: `playwright.config.ts`, `.pre-commit-config.yaml`, `test/conftest.py`, `test/sandbox/conftest.py` | Not executed (e2e / Python suites not run) | N/A |
| npm lifecycle hooks in `frontend/package.json` | None | Benign |
| Committed binaries | None | Benign |
| env-dump (23) `dict(os.environ)` in Python tests / websocket_proxy | Passing env to subprocesses in tests; not run | Benign |
| pipe-to-shell `install/install-docker-multi-custom-ssl.sh` (astral uv installer) | Documented installer script, not run | Benign |
| powershell-download `install/docker-run.bat` (sample .env) | Installer, not run | Benign |
| raw-ip-url 169.254.169.254 in Python tests | SSRF-guard negative test inputs | Benign |
| secret-paths (12) | Comments mentioning "local state" | False positives |
| webhook/paste/tunnel (5) | Telegram getMe API, ngrok placeholder, Bruno sample collection | Benign |

Verdict: nothing malicious; safe to run the frontend lint/test/typecheck with `npm ci --ignore-scripts`.
