Thanks for taking a look. I couldn't find a clean way without it. The `toml` crate only gives you a value tree, so comments and key order are gone as soon as the file is parsed; keeping them means either a format-preserving parser or hand-editing the TOML text, and the second felt riskier for a file people edit by hand.

To keep the cost down: `toml_edit` comes from the same toml-rs repo as `toml`, it's already in `Cargo.lock` (through `rstest`'s proc-macro), and everything it depends on (`toml_parser`, `toml_writer`, `toml_datetime`, `indexmap`, `winnow`) is already pulled in by `toml` 0.9. So the release build gains that one crate and nothing else.

If you'd still rather not have it, I can switch to a narrower text edit that only touches the git-ai hook entries. Just say so.

I also pushed a fix for the Devin note: when a git-ai hook came before a custom hook in the same `[[hooks.*]]` array, uninstalling rewrote the first table with the custom hook's values and dropped the last one, so the custom hook's comments were lost. It now removes the table that's actually gone. There's a test for it, and the `codex` tests pass (145/145).
