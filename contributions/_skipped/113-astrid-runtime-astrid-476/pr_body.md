## Linked Issue

Closes #476

## Summary

Duplicate registrations in `CapsuleRegistry` returned `CapsuleError::UnsupportedEntryPoint`, so the message read `Unsupported entry point: Already registered: <id>` and callers could not tell a duplicate apart from a real entry-point problem without matching on the string. This PR adds two variants for these cases and returns them from every duplicate check:

- `CapsuleError::AlreadyRegistered(String)`: a capsule ID is already in the principal's view.
- `CapsuleError::UplinkAlreadyRegistered(String)`: an uplink ID is already registered.

The issue proposed `ConnectorAlreadyRegistered`. It was filed before connectors were renamed to uplinks (`register_connector` is now `register_uplink`), so the variant follows the current name. The payload is the bare ID, and the `#[error]` strings keep today's wording (`Already registered: <id>`, `Uplink already registered: <id>`) without the misleading `Unsupported entry point:` prefix.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Changes

- `astrid-capsule-types`: add `CapsuleError::AlreadyRegistered` and `CapsuleError::UplinkAlreadyRegistered`.
- `astrid-capsule` registry: return the new variants from the duplicate checks in `commit_reserved_runtime`, `validate_reserved_runtime`, `register_existing`, `register_uplink` and the system-runtime replacement paths (`replacement.rs`).
- Update the `# Errors` docs of `register`, `register_for`, `register_existing`, `register_uplink` and `register_owned_by_default` so they name the variants.
- Left unchanged: the `register_owned_by_default` error for a runtime held by a non-default system owner (`compatibility.rs`). It is an ownership conflict, not a plain duplicate in the requested view, so it still returns `UnsupportedEntryPoint`. Happy to move it to `AlreadyRegistered` if you prefer.
- New regression tests at the end of `crates/astrid-capsule/src/registry_tests.rs` for `register`, `register_existing` and `register_uplink`.
- Changelog fragment `changes/476.fixed.md`.

A grep of the workspace found no code that matches on these messages, and no exhaustive `match` on `CapsuleError`. Adding the variants therefore does not break any downstream code.

## Verification

- Red: with the new variants and tests in place but the call sites reverted, `cargo test -p astrid-capsule --lib duplicate_register` fails 3 of 3. For example: `expected AlreadyRegistered, got UnsupportedEntryPoint("Already registered: dup-capsule")`.
- Green: with the fix, those 3 tests pass. `cargo test -p astrid-capsule registry` gives 34 passed.
- `cargo test -p astrid-capsule -p astrid-capsule-types`: all pass (799 lib tests in astrid-capsule, plus the other test targets).
- `cargo clippy -p astrid-capsule -p astrid-capsule-types --all-targets -- -D warnings`: clean.
- `cargo fmt --check`: clean.
- File sizes: `registry.rs` 962 lines (source cap 1000), `registry_tests.rs` 1061 lines (test cap 2000).
- Toolchain 1.95.0, from `rust-toolchain.toml`. I did not run `cargo test --workspace`. Adding variants can only break an exhaustive `match`, and none exists in the workspace.

## AI / Tool Assistance

Assisted-by: Claude Code

- Affected areas: `crates/astrid-capsule-types/src/error.rs`, the duplicate checks and `# Errors` docs in `crates/astrid-capsule/src/registry.rs` and `registry/{uplinks,replacement,compatibility}.rs`, the new tests in `registry_tests.rs`, and the changelog fragment.
- Nature of assistance: Claude Code located the duplicate-registration sites, drafted the new variants, call-site changes, doc updates, regression tests, changelog fragment and this description.
- Review and validation: I reviewed the full diff line by line. The tests failed before the fix and pass after it. I also ran the crate's registry tests, clippy with `-D warnings`, and `cargo fmt --check`, as listed under Verification.

## Checklist

- [x] Linked to an issue
- [x] Changelog fragment added under `changes/{issue}.{kind}.md` (docs/CI-only may skip; release PRs roll fragments into the version section instead of adding one)
- [x] I understand every change in this PR and can explain its design, risks, and validation.
- [x] I reviewed and tested any meaningful tool-generated output included in this PR.
- [x] Every non-bot, non-merge commit has a matching `Signed-off-by` trailer.
