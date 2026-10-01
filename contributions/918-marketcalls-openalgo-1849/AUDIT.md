# Malicious-code audit — marketcalls/openalgo @ ad2a3f5 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/openalgo` — 2442 text files scanned. Only the `frontend/` JS toolchain was executed (npm ci --ignore-scripts, vitest, biome, tsc); no Python code was run.

| Hit | Reviewed | Verdict |
|---|---|---|
| npm lifecycle hooks (frontend/package.json) | none present; installed with `--ignore-scripts` anyway | benign |
| frontend/vitest.config.ts | plain jsdom/vitest config, setupFiles `src/test/setup.ts` | benign |
| frontend/src/test/setup.ts | jest-dom, cleanup, DOM API mocks (matchMedia/ResizeObserver/clipboard); no network/fs | benign |
| frontend/playwright.config.ts | e2e config, not run | benign (not executed) |
| test/conftest.py, test/sandbox/conftest.py, .pre-commit-config.yaml | Python/pre-commit, not run | not executed |
| env-dump (23, `dict(os.environ)`) | test subprocess env copies / websocket proxy launch | benign |
| pipe-to-shell install/install-docker-multi-custom-ssl.sh:205 | official astral uv installer in an install script | benign, not executed |
| powershell-download install/docker-run.bat | downloads sample .env from project repo | benign, not executed |
| raw-ip-url 169.254.169.254 (tests) | SSRF-rejection test inputs | benign |
| secret-paths (12) | matches the words "local state" in comments | false positive |
| webhook/paste/tunnel (5) | Telegram getMe API, ngrok placeholder, Bruno sample collection | benign |
| Committed binaries | none | — |

Verdict: nothing malicious found; safe to run the frontend tests.
