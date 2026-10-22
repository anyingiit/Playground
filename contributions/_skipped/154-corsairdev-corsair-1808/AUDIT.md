# Malicious-code audit — corsairdev/corsair @ 9dce172e

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/corsair` (9765 text files).

| Hit | Reviewed | Verdict |
|---|---|---|
| ~330 `jest.config.*` (incl. `packages/cli/jest.config.cjs`) | Read cli config: plain ts-jest preset, moduleNameMapper, no setup files | benign |
| `package.json` prepare = `simple-git-hooks` | standard git hook installer; skipped anyway via `--ignore-scripts` | benign |
| `packages/corsair/package.json` postinstall = `scripts/postinstall-frpc.mjs` | Downloads pinned frp release from github.com/fatedier/frp, verifies SHA-256 from `frpc-release.json`, extracts into `~/.cache/corsair/frpc`. Documented dev-tunnel helper. Not run here (`--ignore-scripts`). | benign |
| powershell-download (66) | all are `downloadFile` API endpoint names in plugin code / explorer JSON | benign (false positive) |
| raw-ip-url (3) | SSRF-guard tests using 169.254.169.254 / 127.0.0.2 | benign |
| webhook/paste/tunnel (19) | ngrok/webhook.site placeholder URLs in docs, prompts and demo tests | benign |
| committed binaries | none | — |

Verdict: nothing malicious. Install performed with `pnpm install --ignore-scripts`, only the CLI test/typecheck/lint were run.
