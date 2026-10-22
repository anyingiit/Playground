# Malicious-code audit — square/kotlinpoet @ d438267 (main, 2026-09-26)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/square-kotlinpoet` (139 text files) + manual review of the build surface.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (tool) | none reported | benign |
| npm lifecycle hooks | none (only `kotlin-js-store/` lock files for Kotlin/JS) | benign |
| Pattern findings | none | benign |
| `gradle/wrapper/gradle-wrapper.jar` (committed binary) | sha256 `7a9ce74c…262c5d` == official Gradle wrapper checksum for 9.7.0/9.7.1 (checked against `services.gradle.org/versions/all` `wrapperChecksumUrl`) | benign (official jar) |
| `gradle-wrapper.properties` | `distributionUrl=https://services.gradle.org/distributions/gradle-9.8.0-bin.zip`, `distributionSha256Sum` == official `gradle-9.8.0-bin.zip.sha256` (`bafd5ce9…`), `validateDistributionUrl=true` | benign |
| `settings.gradle.kts` | repos mavenCentral/gradlePluginPortal; plugin `org.gradle.toolchains.foojay-resolver-convention` 1.0.0 (official Gradle plugin) | benign |
| `build.gradle.kts` (root) | well-known plugins only (Kotlin MPP/JVM, KSP, Dokka, Spotless 8.10.3 + ktfmt, vanniktech maven-publish, binary-compatibility-validator); JDK-toolchain test tasks only when `CI` env set; no `Exec`/downloads/network code | benign |
| `kotlinpoet/build.gradle.kts` | Kotlin MPP config (jvm, js, wasmJs with nodejs/mocha test tasks), test deps from Maven Central | benign; JS/Wasm tasks not run here (would download Node) |
| `.github/workflows/*.yml` | `./gradlew build`, `:kotlinpoet:check`, dokka, mkdocs; not run locally | benign |

**Verdict: no malicious code found. Safe to build/test with `./gradlew :kotlinpoet:jvmTest` and `spotlessCheck`.**
