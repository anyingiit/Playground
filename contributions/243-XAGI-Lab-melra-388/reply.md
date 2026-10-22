Thanks for the careful review, and for the repro. All three points are addressed in the new commit:

1. `help()`'s body is now blanked (line breaks kept) before the `MELRA_*` read scan, and the script fails if it can't find `help()` or the end of its template literal. With your repro (renaming `MELRA_HARNESS_TOOLS` in `packages/server/src/mcp-server.ts` and keeping the row) it now reports `MELRA_HARNESS_TOOLS is documented but nothing in {apps,packages}/*/src reads it; remove the row`.
2. The Environment block is taken from that `help()` body up to the first `` `); ``, so a last line that runs straight into the backtick still parses.
3. Added a case to `scripts/release.test.mjs` that runs the check on a scratch tree and expects the "remove the row" failure. It fails on the previous commit and passes now; `node --test scripts/release.test.mjs` is 8/8 and `node scripts/check-env-docs.mjs` passes on the real tree.
