# Malicious-code audit — ColeMurray/background-agents @ b98a378 (shallow clone)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/background-agents` (2465 text files).

| Hit | Reviewed | Verdict |
|---|---|---|
| `packages/*/vitest.config.ts` (shared, slack-bot, control-plane, web, …) | Read slack-bot + shared configs: plain `defineConfig` with node env, include globs, v8 coverage | benign |
| `packages/sandbox-runtime/tests/conftest.py`, `packages/modal-infra/tests/conftest.py` | Python tests — not run in this task (TS-only change) | not executed |
| `.husky/pre-commit` | activates optional venv then `npx lint-staged` | benign (hooks not installed; `prepare` uses husky only outside CI) |
| `package.json` `prepare` = `node -e "if (process.env.CI) process.exit(0)" && husky` | installs git hooks only | benign; installed with `CI=1 npm ci --ignore-scripts` anyway |
| env-dump (8): sandbox-runtime/modal-infra tests, `sandbox_images/native.py` | test fixtures snapshotting `os.environ` to assert no mutation / pass env to subprocess; no network exfiltration | benign |
| secret-paths (5): comments, `.npmrc` path globs in smoke test/workflow | path lists for compose-smoke change detection | benign |
| Committed binaries | none | — |

Verdict: nothing malicious found. Only the slack-bot / shared vitest + eslint + tsc were executed.
