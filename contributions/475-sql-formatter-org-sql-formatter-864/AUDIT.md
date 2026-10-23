# AUDIT — sql-formatter-org/sql-formatter @ 223a6ce

| Hit | Reviewed | Verdict |
|---|---|---|
| `tools/audit_repo.py`: no auto-exec surface, no committed binaries, no pattern hits | — | benign |
| package.json `prepare` = clean + grammar + fix + check + build | Only runs local tools (nearleyc, prettier, eslint, tsc, jest, webpack). Skipped anyway with `pnpm install --ignore-scripts`. | benign |
| Dependencies (argparse, nearley, dev: jest/ts-jest/eslint/prettier/webpack/babel) | Standard, from the lockfile | benign |

Commands run: `pnpm install --ignore-scripts`, `pnpm run grammar` (nearleyc), jest, tsc, prettier, eslint. Nothing else executed.
