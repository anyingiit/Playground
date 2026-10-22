Part of #11892: the `script()` part; the binary encoding part is left out (see Reviewer Notes)

## Summary

`transparent::Address::script()` returned an empty, anyone-can-spend script for TEX addresses. Under ZIP 320 a TEX address is a P2PKH destination with a sender restriction, so it now returns the P2PKH script for its validating key hash. Nothing in Zebra reaches this arm today (the funding-stream check rejects TEX), so this only removes a trap for future callers of the public API.

## Reviewer Notes

I left the `zcash_serialize` part of #11892 (error on `Tex`, drop or deprecate `NetworkKind::tex_address_prefix()`) out of this PR. `Display` for `Address` still Base58Check-encodes via `zcash_serialize` until #11880 merges, so making `zcash_serialize` fail for `Tex` now would turn TEX `Display` output into the encoding of an empty buffer. That part fits better after #11880, and the prefix removal is a breaking API change that the issue already suggests splitting into its own `!` PR.

Spec: [ZIP 320, Specification](https://zips.z.cash/zip-0320#specification): a TEX address encodes the same 20-byte validating key hash as a P2PKH address, and payments to it are P2PKH outputs.

## Evidence

New test `transparent::address::tests::tex_script_is_p2pkh_script` checks, for Mainnet, Testnet and Regtest, that a TEX address's script is non-empty and equal to the script of the P2PKH address with the same key hash.

- Before (`main` @ 6c0bfba): `cargo test -p zebra-chain --lib -- --exact transparent::address::tests::tex_script_is_p2pkh_script` fails on the non-empty assertion.
- After: passes. `cargo nextest run -p zebra-chain`: 341 passed.

## Merge Danger

**Door:** two-way until the next release (changes the output of a public `zebra-chain` API for `Tex`; affects crate users that call `script()` on TEX addresses, of which Zebra has none)

**Blast radius:** `zebra-chain` API users only; no consensus, state, or RPC path calls `script()` on a TEX address

## AI Disclosure

Claude Code wrote the implementation, test, and change fragment; I reviewed them and ran the checks above. Context: I had some spare AI-assistant quota and am using it to help projects with open good-first-issues. If this doesn't fit or you'd rather not take it, please feel free to close it, no hard feelings at all.
