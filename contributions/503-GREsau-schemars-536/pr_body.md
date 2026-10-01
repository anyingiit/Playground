## Description

For tuple structs, serde fills in trailing sequence elements that are missing from the input using their default values when the field (or the whole container) has `#[serde(default)]`. The derived schema, however, always set `minItems` to the total number of elements, so e.g.

```rust
#[derive(Deserialize, JsonSchema)]
struct Skippy(String, #[serde(default)] u32);
```

produced `"minItems": 2` even though `["abc"]` deserializes fine.

`expr_for_tuple_struct` now tracks a separate `min_len` at runtime (it already computes the length at runtime because of the contract-dependent `skip_*` handling). Under the deserialize contract, an element only bumps `min_len` if it has no default (field-level or container-level), so `minItems` becomes the number of elements that are always present — for deserialization this matches serde's `invalid_length` behaviour (serde_derive also enforces that defaulted tuple fields are trailing). If every element is optional, `minItems` is omitted. Similarly, under the serialize contract, elements with `skip_serializing_if` may be omitted by serde, so they no longer count towards `minItems` in the serialize schema (the title of #536 also mentions `skip*`). `skip_deserializing` fields were already excluded from the deserialize schema and keep working with this.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #536

## Checklist

- [x] Tests pass locally (`cargo test --all-features --no-fail-fast`: all pass, integration 142/142; new tests `default::default_fields_tuple_struct`, `default::default_container_tuple_struct`, `default::default_skip_deserializing_tuple_struct`, `default::skip_serializing_if_tuple_struct` fail without the fix (de schema rejects e.g. `["abc"]` / ser snapshot has `minItems: 2`) and pass with it; `cargo clippy --all-targets [--all-features] -- -D warnings`: clean)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, left for the release (no Unreleased section)
- [ ] Documentation is updated (if applicable) — n/a, behaviour fix only
