# AUDIT — wiktor-k/ssh-agent-lib @ 3114e4e

- `tools/audit_repo.py`: Pattern findings: none. No git hooks.
  - Binaries: only the protocol message fixtures in `tests/messages/*.bin`, which are read as test data and never executed.
  - The fixture sizes are normal: 1–1837 bytes.
- No build.rs. `.justfile` was read in full:
  - checks: codespell, `just --fmt`, nightly fmt, clippy, cargo deny, tests;
  - nothing downloads or executes external scripts beyond the cargo dependencies.
- CI (`.github/workflows/*.yml`): rust.yml, misc.yml, all.yml and dco.yml. dco.yml requires a Signed-off-by line.
- AI policy: there is no AI clause in CONTRIBUTING or README. The PR body still includes a disclosure paragraph.
- Builds and tests ran in an isolated cloud container with CARGO_TARGET_DIR outside the repo.
