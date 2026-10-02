# Audit — Kotlin/dataframe @ 68c49eb5 (master, 2026-10-01)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/dataframe` (1770 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks | none reported | benign |
| `gradle/wrapper/gradle-wrapper.jar` (root, the only one we run) | sha256 `238e777f…21abd5` == official `services.gradle.org/distributions/gradle-9.8.0-wrapper.jar.sha256` | benign (official wrapper) |
| 24 other `gradle-wrapper.jar` / `maven-wrapper.jar` under `examples/projects/**`, `plugins/kotlin-dataframe` | standard wrapper jars of example/legacy projects; not used by the root build | benign, not executed |
| powershell-download x8 (`kotlin.bat`, `mvnw.cmd` in examples) | standard Kotlin toolchain / Maven wrapper bootstrap scripts, Windows only | benign, not executed |
| `gradle/gradle-daemon-jvm.properties` toolchain URLs | api.foojay.io (Gradle's standard JDK provisioning service) for JDK 21 | benign |
| `build-logic` `ProcessBuilder` | only in `testBuildingExamples` source set (builds example projects with Gradle); not run by `:core:test` | benign |
| `build-settings-logic`, `build-logic` convention plugins | read-through: Kotlin/ktlint/kodex/korro/BCV configuration only | benign |

Verdict: **no malicious code found**; safe to run `./gradlew` for `:core` compile/test/apiCheck/ktlint.
