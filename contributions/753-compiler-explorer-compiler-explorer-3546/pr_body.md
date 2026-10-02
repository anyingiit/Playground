## Description

When solc writes its artifacts (we pass `--combined-json ... -o contracts`), it also prints `Compiler run successful. Artifact(s) can be found in directory "contracts".`. Compiler Explorer counts that line as compiler output, so every successful Solidity compilation shows an output indicator, as if there were a warning.

`SolidityCompiler` now overrides `processExecutionResult` and drops lines that start with `Compiler run successful` from both stdout and stderr. Both streams are filtered because, per solc's `CommandLineInterface.cpp`, the artifact message goes to stdout, while versions before 0.8.x print the variant `Compiler run successful, no output requested.` to stderr (current versions also have `... No contracts to compile.` / `... No output generated.` on stdout). Real warnings and errors are kept. This only affects `solc`: `solx`, `resolc` and the zksync compiler don't extend `SolidityCompiler`.

`test/solidity-tests.ts` is new. It stubs `exec` and runs `runCompiler`, checking that the message is removed from either stream and that warnings are kept.

I couldn't run a real solc binary here; the message texts and streams were checked against solc's source (v0.5.17, v0.7.6, v0.8.0, v0.8.20 and `develop`) rather than a live run.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #3546

## Checklist

- [x] Tests pass locally
  - `npx vitest run test/solidity-tests.ts`: 3 passed. All 3 fail with `lib/compilers/solidity.ts` reverted to `main`.
  - `npm run check` (ts-check, biome lint-check, frontend imports, license headers, `test-min`): passes, 136 test files passed, 1 skipped.
  - The pre-commit hook (lint-staged + checks) passed.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no changelog)
- [ ] Documentation is updated (if applicable) — n/a (no user-facing docs cover this)
