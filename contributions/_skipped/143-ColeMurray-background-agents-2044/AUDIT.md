# Malicious-code audit — ColeMurray/background-agents @ b98a378

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/background-agents` (2465 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `packages/*/vitest.config.ts` (shared, slack-bot, web, control-plane, linear-bot, github-bot, docs) | Read slack-bot/shared/web configs: only `environment`, `include`, coverage, path alias; no `setupFiles`/globalSetup in any package | benign |
| `packages/{sandbox-runtime,modal-infra}/tests/conftest.py` | Python packages not run for this change | n/a (not executed) |
| `.husky/pre-commit` | Activates local venv if present, runs `npx lint-staged` | benign |
| root `package.json` `prepare` | `node -e "if (process.env.CI) process.exit(0)" && husky` — installs git hooks only | benign |
| env-dump (8): sandbox-runtime/modal-infra tests, sandbox-images/native.py | Test fixtures comparing/printing env in subprocess fakes; native.py copies env for subprocess; nothing sent over network | benign |
| secret-paths (5): comments/test strings mentioning `.npmrc`, "local state" | Path lists for compose-smoke path filter, comments | benign |
| Committed binaries | none | — |

Verdict: nothing malicious. Executed only: `npm ci` (root lifecycle = husky only; run with `--ignore-scripts` anyway), `npm run build -w @open-inspect/shared`, eslint/tsc/vitest/prettier for the touched packages.
