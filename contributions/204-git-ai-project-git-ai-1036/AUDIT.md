# AUDIT — git-ai-project/git-ai (shallow clone of main @ 8a6184a, 2026-10-22)

`python3 -I tools/audit_repo.py <clone>` → 558 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface | none; no `build.rs`, no proc-macro crate in repo | benign |
| npm lifecycle hooks | none | benign |
| Committed binary `agent-support/intellij/gradle/wrapper/gradle-wrapper.jar` | standard Gradle wrapper for the IntelliJ plugin; not touched by `cargo` build/test | benign (not executed) |
| env-dump (17) in `scripts/benchmarks/**.py` | copy `os.environ` to pass to child git processes in benchmarks | benign (not run) |
| pipe-to-shell (10) | official installers (`usegitai.com/install.sh`, rustup, factory.ai CLI) in CI workflows, dev.sh, CI templates, WSL install string | benign; none run by `cargo test` |
| powershell-download (2) | `install.ps1` download of release binary; nightly CI | benign (not run) |
| long-base64-blob (1) | `tests/fixtures/amp-threads/*.json` thinking signature in a transcript fixture | benign data |
| secret-paths (1) | test asserting `.npmrc` is ignored | benign |
| `lefthook.yml` | pre-commit runs `task format:check/lint/doc` only (not installed here) | benign |

Only `cargo build/test/clippy/fmt` on the lib unit tests were run (tests use temp HOME dirs). Verdict: nothing suspicious.
