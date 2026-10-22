### Description

Adds an optional `description` field to entries in the `[environments]` table, as proposed in #7105, and shows it in `pixi info`:

```toml
[environments]
test = { features = ["test"], description = "Run the test suite" }
docs = { description = "Build the documentation" }
```

`pixi info` (excerpt):

```
        Environment: test
        Description: Run the test suite
           Features: test, default
   Dependency count: 0
...
        Environment: docs
        Description: Build the documentation
           Features: default
```

Changes:
- `pixi_manifest`: `TomlEnvironment` parses the new `description` key and `Environment` carries it (`Option<String>`). A `description` alone is enough to define an environment (like `solve-group` alone), resulting in an environment with only the default feature. `update_environment_features` / `remove_feature` keep the description when they rebuild the in-memory environment.
- `pixi_core`: `Environment::description()` accessor.
- `pixi info`: prints a `Description` line right below the environment name when set, and `pixi info --json` gets a `description` field (`null` when unset) in each `environments_info` entry.
- JSON schema: `description` added to `Environment` in `schema/model.py`, schema files regenerated, and `schema/examples/valid/full.toml` uses it.
- Docs: `docs/reference/pixi_manifest.md` documents the field.

Not included (happy to add if wanted): a `--description` option for `pixi workspace environment add`, and showing the description in other commands.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Fixes #7105

### How Has This Been Tested?

- New Rust unit tests in `pixi_manifest` (`test_parse_environment_description`, `test_parse_description_only_environment`, `test_environment_description`, `test_editing_environment_features_keeps_description`); they fail without the change (`'description' was not expected here`) and pass with it. Updated the four snapshots that list the accepted environment keys.
- `cargo test -p pixi_manifest`: all pass except `task::jinja_rendering_tests::tojson_stays_json`, which fails the same way on `main` when the crate is tested on its own.
- New Python integration test `test_pixi_info_environment_description` (text and `--json` output), plus the `description: None` entries added to the `test_info_output_extended` JSON snapshot.
- `pixi run test-schema` equivalent (`python model.py && pytest` in `schema/`): 102 passed, 1 skipped; `full.toml` fails validation against the old schema.
- `cargo test -p pixi --test integration_rust -- parse_valid` (parses `schema/examples/valid/*.toml` and the docs manifests): 4 passed; `-- environment feature`: 6 passed.
- `pytest --pixi-build=debug tests/integration_python/test_main_cli.py::{test_pixi_info_environment_description,test_info_output_extended,test_pixi_info_tasks} tests/integration_python/test_inline_environments.py`: 46 passed (the first two fail against a `main` build).
- `cargo fmt --all -- --check`, `cargo clippy -p pixi_manifest -p pixi_core -p pixi_cli --all-targets -- -D warnings`, `ruff check` / `ruff format --check`, `typos`, `tombi format --check` / `tombi lint`: all clean.

### AI Disclosure
- [x] This PR contains AI-generated content.
  - [x] I have tested any AI-generated content in my PR.
  - [x] I take responsibility for any AI-generated content in my PR.

Tools: Claude Code

### Checklist:
- [x] I have performed a self-review of my own code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] I have added sufficient tests to cover my changes.
- [x] I have verified that changes that would impact the JSON schema have been made in `schema/model.py`.
