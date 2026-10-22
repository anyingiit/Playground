Closes #348

`zb install felixkratz/formulae/sketchybar` died with `uninitialized constant Sketchybar::MacOS (NameError)` and a Ruby backtrace through the build shim. This fixes both halves of the issue.

- **`MacOS`:** Homebrew aliases `OS::Mac` as `::MacOS` (`os/mac.rb`), and formulae call `MacOS.version`. The shim already has `OS::Mac.version`, so it now defines `MacOS = OS::Mac`. sketchybar's `if MacOS.version < 11` gets past that line. Homebrew only defines the alias on macOS, but the shim defines `OS::Mac` everywhere, so the alias is defined everywhere too, which is also what lets the test run on Linux.
- **The error:** a `NameError` raised while loading or installing the formula, or a `NoMethodError` on the formula or one of the shim's modules, is reported as the name the formula needs and the formula line that uses it, with Ruby's message underneath:

  ```
  Error: sketchybar uses `Xcode`, which zerobrew can't build from source yet (sketchybar.rb:5)
    uninitialized constant OS::Mac::Xcode
  ```

  Any other `NoMethodError` (say, a method called on `nil`) is the formula's own failure, so it says `Error: foo's formula failed (foo.rb:4)` with the message, rather than blaming the shim. The backtrace is printed only when `zb` runs with `-v` or more: the executor sets `ZEROBREW_BACKTRACE=1` for the shim when `tracing` has `INFO` enabled. A missing method on the formula reads the same way, e.g. ``uses `which` `` for the `openssl@3` build in #404 (this doesn't fix #404, it only makes its error clearer).

  Not changed here: the shim's stderr is still streamed live and then repeated in zerobrew's "source build failed" error, so these lines show twice. That's how every build failure reads today, and changing it is a separate question.

Tests in `zb_io/src/build/executor.rs`, run against the real shim with the local `ruby`: `MacOS` is `OS::Mac` and `MacOS.version < 11` works; an unknown constant in `install` or in the class body is reported with its name and formula line and without shim backtrace lines; with `ZEROBREW_BACKTRACE` the backtrace is there; a missing method (`which`) is named; and `nil.split` is reported as the formula's own failure. `run_shim_formula` gained a `_with_env` variant for the backtrace test. `CHANGELOG.md` has two entries under Unreleased.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Testing

- `cargo test -p zb_io build::`: the six new tests fail with the shim from `main` and pass with this change.
- `cargo test --workspace` on Linux x86_64 (Rust 1.96, Ruby 3.3): everything else passes except four tests that fail the same way without this change because I ran them as root (`init::tests::is_writable_returns_false_for_readonly_dir`, `init::tests::needs_init_when_not_writable`, and two installer tests in `zb_cli/tests`).
- `cargo clippy --workspace --all-targets -- -D warnings` and `cargo fmt --all -- --check` are clean.
- Not tried on macOS, so I haven't seen how far sketchybar's build gets after this; its `codesign` and `curl` steps are plain `system` calls.
