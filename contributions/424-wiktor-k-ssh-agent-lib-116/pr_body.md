Refs #116

This covers the first half of #116: the crate docs, comments and README now point at [RFC 9987](https://www.rfc-editor.org/rfc/rfc9987.html) instead of `draft-miller-ssh-agent-14`. It also reports what I found when I checked the implementation against the RFC (below).

### Documentation changes

- Section 3.x of the draft is section 5.x of the RFC. All the `[draft-miller-ssh-agent-14 § 3.x](…)` links now read `[RFC9987 § 5.x](https://www.rfc-editor.org/rfc/rfc9987.html#section-5.x)`. I checked every anchor against the RFC text.
- `request.rs`: the session-bind link was labelled `§ 8.8.1`, but its URL already pointed at `#section-8.1.1`. The label now says 8.1.1.
- `tests/unknown_request.rs` cited § 4.1 for the "unknown request type → `SSH_AGENT_FAILURE`" rule. The rule is in RFC 9987 § 5.1, and the quoted text now uses the RFC wording ("MUST also be sent").
- The `KeyConstraint::decode` comment pointed at draft-12 § 5.2. It now points at the constraint type registry in RFC 9987 § 8.2.
- README: "SSH Agent Protocol Internet Draft" is now "SSH Agent Protocol (RFC 9987)".

There are no code changes.

### Implementation check (not fixed here)

1. **Unknown key constraint closes the connection.** RFC 9987 § 5.2.7 says an agent that does not recognise a constraint "MUST abort parsing, refuse the request, and return an SSH_AGENT_FAILURE message". draft-14 already said the agent must refuse the request. Today `KeyConstraint::decode` returns `Err(KeyError::AlgorithmUnknown)` for an unknown type byte. That makes the codec fail, so `adapter.try_next().await?` in `handle_socket` returns an error and the connection is dropped. No `SSH_AGENT_FAILURE` is sent.

   I confirmed this with a throw-away test that is not part of this PR. It sent `tests/messages/req-add-identity-constrained-lifetime.bin` with the constraint type byte changed to `3` through the same `agent::handle_socket` setup as `tests/unknown_request.rs`. The client got no response, and the next request on the same stream got none either.

   Fixing it means changing how the decoder reports this error, or adding an "unknown constraint" variant, so the agent can reply with `Failure`. I'd rather leave that design choice to you. I'm happy to send a follow-up PR once you say which way you prefer.
2. **Unknown requests and unsupported known requests** already get `SSH_AGENT_FAILURE`, because #114 and `Session` default to `UnsupportedCommand` → `Response::Failure`. This matches § 5.1.

So #116 should stay open for the implementation part.

### Testing

- `cargo test --all`: all tests pass.
- `cargo clippy --workspace --no-deps --all-targets -- -D warnings`: clean.
- `codespell --config .codespellrc` on the tree and on the commit message: clean.
- `cargo fmt --all -- --check` (stable): clean. The diff only touches comments and doc text.
- `cargo doc --no-deps`: no new warnings. The one existing warning is the redundant link target at `src/agent.rs:269`, which is unchanged.

The commit is signed off (DCO).

This change was prepared with AI assistance (Claude Code). I reviewed the diff and checked every section number and anchor against the RFC text myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
