# Malicious-code audit — flint-fyi/flint @ 664805c (main, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/flint` (1705 text files scanned), then manual review of everything that runs on install / test.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `package.json` `prepare = husky` | installs git hooks into `.git/hooks` only | benign (standard); ran install with `--ignore-scripts` anyway |
| `.husky/pre-commit` → `lint-staged` | only runs on `git commit` | benign |
| `.agents/setup:4` `curl https://mise.run \| sh` | setup script for the maintainers' remote agent "orb" (installs mise, node, pnpm); not invoked by install/test | benign, **not run** |
| `vitest.config.ts` | builds per-package vitest projects; setupFiles `console-fail-test/setup` + `@flint.fyi/ts-patch/install-patch-hooks` | benign |
| `packages/ts-patch/src/{install-patch-hooks,install-patch,shared}.ts` | `module.registerHooks` that string-patches the in-memory `typescript` module source (Volar-style extra-extension support); no network, no fs writes, no exec | benign |
| `pnpm-workspace.yaml` `allowBuilds` | only `esbuild` and `sharp` (well-known native binaries) | benign |
| Other package `pre/postinstall` scripts | none in `packages/*/package.json` | n/a |
| Committed binaries | none | n/a |

Verdict: **no malicious code found**; safe to install (with `--ignore-scripts`) and run the vitest suite.
