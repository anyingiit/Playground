# AUDIT — openrewrite/rewrite-cucumber-jvm @ 41933f4

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/rewrite-cucumber-jvm` (43 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface: none reported | `build.gradle.kts`, `settings.gradle.kts` read manually: only the standard `org.openrewrite.build.recipe-library` / license plugins, Develocity plugin (build-scan publishing only when an access key is set), plugin repos = codegenome Maven (credentials from env, absent here) + Gradle Plugin Portal | benign, standard OpenRewrite build |
| npm lifecycle hooks: none | — | n/a |
| Committed binary `gradle/wrapper/gradle-wrapper.jar` | sha256 `238e777f…21abd5` == official `https://services.gradle.org/distributions/gradle-9.8.0-wrapper.jar.sha256` | benign (official wrapper) |
| `gradle-wrapper.properties` | official `services.gradle.org` 9.8.0 distribution with `distributionSha256Sum` pinned | benign |
| `.claude/settings.json` | IDE/agent permission allow-list only, not executed by the build | benign |
| Pattern findings: none | — | — |

Verdict: no malicious code found; safe to run `./gradlew`.
