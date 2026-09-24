# Malicious-code audit — denoland/std (shallow clone of main @ 2958335, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py deno-std` (2760 text files scanned) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported; repo has no package.json lifecycle hooks at root | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none (0 bytes) | benign |
| `long-base64-blob` ×4 in `cli/_data.json` | Unicode width lookup tables (`UNICODE_VERSION`, `tables[].d/.r`) used by `@std/cli` `unicodeWidth()` | benign (data, never executed) |
| `deno.json` tasks | `test`, `lint:*`, `ok` only run `deno test/lint/check` and repo `_tools/*.ts` checkers; `test:node`/`test:bun` do `npm install` in `_tools/node_test_runner` (not run here) | benign; only `deno test expect/`, `deno lint`, `deno fmt --check`, `deno check` and the doc/export checkers were run |
| Tests for the touched module (`expect/*_test.ts`) | read `_to_match_snapshot_test.ts`, `_snapshot_state.ts`: write only to `__snapshots__/` next to test files / temp dirs | benign |

Verdict: **nothing suspicious; safe to run the targeted Deno tests.** Deno runtime installed separately from the official release zip into the work dir.
