## Description

`monty` now treats a `-` file argument as standard input, like `python -`: it reads the whole program from stdin and runs it in script mode (or, with `-i`, before the REPL starts, like `python -i -`). Tracebacks and type-check diagnostics name the program `<stdin>`, matching how `-c` programs are named `<string>`. All other CLI options (`-t`, `--mount`, resource limits, …) apply as before.

- `crates/monty-runtime/src/run.rs`: the file branch reads stdin through a small `read_stdin` helper (same error style as `read_file`) when the path is `-`.
- `crates/monty-runtime/src/main.rs`, `README.md`, `README-crate.md`: `--help` and the usage lists mention `-`.
- `crates/monty-runtime/tests/cli.rs`: new CLI tests that pipe a program into `monty -`: output, `<stdin>` in a traceback, a resource-limit flag before `-`, and `-t -` naming `<stdin>` in diagnostics.

Edge cases checked by hand: `-c x -` is still refused ("cannot specify both -c and a file"), `- subprocess` is refused by the existing conflict check, empty stdin runs an empty program, non-UTF-8 stdin fails with `reading <stdin>: stream did not contain valid UTF-8`, and a real file called `-` is still reachable as `./-`. One small difference from CPython: `sys.argv` is `['<stdin>']` rather than `['-']`, consistent with `-c` giving `['<string>']` here.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1101

## Checklist

- [x] Tests pass locally: `cargo test -p monty-runtime` (all pass, including the 4 new tests in `tests/cli.rs`; the new tests fail without the change). `cargo clippy -p monty-runtime --tests --no-deps -- -D warnings` and `cargo fmt --all -- --check` are clean.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [x] Documentation is updated (if applicable) — `--help` text and the `monty-runtime` READMEs
