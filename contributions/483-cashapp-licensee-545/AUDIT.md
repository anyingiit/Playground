# Malicious-code audit — cashapp/licensee @ 117a759 (trunk, 2026-10-01; re-verified same HEAD on resume)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/licensee-545` (246 text files scanned): no auto-executing hooks, no npm lifecycle hooks, no pattern findings. Committed binaries: `gradle/wrapper/gradle-wrapper.jar` and ~100 fixture `*.jar` files of 22 bytes each. Manual review below.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `gradle/wrapper/gradle-wrapper.jar` (48462 B) | sha256 `497c8c2a…a9c7` matches the official `https://services.gradle.org/distributions/gradle-9.5.1-wrapper.jar.sha256` | benign (official) |
| `gradle/wrapper/gradle-wrapper.properties` | official `services.gradle.org` gradle-9.5.1-bin.zip with `distributionSha256Sum` pinned | benign |
| `src/test/fixtures/**/repo/**/*.jar` (22 B each) | `build.gradle` `checkFixtureJars` enforces they all equal the empty-zip base64 `UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA==` (empty ZIP end-of-central-directory record); 22 bytes cannot carry code | benign |
| `settings.gradle` | `includeBuild("build-logic")`, standard repos (mavenCentral/google/gradlePluginPortal) | benign |
| `build-logic/` (included build, runs at configuration time) | `app.cash.licensee.repos.settings.gradle.kts` only declares repositories (Maven Central, Google, repo.gradle.org restricted to `org.gradle.experimental`); `GenerateSpdxIdTask` + `SpdxLicenses*.kt` + `defaultFallbackUrls.kt` generate Kotlin source (kotlinpoet) from the committed `licenses.json`; no exec / process / network | benign |
| `build.gradle` | standard plugins (kotlin, android-lint, publish, dokka, spotless, poko, buildConfig); `test` depends on publishing to local `build/localMaven`; `downloadLicensesJson` fetches spdx.org but is only run manually (not wired into build/test); publish secrets only in CI on trunk | benign |
| `.github/workflows/build.yaml` | `./gradlew build dokkaGenerate`; publishing only on trunk in cashapp/licensee | benign |
| Test fixtures (`src/test/fixtures/*/build.gradle`) | Gradle TestKit projects applying the plugin with a local `repo/` Maven dir | benign |

Verdict: **no malicious code found**; safe to build and run targeted tests under /home/user/work.
