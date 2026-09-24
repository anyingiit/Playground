# Malicious-code audit — ezedike-evan/corridor-in-a-box @ 5bc2bb5

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/corridor` (138 text files) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| npm lifecycle hooks (root + all `packages/*/package.json`) | `grep` for preinstall/install/postinstall/prepare | none present — benign |
| `vitest.config.ts` (auto-exec on test) | read in full: only path aliases + `tests/**/*.test.ts` include | benign |
| `tests/probe.test.ts:188,215` raw IP `169.254.169.254` | SSRF-guard tests asserting `isSafeUrl`/`probeAnchor` *refuse* the metadata URL; fetch is a stub | benign |
| `tests/cli.test.ts` `spawnSync` | spawns local `tsx packages/cli/src/index.ts` with args in repo root | benign |
| `tests/integration/*.test.ts` | skipped unless live-anchor/DB env vars set; not set here | benign (not run) |
| Third-party deps with install scripts (lockfile) | `esbuild` (platform binary postinstall, well-known), `fsevents` (macOS only) | benign, standard toolchain |
| Committed binaries | none | — |
| `.npmrc` | absent | — |

Verdict: **no malicious code found**; safe to `pnpm install` and run lint/typecheck/test.
