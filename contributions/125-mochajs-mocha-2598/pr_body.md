## PR Checklist

- [x] Addresses an existing open issue: fixes #2598
- [x] That issue was marked as [`status: accepting prs`](https://github.com/mochajs/mocha/issues?q=is%3Aopen+is%3Aissue+label%3A%22status%3A+accepting+prs%22)
- [x] Steps in [CONTRIBUTING.md](https://github.com/mochajs/mocha/blob/main/.github/CONTRIBUTING.md) were taken

## Overview

`done(obj)` with a circular plain object threw `TypeError: Converting circular structure to JSON` from `JSON.stringify` in `lib/runnable.js`, hiding the real "done() invoked with non-Error" failure. Now, if `JSON.stringify` throws, it falls back to Mocha's own `utils.stringify`, which marks cycles as `[Circular]`. Output for non-circular objects is unchanged. Added a unit test in `test/unit/runnable.spec.cjs` (fails without the fix).

Checked locally: `format:check`, `lint:code`, `lint:knip`, `tsc`, `test-smoke`, `test-node:unit`, `test-node:interfaces`, `test-node:reporters` and `test-node:integration` pass. I did not run browser tests.

**Disclosure:** prepared with Claude Code (AI assistant) using spare quota; I reviewed it. Feel free to close if it doesn't fit.
