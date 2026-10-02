# Audit — protocolbuffers/protobuf @ 1d2f6fa4 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/protobuf` (2185 text files) + manual review of every hit.
Planned execution scope: only a tiny standalone CMake project that `include()`s `cmake/protobuf-generate.cmake` and runs `cmake` configure (plus, if needed, a targeted `-j2` build of `protoc`). Nothing from python/, rust/, csharp/ is executed.

| Hit | Reviewed | Verdict |
|---|---|---|
| python/protobuf_distutils/setup.py (setup.py hook) | Standard setuptools metadata for the distutils extension; not run here | benign / not run |
| rust/release_crates/*/build.rs (4 cargo build scripts) | Invoke protoc codegen for release crates; not run here | benign / not run |
| cmake/gtest.cmake, abseil-cpp.cmake, conformance.cmake `FetchContent_Declare` | Fetch googletest / abseil-cpp / jsoncpp from their official github.com repos at pinned version tags, only when not found locally | benign (well-known deps) |
| cmake/examples.cmake `ExternalProject_Add` | Builds the in-tree examples/ directory as an external project; no download | benign |
| src/google/protobuf/cpp_features.pb.h:69 long base64-like string | Serialized FeatureSetDefaults embedded by the generator (generated code) | benign |
| src/google/protobuf/descriptor_unittest.cc:16437 | Long "aaaa…" package name in a test fixture | benign |
| python/google/protobuf/internal/message_test.py `pickle.loads` | Round-trips pickled protobuf messages created in the same test | benign / not run |
| csharp/install_dotnet_sdk.ps1 `Invoke-WebRequest` | Downloads the official https://dot.net/v1/dotnet-install.ps1 for CI; not run (no pwsh) | benign / not run |
| python/protobuf.h:91 "secret-paths" | False positive: comment text "thread-local state" | benign |
| cmake/protobuf-generate.cmake (file to change) | Pure CMake function: argument parsing + add_custom_command; no network/exec at configure time | benign |

No committed binaries, no npm lifecycle hooks.

Verdict: nothing malicious; safe to run CMake configure on a small test project using `cmake/protobuf-generate.cmake`, and (if needed) a targeted CMake build of protoc.
