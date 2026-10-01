## Description

`Escrow.withdrawals` validated its inputs in opposite orders in the two SDKs: TypeScript resolves the wallet address first and then checks `include`, while Python checked `include` first. So `withdrawals(include="")` with no wallet address configured and no `address` override raised `MissingWalletAddress` in TypeScript but `ValidationError("include must not be empty")` in Python.

This PR moves the wallet-address resolution in `sdks/python/pmxt/escrow.py` ahead of the `include` check, matching the TypeScript SDK (and Python's own `approve_tx`). Behaviour for valid inputs and the generated request path are unchanged. A new `sdks/python/tests/test_escrow_withdrawals.py` covers the validation order (missing address + empty `include` → `MissingWalletAddress`; resolved address + blank `include` → `ValidationError(field="include")`) and the request path that gets built.

I only changed `withdrawals` here. The matching `deposit_tx` drift is tracked separately in #1892, and I didn't want to pre-empt how that one gets resolved. Address-first is already what TypeScript and the other Python escrow builders do, so this fix should line up with either outcome.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2353

## Checklist

- [x] Tests pass locally (`cd sdks/python && pytest` → 270 passed, 66 deselected (integration). The new test `test_missing_wallet_address_is_checked_before_empty_include` fails without the fix and passes with it. `black --check` passes on the new test file.)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, root changelog appears to be written at release time; happy to add an entry if you prefer
- [ ] Documentation is updated (if applicable) — n/a, no public behaviour change for valid inputs
