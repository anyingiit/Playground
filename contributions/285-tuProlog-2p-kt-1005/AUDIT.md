# AUDIT: tuProlog/2p-kt @ 4443ffd (master, 2026-10-22, release 3.0.5)

`python3 tools/audit_repo.py /home/user/work/2p-kt`: 1947 text files scanned.
- No auto-executing hooks, no npm lifecycle scripts, no pattern findings.
- Committed binaries: `gradle-wrapper.jar` and a 1 KB `random.bin` test resource.

Only Gradle tasks of the `solve`, `test-solve`, `solve-prolog` and `solve-problog` modules were run (`jvmTest`, `ktlintCheck`, `detekt`), with the official Gradle wrapper. `jsTest` could not run because yarn could not be downloaded.

Policy:
- The root AGENTS.md is written for AI agents (build and lint tips) and has no restriction on AI contributions. The maintainer's own triage comment on #1005 says it was done by Claude Code. So the disclosure paragraph is fine.
- No CONTRIBUTING, CLA or DCO, and no PR template.
- Commits use Conventional Commits (`fix(...)`, `chore(...)`) and releases are semantic-release driven, so the commit message type matters.
