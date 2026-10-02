# AUDIT — openrewrite/rewrite-cucumber-jvm @ 41933f4

`python3 tools/audit_repo.py` : 43 text files, no auto-exec hooks, no npm hooks, no pattern findings.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `gradle/wrapper/gradle-wrapper.jar` (committed binary, sha256 238e777f…) | Standard Gradle wrapper; `gradle-wrapper.properties` pins services.gradle.org gradle-9.8.0-bin.zip with `distributionSha256Sum` | benign |
| `settings.gradle.kts` | pluginManagement: mavenLocal, artifacts.codegenomeproject.org (org.openrewrite/io.moderne only, creds from env), Gradle plugin portal; Develocity build scan publishes only with access key | benign |
| `build.gradle.kts` | Only the openrewrite recipe-library / license plugins and declared dependencies; no Exec/download tasks | benign |
| `.github/workflows/*.yml` | Reuse openrewrite/gh-automation workflows; not executed locally | benign |
| `.claude/settings.json` | Tool permission allowlist for maintainers' assistant; not executed by build | benign |
| Tests (`src/test/java/**`) | Plain OpenRewrite `RewriteTest`s, no process/network code | benign |

Verdict: nothing malicious; OK to build and test.
