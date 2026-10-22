Closes #414

zerobrew links a keg's `bin`, `sbin`, `lib`, `include`, `share` and `etc`, but not `Frameworks`, so Python's framework build on macOS (`python@3.x` ships `Frameworks/Python.framework`) never shows up in `$PREFIX/Frameworks`, where Homebrew puts it. (The `sbin` half of the issue was already fixed on `main`.)

This follows Homebrew's `Keg#link` rule for `Frameworks`: a path matching `[^/]*\.framework(/Versions)?$` is created as a real directory so several kegs can share `Foo.framework/Versions`, and everything else (`Versions/3.13`, `Versions/Current`, the bundle's top-level `Python`/`Headers` links) is linked as it is.

- `zb_io/src/cellar/link.rs`: `Frameworks` is added to `LINK_DIRS`; `dir_mode` creates `*.framework` and `*.framework/Versions` and links the rest. `Linker::new` does not create `Frameworks` up front, since most prefixes (and every Linux one) never get a framework; it is created when a keg first links into it.
- Tests: `links_frameworks_the_way_homebrew_does` builds a keg shaped like `python@3.13`'s framework, links and unlinks it; `frameworks_dir_is_created_on_first_use`; `framework_dirs_are_recognised`. `zb_cli/tests/parity.rs` lists `Frameworks` among the linked directories.
- `CHANGELOG.md`: an entry under Unreleased.

One thing a reviewer might ask: two kegs that both ship the bundle's top-level `Python`/`Headers` links and `Versions/Current` would conflict, as they would in Homebrew. Homebrew's non-default Pythons remove those links (`altinstall`), so real bottles shouldn't hit it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Testing

- `cargo test --workspace` on Linux x86_64 (Rust 1.96): the new link test fails on `main` (nothing is linked into `Frameworks`) and passes with the change; all other link tests pass. Four tests fail the same way with and without this change because I ran them as root (`init::tests::is_writable_returns_false_for_readonly_dir`, `init::tests::needs_init_when_not_writable`, and two installer tests in `zb_cli/tests`).
- `cargo clippy --workspace --all-targets -- -D warnings` and `cargo fmt --all -- --check` are clean.
- Not tested on macOS with a real `python@3.13` bottle.
