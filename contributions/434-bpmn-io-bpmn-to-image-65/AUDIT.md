# AUDIT — bpmn-io/bpmn-to-image @ d9907a1

- The change touches README.md only. No code was executed beyond:
  - `npm ci --ignore-scripts` with `PUPPETEER_SKIP_DOWNLOAD=1`, so no Chromium download and no lifecycle scripts;
  - `node cli.js --help` and a failing CLI call, run to confirm the help output and the error message.
- package.json scripts: `all` and `test` (mocha). No install hooks.
- AI policy: none in the repo or in the bpmn-io/.github CONTRIBUTING.
- CLA: **required**. bpmn-io uses CLA assistant, which needs only a GitHub login. It is the same CLA as package 432, so one signature covers both. No DCO.
- PR check (bpmn-io pull-request-quality):
  - The template headings and checklist are kept intact.
  - The title follows Conventional Commits (`docs:`).
  - `Related to #65` is used instead of `Closes`, because the issue's real fix (separate CLI arguments) stays open. This may produce only a warning.
