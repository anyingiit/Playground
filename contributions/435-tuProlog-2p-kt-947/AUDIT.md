# AUDIT — tuProlog/2p-kt @ 4443ffd

Same repository and base commit as packages 421 and 433, which were audited in full (`tools/audit_repo.py`: no npm lifecycle hooks; gradle-wrapper.jar sha256 matches the official 9.8.2 checksum; `buildSrc` only runs `java -jar` on the project's own fat jars; the pre-commit plugin installs a Conventional Commits `commit-msg` hook). origin/master has not moved since (still 4443ffd), so that audit applies unchanged.

Build note: Maven Central returns HTTP 429 through the proxy, so builds use a local init script (in GRADLE_USER_HOME, not in the repo) pointing Maven Central to Google's mirror, with `--no-scan`. Only `jvmTest`, `ktlintCheck` and `detektAll` of `oop-lib` were run.

AI policy: AGENTS.md is a build guide for agents; no restriction on AI-assisted contributions (the maintainer triages these issues with Claude Code, see #1005). CLA/DCO: none.

Verdict: nothing suspicious.
