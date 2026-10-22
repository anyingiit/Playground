# Audit — apache/iggy (scope: foreign/java, the only part built/run)

Clone: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/apache/iggy.git` @ 985b0ac1fb4d0e2d0f92afae50c2e3014604c5ff
Tool: `python3 /home/user/Playground/tools/audit_repo.py foreign/java` (407 text files)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-exec hooks / npm lifecycle | none reported | n/a |
| Committed binaries | none (gradle-wrapper.jar not committed, ASF policy) | n/a |
| long-base64-blob ×2 in `serde/MessagesBatchWireFormatTest.java` | hex golden wire frames used as test vectors | benign |
| `gradlew` wrapper-jar auto-fetch | downloads from `raw.githubusercontent.com/gradle/gradle/v9.7.1/...` and verifies a pinned SHA-256 | benign (official Gradle source, checksum-pinned) |
| `buildSrc/*.gradle.kts` (3 convention plugins) | only java/jacoco/application config | benign |
| `java-sdk/build.gradle.kts` | `git rev-parse --short HEAD` for version metadata; standard deps from Maven Central | benign |
| `settings.gradle.kts`, plugins (spotless, shadow) | well-known Gradle plugins, Maven Central / plugin portal | benign |
| Tests (`BaseIntegrationTest`) | start `apache/iggy:edge` Docker image via Testcontainers (official ASF image); no exec/ProcessBuilder in tests | benign |

Verdict: nothing malicious; OK to build and test.
