# Malicious-code audit — inokawa/remark-pdf @ 3c36bf5

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/remark-pdf` (33 text files scanned) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `package.json` lifecycle hooks | Only `prepublishOnly` (typedoc + rimraf + build), runs on publish only, never on install/test | benign |
| `vitest.config.ts` (auto-executed by `npm test`) | Only sets `root: "src"`, `clearMocks: true` | benign |
| `rollup.config.js` (runs on `npm run build`) | Reads pdfkit AFM/ICC data from `node_modules/pdfkit` and inlines it; asserts dependency versions; no network, no process spawning, no writes outside `lib/` | benign |
| `src/index.spec.ts` | Reads `fixtures/*.md` + `fixtures/images/img.png`, renders PDF via pdf-to-img / pdfjs-dist, compares image snapshots | benign |
| `.github/workflows/check.yml`, `demo.yml` | `npm ci`, `tsc`, `test`, `build`, storybook build + gh-pages deploy (secrets only GITHUB_TOKEN) | benign |
| Committed binaries | audit reports none in text scan; `fixtures/fonts/*.ttf`, `fixtures/images/*.png`, `src/__image_snapshots__/*.png` are data files for tests | benign |
| Pattern findings (eval/exec/curl/base64/…) | none | — |
| Dependency install scripts | Installed with `npm ci --ignore-scripts` (only `esbuild` postinstall exists — binary check, not needed as its optional platform package is installed anyway) | not executed |

**Verdict: no malicious code found; safe to build/test.**
