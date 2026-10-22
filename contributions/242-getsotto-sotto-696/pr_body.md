Summary: Invitation expiry copy now names the response deadline when that deadline passes before renewal, instead of always blaming the renewal boundary.

Closes #696

Tests: `cd web && npm test -- src/__tests__/PayerTransferJourneys.test.tsx` → 17 passed. Full `npx vitest run` → 260 passed; the only 2 failures are `wasmLoader.test.tsx`, which needs the wasm-pack output (`src/wasm/sotto_wasm.js`) that I didn't build locally, and fail identically on `main`. `tsc -p tsconfig.json` only reports the same missing wasm module, also identical on `main`.

- [x] I signed off every commit (`git commit -s` / Developer Certificate of Origin).

## Description

`PayerTransferInbox` already expires an open invitation at the earlier of `consentExpiresAtEpoch` and `effectiveFrom`, but `stateCopy` only got a boolean, so every expiry read "This invitation expired at the renewal boundary". The inbox now works out which deadline closed the invitation (the response deadline when `consentExpiresAtEpoch < effectiveFrom`, otherwise renewal) and shows:

- response deadline first: "This invitation expired because its response deadline passed. Ask the initiator to start a new request."
- renewal first (or both at the same second): the existing renewal-boundary copy, unchanged.

The expiry calculation, the timer and the removal of the action buttons are untouched.

Tests (`PayerTransferJourneys.test.tsx`):
- the existing timer test (`consent 2000000001`, renewal `2000000100`) now asserts the response-deadline copy and that renewal isn't mentioned; it fails on `main`;
- new: an invitation whose renewal comes first still shows the renewal-boundary copy when the timer fires;
- new: an invitation loaded after its response deadline (but before renewal) shows the response-deadline copy; fails on `main`;
- the existing "already past renewal when loaded" test is unchanged and still passes.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
