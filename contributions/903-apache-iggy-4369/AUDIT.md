# AUDIT — apache/iggy @ a08d0ca (shallow clone, 2026-10-01)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/iggy` (3078 text files).

Only `foreign/java` (Gradle) is built/run for this contribution (plus, if needed, the Rust `iggy-server` binary for integration tests).

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` hooks | read; standard lint/format hooks | benign (not run automatically here) |
| `foreign/python`, `bdd/python` conftest.py | not on our execution path | not executed |
| `core/server/build.rs`, `core/integration/build.rs`, `core/cli/build.rs`, `foreign/cpp/build.rs` | vergen-style build metadata / codegen; no network | benign |
| `foreign/node/package.json` prepare=husky | not executed | benign |
| long-base64-blob (24) | Go/Java/Swift golden wire-format hex fixtures | benign test data |
| pipe-to-shell (4) | Dockerfiles / echoed install hints (uv, nodesource, cargo-binstall) | benign, not executed |
| raw-ip-url (1) | 203.0.113.1 = TEST-NET-3 in a test assertion | benign |
| secret-paths (16) | comments about "local state" | false positives |
| Gradle: `foreign/java/buildSrc/*.kts`, `build.gradle.kts` | conventions plugins (java, jacoco, checkstyle, spotless); `git rev-parse --short HEAD` in java-sdk processResources | benign |
| `gradle-wrapper.properties` | official `services.gradle.org` gradle-9.7.1 distribution, `validateDistributionUrl=true` | benign |

Committed binaries: none (aside from standard gradle-wrapper.jar). Verdict: **no malicious code found; safe to build/test.**
