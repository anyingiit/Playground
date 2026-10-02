# Audit — xtermjs/xterm.js @ c58ea363 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/xterm.js` (513 text files) + manual review of npm scripts, dependency install scripts, and the bin/ helpers that `npm run build` / `esbuild` / `test-unit` / `lint` execute.

| Hit | Reviewed | Verdict |
|---|---|---|
| 13 × `playwright.config.ts` (test/ and addons/*/test) | Standard Playwright config; `webServer` runs `npm start` (local demo on :3000). Integration tests are not run here (only Node unit tests). | benign / not run |
| npm lifecycle hooks (root package.json) | No install/postinstall/prepare. `presetup`/`postsetup`/`prepackage`/`prepublishOnly`/`posttest` only chain the repo's own build/lint scripts. | benign |
| Dependencies with install scripts (package-lock.json) | `esbuild@0.28.1`, `fsevents@2.3.2` (macOS only), `node-pty@1.2.0-beta.13` — all from registry.npmjs.org, well-known packages. Plan: `npm ci --ignore-scripts` where possible (node-pty is only needed for the demo server). | benign |
| addons/addon-unicode-graphemes/src/third-party/UnicodeProperties.ts:2 long base64 | Serialized Unicode trie decoded by `UnicodeTrie` (grapheme/width tables); pure data, no eval. | benign |
| bin/publish.js:13 writes `~/.npmrc` with `NPM_AUTH_TOKEN` | CI release script; only runs on publish, token from CI env. Not executed here. | benign / not run |
| bin/esbuild_all.mjs, bin/esbuild.mjs, bin/test_unit.js, bin/lint_changes.js (`child_process`) | Spawn `node bin/esbuild.mjs`, mocha/nyc, `git diff --name-only`, oxlint/eslint. No network, no fetch/eval. | benign |
| .github/workflows/copilot-setup-steps.yml | `npm ci`, `npm run setup`, `npm run esbuild`; read-only permissions, pinned actions. | benign |
| Committed binaries | none | — |

Verdict: nothing malicious; safe to run `npm ci`, `npm run build`, `npm run esbuild`, `npm run test-unit`, `npm run lint`/`lint-changes` locally.
