## Description

`protobuf_generate()` only uses `IMPORT_DIRS` / `APPEND_PATH` (or `CMAKE_CURRENT_SOURCE_DIR` by default) to work out the relative path of each `.proto` and from that the `OUTPUT`s of the custom command. An import root passed as `PROTOC_OPTIONS --proto_path=...` (or `-I...`) is forwarded to protoc, but the function never sees it. If that directory contains the `PROTOS`, this either:

- fails at configure time with `could not find any correct proto include directory`, or
- declares outputs that protoc never writes. For example, CMake expects `<bin>/proto/foo/a_pb2.py`, but protoc writes `<bin>/foo/a_pb2.py` because the `PROTOC_OPTIONS` path comes first on the command line. The command then reruns on every build.

The issue is labeled `documentation`, so this PR only updates `docs/cmake_protobuf_generate.md` and keeps the behavior as is:

- The `PROTOC_OPTIONS` entry says not to pass the import directory of the `PROTOS` there, explains what goes wrong, and points to `IMPORT_DIRS` (or `APPEND_PATH`).
- The `IMPORT_DIRS` entry notes that each directory is passed to protoc as `-I`, so it is also the place for directories that only contain imported files.

I considered a configure-time warning for `-I`/`--proto_path` in `PROTOC_OPTIONS`, but it would also fire for working setups that pass an import-only directory there, so I left it out. Parsing `--proto_path` out of `PROTOC_OPTIONS` (the issue's first option) would be a behavior change; happy to follow up on that if you'd prefer it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #30162

## Testing

Docs-only change. I checked the documented behavior with a small standalone CMake project that includes `cmake/protobuf-generate.cmake`, using a real protoc (libprotoc 35.1 from grpcio-tools, `LANGUAGE python`, Ninja, CMake 3.28.3):

- `PROTOC_OPTIONS --proto_path=proto -Idep`: protoc reruns on every `ninja` invocation (the issue).
- `IMPORT_DIRS proto dep` (the documented way): second `ninja` prints `no work to do`.
- `IMPORT_DIRS proto` + `PROTOC_OPTIONS -Idep` (import-only directory): also `no work to do`, which is why the docs only warn about the import directory of the `PROTOS`.
