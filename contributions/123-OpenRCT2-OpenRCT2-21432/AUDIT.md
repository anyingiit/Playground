# Audit — OpenRCT2/OpenRCT2 @ e9fedc1 (develop, shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/OpenRCT2` (1638 text files scanned) + manual review of the CMake configure/build path that is executed locally.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks / npm lifecycle hooks | none found | — |
| `src/openrct2-android/gradle/wrapper/gradle-wrapper.jar` (committed binary) | Standard Gradle wrapper for the Android port; Android build is not run here | benign / not executed |
| `cmake/download.cmake:34` `file(DOWNLOAD …)` | Helper `download_openrct2_zip` with `EXPECTED_HASH SHA256`; only called from install() steps gated by `DOWNLOAD_TITLE_SEQUENCES/OBJECTS/OPENSFX/OPENMUSIC/REPLAYS` (all set OFF here) and the macOS dylib path (not Linux) | benign; not triggered |
| `src/openrct2-android/app/src/main/CMakeLists.txt:22` `ExternalProject_Add(libs` | Android-only dependency fetch; not part of the Linux build | benign / not executed |
| `.github/workflows/localisation.yml:15-17` writes deploy key to `~/.ssh/id_rsa` | CI workflow using a repo secret to push translations; runs only on GitHub Actions | benign / not executed |
| `CMakeLists.txt:185-210` `execute_process` | `git rev-parse` / branch / describe to embed version info | benign |

Configure flags used locally: `-DDISABLE_HTTP=ON -DDOWNLOAD_*=OFF` (no network at build time).

Verdict: nothing malicious; safe to configure, build (`ninja`) and run the gtest suite (`ctest`).
