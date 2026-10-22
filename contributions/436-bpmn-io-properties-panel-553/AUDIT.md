# AUDIT — bpmn-io/properties-panel @ 193caac (3.58.0)

- Dependencies were installed with `npm ci --ignore-scripts`; no lifecycle hooks were run.
- `prepare` only runs `run-s build` (rollup). I ran `npm run build` by hand because the tests import the built `preact` output.
- Tests: karma + webpack, run in local Chromium (Playwright build at /opt/pw-browsers, launched through a wrapper that adds `--no-sandbox` because the container runs as root; the wrapper is not in the repo).
- No committed binaries were executed.
- AI policy: none in the repo or in bpmn-io/.github.
- CLA: **required** (bpmn-io CLA assistant). It is the same CLA as 432 and 434; local has already submitted those PRs.
- PR check (bpmn-io pull-request-quality):
  - the template headings and checklist must be kept;
  - the title must follow Conventional Commits.
- CHANGELOG: not edited. Maintainers write it in separate `chore: update changelog` commits.
