# AUDIT — bpmn-io/dmn-migrate @ 5fb8357

- `tools/audit_repo.py`:
  - No auto-executing surface in the repo itself.
  - The npm `prepare` script runs only `run-s build` (rollup).
  - No committed binaries.
- Dependencies were installed with `npm ci --ignore-scripts`.
- Tests ran with `npm test` / `npm run all` (eslint, rollup, mocha).
  - `xsd-schema-validator` uses the local Java to validate the XSD.
- AI policy: none in bpmn-io/.github CONTRIBUTING or in the repo.
- CLA: **required**. bpmn-io uses CLA assistant (GitHub login only, no extra personal data). Closed PR #61 for this issue stalled on the CLA. No DCO.
- The PR check (bpmn-io/actions pull-request-quality) requires:
  - the template headers and the checklist kept intact;
  - Conventional Commits.
  - It also gives a warning if no `Closes #` is present.
  - pr_body.md follows the template, and the commit is `fix:` with `Closes #60`.
- Note: the repository uses CRLF line endings. The patch preserves CRLF.
