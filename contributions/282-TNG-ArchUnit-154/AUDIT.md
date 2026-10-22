# AUDIT: TNG/ArchUnit @ 5f0884eb (main, 2026-10-22)

`python3 tools/audit_repo.py /home/user/work/ArchUnit`: 1537 text files scanned.
- No auto-executing hooks and no npm lifecycle scripts.
- Committed binaries: the standard `gradle/wrapper/gradle-wrapper.jar` and small `.class`/`.jar` test fixtures under `archunit/src/test*/resources` (classfile importer tests). Expected for this project.
- One pattern hit: `archunit-maven-test/mvnw.cmd` downloads the Maven distribution (the standard Maven wrapper script). It was never run here.

Note: the audit ran after the first Gradle build, not before. The Gradle wrapper (official distribution from services.gradle.org with `validateDistributionUrl=true`) and Maven Central dependencies were the only things fetched. No plugin or script from outside the repository was executed.

Policy:
- No AGENTS.md and no PR template. CONTRIBUTING.md has no AI policy.
- Commits need a DCO sign-off (`Signed-off-by`), and a `Resolves: #n` trailer is suggested.
- No CLA.
