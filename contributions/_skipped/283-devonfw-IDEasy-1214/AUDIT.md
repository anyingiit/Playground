# AUDIT: devonfw/IDEasy @ 616cffc (main, 2026-10-22)

`python3 tools/audit_repo.py /home/user/work/IDEasy`: 1432 text files scanned.
- No auto-executing hooks and no npm lifecycle scripts. `install-hooks.sh` / `git-hooks/` exist but were not installed.
- Committed binaries are tiny dummy `.exe`/`.jar` test fixtures (0–600 bytes) under `cli/src/test/resources/ide-projects`.
- The 79 "powershell-download" hits are false positives: the Java class name `UrlDownloadFile` in url-updater.

Only Maven builds/tests of the `cli` module were run (`mvn test`, `spotless:check`, `checkstyle:check`). Dependencies came from Maven Central. JDK 25 (required by the pom) was downloaded from Adoptium (Temurin 25.0.5+8) into /home/user/work/jdk25.

Policy:
- AGENTS.md welcomes AI agents but **forbids any AI attribution** in commits, PR titles/descriptions and comments ("generated with", Co-authored-by, etc.). So pr_body.md has no disclosure paragraph. Do not add one, and do not add `Assisted-by` trailers.
- CLA via cla-assistant (SAP), signed once on the first PR. The doc says to give the email address used in commits. Field list not verifiable without login; probably name + email.
- The PR template asks for the issue to be assigned / In Progress. Optional; a short comment on the issue before opening is enough.
