# Malicious-code audit — rjsf-team/react-jsonschema-form @ 7466db4

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/rjsf` (1239 text files scanned), hits reviewed manually before any install/build/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| `vitest.config.ts` (root + 16 packages) | root lists `packages/*/vitest.config.ts` projects; package configs re-export / mergeConfig `testing/vitest.base.ts` (jsdom env, `@rjsf/source` resolve condition, setup file) | benign |
| `testing/testSetup.ts` (setup file run by tests) | imports `@testing-library/jest-dom`, installs `jsdom-testing-mocks` ResizeObserver mock | benign |
| `.husky/pre-commit` | runs `pnpm run pre-commit:husky` (nx `precommit` target = lint-staged); not triggered since we commit with hooks irrelevant (husky not installed outside `prepare`) | benign |
| `package.json` `prepare: is-ci \|\| husky` | standard husky install | benign |
| `pnpm-workspace.yaml` `onlyBuiltDependencies`/`allowBuilds` | only `@parcel/watcher`, `ata-validator`, `core-js`, `esbuild`, `nx` may run install scripts — all well-known packages | benign |
| `powershell-download` in `pnpm-lock.yaml:9293` | false positive: substring of a sha512 integrity hash | benign |
| `secret-paths` in daisyui Date/DateTime widgets | false positive: "local state" in code comments | benign |
| Committed binaries | none | — |

Verdict: **no malicious code found**; safe to install deps and run tests.
