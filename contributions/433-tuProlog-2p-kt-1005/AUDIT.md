# AUDIT — tuProlog/2p-kt @ 4443ffd

Same repository and base commit as package 421, which was audited in full (`tools/audit_repo.py`: no npm lifecycle hooks; gradle-wrapper.jar sha256 matches the official 9.8.2 checksum; `buildSrc` only runs `java -jar` on the project's own fat jars; the pre-commit plugin installs a Conventional Commits `commit-msg` hook). origin/master has not moved since (still 4443ffd), so that audit applies unchanged.

Build note: Maven Central returns HTTP 429 through the proxy, so builds use a local init script (in GRADLE_USER_HOME, not in the repo) pointing Maven Central to Google's mirror, with `--no-scan`. Only `jvmTest`, `ktlintCheck` and `detektAll` of `solve`, `test-solve`, `solve-prolog`, `solve-problog` were run.

AI policy: AGENTS.md is a build guide for agents; the maintainer's own triage comment on #1005 was written with Claude Code. No restriction. CLA/DCO: none.

Verdict: nothing suspicious.
