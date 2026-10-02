# Malicious-code audit — fadyehabamer/qr-zero @ 0779ccc

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/qr-zero` → 34 text files, **0 findings** (no auto-exec surface, no npm install hooks, no committed binaries, no suspicious patterns).

Manual review of everything that runs during install/build/test:

| Item | Reviewed | Verdict |
|---|---|---|
| `package.json` scripts | build (rm dist + tsup), typecheck (tsc), test (`node --import tsx --test`), size, check:pack; only lifecycle hook is `prepublishOnly` (runs only on `npm publish`) | benign |
| `package-lock.json` | all `resolved` URLs point to registry.npmjs.org; deps are well-known (tsup, tsx, esbuild, typescript, react, qrcode, jsqr) | benign |
| `tsup.config.ts` | build config + tiny esbuild resolve plugin marking `./index` external | benign |
| `scripts/check-pack.sh` | npm pack → install tarball in mktemp dir → smoke-test ESM/CJS/React/CLI; no network other than npm install | benign |
| `scripts/size.mjs` | esbuild bundle + gzip/brotli size report | benign |
| `test/*.ts`, `test/helpers.ts` | pure unit tests; cli tests spawn the local CLI | benign |
| `.github/workflows/ci.yml` | npm ci / typecheck / test / build / check-pack / size, `contents: read` | benign |

**Verdict: benign — safe to install and run.**
