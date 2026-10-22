## What changed

- `melra help` now lists `MELRA_PAYLOAD_KEY` and `MELRA_HARNESS_TOOLS` at the end of its Environment block, with the wording suggested in the issue (payload key default and "back it up"; `1` turns on `read_file`, `run_command` and the other plain tool names).
- `scripts/check-env-docs.mjs` also reads the Environment block of `help()` in `apps/cli/src/index.ts` and fails when a variable that has a row in `docs/INSTALLATION.md` is missing from it, e.g. `docs/INSTALLATION.md:237: MELRA_PAYLOAD_KEY is documented but missing from the Environment block of 'melra help' in apps/cli/src/index.ts`.
- `CHANGELOG.md`: one line under `[Unreleased]` → `Fixed`.

Closes #388

## Why

Terminal users had no hint that the payload key needs backing up or that the plain tool names exist, and nothing caught help drifting from the docs. With the check in `pnpm docs:check`, the next documented variable can't be left out of `help` silently.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Validation

- [x] `pnpm docs:check`: passes (`All 18 MELRA_* configuration variables are documented in docs/INSTALLATION.md and listed by 'melra help'.`). With only the `help()` change reverted it fails listing both variables, so the check catches the bug.
- [x] `pnpm build`, then `node apps/cli/dist/bin.js help | grep -c 'MELRA_PAYLOAD_KEY\|MELRA_HARNESS_TOOLS'` → `2` (was `0`)
- [x] `apps/cli`: `tsc -p tsconfig.test.json` OK; `vitest run` 137 passed. `check-readme-examples.mjs` and `check-dist.mjs` pass. I did not run the rest of `pnpm check` (other packages' tests, `python:check`) since nothing outside the CLI help text and the docs script changed.
- [x] `CHANGELOG.md` entry under `## [Unreleased]`, in the existing `### Fixed` section
- [x] Documentation updated (n/a beyond the help text; INSTALLATION.md already documents both)
- [x] Security and compatibility impact considered (help text and a docs check only)

## Checklist

- [x] I have signed off my commits under the DCO.
- [x] I have not included secrets, customer data, or deployment details.
- [x] API changes include documentation and tests. (no API change)
