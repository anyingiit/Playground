# AUDIT — jsx-eslint/eslint-plugin-react @ b6ba4e1

| Hit | Reviewed | Verdict |
|---|---|---|
| `tools/audit_repo.py`: no auto-exec surface, no npm install hooks, no binaries, no pattern hits | — | benign |
| package.json `prepack` (build-types + npmignore), `pretest`/`posttest` (lint, npm audit) | Only on pack/test via npm scripts; I ran mocha/eslint/tsc directly and `npm install --ignore-scripts` | benign |

Commands run: `npm install --ignore-scripts`, mocha, eslint, tsc, `npm run lint:docs` (markdownlint + eslint-doc-generator --check).
