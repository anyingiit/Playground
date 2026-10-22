Fixes #2944.

Over SSH, Fresh decided whether a remote file is writable by comparing the file's uid/gid (from the agent's `stat`) with the *local* process's uid and groups. Those ids come from different hosts. With `auto_read_only` on, a file that only its owner may write (0644, 0600) opened read-only whenever the local and remote uids differ. Termux is one easy way to get there. It also cuts the other way: if the uids happen to match, a file the remote user can't write could look writable.

The agent is the one process that runs as the remote user, so it now answers the question:

- `agent.py`: `stat` adds `"writable": os.access(path, os.W_OK)` (with `effective_ids` where the platform supports it, like the local `faccessat(AT_EACCESS)` check). Being the kernel's answer, it also covers ACLs and read-only mounts, which the mode-bit comparison couldn't see.
- `RemoteMetadata` gains an optional `writable`. `convert_metadata` uses it, and falls back to the old uid/gid comparison when an agent doesn't send it.

`ls` entries are unchanged. They never carried uid/gid and still use the mode bits, so this only affects `stat`-based checks such as `auto_read_only` on open.

Tests:
- `test_agent_stat_reports_writable` (`services/remote/tests.rs`) runs the bundled agent on a temp file. `writable` is `true`, and after `chmod 0444` it matches what `faccessat(W_OK, AT_EACCESS)` says for the same file (`false` normally, `true` for root).
- `test_convert_metadata_uses_the_agents_writable` (`services/remote/filesystem.rs`): a 0644 file owned by a different uid is writable when the agent says so, and a file with our own uid is read-only when the agent says it isn't writable.

Both fail without the change. `cargo test -p fresh-editor --lib services::remote` passes, and so do the 90 e2e tests matching `remote`. `cargo fmt` and `cargo check --all-targets` are clean. `cargo clippy --all-targets` adds no new warnings. I haven't tried a real SSH session with differing uids.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

- [x] I agree my contributions are licensed under GPL-3.0-or-later and may be relicensed in the future at the maintainer's discretion (see [CONTRIBUTING.md](../CONTRIBUTING.md#license)).
