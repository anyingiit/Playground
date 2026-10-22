Closes #376.

`zb bundle check` reports the packages in a Brewfile that aren't installed and exits non-zero if there are any. It only reads the local database, so nothing is downloaded and it returns immediately, and an `.envrc` can run `zb bundle check || zb bundle install` the way it would with `brew bundle check`.

```
$ zb bundle check
==> 2 of 2 packages in Brewfile are not installed:
  jq
  cask:firefox
error: the Brewfile's dependencies are not satisfied (run `zb bundle install`)
$ echo $?
1
$ zb bundle install && zb bundle check
...
==> The Brewfile's dependencies are satisfied.
```

- It reads the Brewfile with the same parser as `bundle install` (`load_manifest`), and `-f` works the same way.
- Each entry is looked up under the name `zb install` records it as: `normalize_formula_name` turns `homebrew/core/jq` into `jq` and `homebrew/cask/x` into `cask:x`, tap formulae keep their full name, and casks are `cask:<token>`.
- Missing entries are listed as written in the Brewfile. Unlike `brew bundle check`, the list is printed without `--verbose`, since it's short and it's what you'd want to see next.
- Because `zb-brew` already forwards `bundle`, `brew bundle check` works through the opt-in `brew` alias too.

What it doesn't do:

- It only checks that each entry is installed, not that it's up to date. `brew bundle check` also treats outdated formulae as unsatisfied (unless `--no-upgrade`); here, `zb outdated` covers that.
- An entry written as an alias or old name (`brew "python"`) is recorded under its canonical name when installed, so the check reports it as missing every time. That errs on the safe side (the `.envrc` just runs `bundle install` again), and Brewfiles from `zb bundle dump` use canonical names. Resolving aliases would mean following the `opt/` links or asking the API, so I left it out; happy to add it if you want.

I went with the `check` half of the issue and left `bundle install` as it is. Skipping already-installed entries in `install` would change what it does when something is installed but outdated or unlinked, which seemed like your call to make.

Tests: `check_file` against a temporary database (everything installed passes; one missing formula fails), `missing_entries` with core, cask and tap names, and parsing `zb bundle check -f <file>`. README and CHANGELOG (Unreleased, Added) are updated.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Testing

- `cargo test -p zb_cli --lib bundle`: the new tests pass. With the name normalisation removed from `missing_entries`, `missing_entries_uses_installed_names` fails; on `main`, `zb bundle check` is `error: unrecognized subcommand 'check'`.
- By hand on Linux with a fresh `ZEROBREW_ROOT`: exits 1 and lists `jq` and `cask:firefox`; after recording both as installed it exits 0 with "The Brewfile's dependencies are satisfied."
- `cargo test -p zb_cli --no-fail-fast` on Linux x86_64 (Rust 1.96): everything else passes except four tests that fail the same way without this change because I ran them as root (`init::tests::is_writable_returns_false_for_readonly_dir`, `init::tests::needs_init_when_not_writable`, and two installer tests in `zb_cli/tests`).
- `cargo clippy --workspace --all-targets -- -D warnings` and `cargo fmt --all -- --check` are clean.
