# AUDIT — tuProlog/2p-kt @ 4443ffd

`python3 tools/audit_repo.py` (1946 text files): no npm lifecycle hooks (package.json only has a semantic-release devDependency), no pattern findings.

| Hit | Reviewed | Verdict |
|---|---|---|
| `gradle/wrapper/gradle-wrapper.jar` | sha256 3b8a2577…e98 matches the official `gradle-9.8.2-wrapper.jar.sha256` from services.gradle.org; distributionUrl is services.gradle.org with validateDistributionUrl=true | benign |
| `io-lib/src/commonTest/resources/.../random.bin` (1 KB) | Test fixture for IO lib reads; never executed | benign |
| `buildSrc/` (Gradle build logic, runs at build time) | grep for exec/ProcessBuilder/network: only `FatJarVerification.kt` runs `java -jar` on the project's own fat jars (task not invoked here) | benign |
| settings plugin `org.danilopianini.gradle-pre-commit-git-hooks` | Installs `.git/hooks/commit-msg` (a Conventional Commits regex check, read in full) | benign |

Build note: Maven Central returned HTTP 429 through the proxy, so the build was run with a local init script (in GRADLE_USER_HOME, not in the repo) that points Maven Central to Google's mirror `maven-central.storage-download.googleapis.com`, and with `--no-scan`. Ran only `:dsl-theory:jvmTest`, `ktlintCheck`, `detektAll`. Verdict: nothing suspicious.
