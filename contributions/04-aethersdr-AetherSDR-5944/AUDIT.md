# Malicious-code audit — aethersdr/AetherSDR (main, 2026-09-24)

Tool: `python3 tools/audit_repo.py` + manual review. **Verdict: no malicious code found.**

| Hit | Location | Reviewed verdict |
|---|---|---|
| CMake downloads ×11 | `FetchContent_Declare(whisper_gpu_prebuilt)`, `hal-plugin` libASPL (macOS), vendored whisper.cpp/KleidiAI, radae `BuildOpus.cmake` ExternalProject + `PatchOpusNnet.cmake file(DOWNLOAD)` | Benign: fetch pinned upstream dependencies (whisper.cpp, Opus, KleidiAI) from their official hosts; GPU/whisper paths are off by default on Linux. We configured with `ENABLE_RADE=OFF` so the Opus fetch never ran; the only download observed was the tarball verification of `third_party/opus-rade` from the repo itself |
| PowerShell `Invoke-WebRequest` ×15 | `scripts/setup/setup-*.ps1` | Benign: Windows dependency bootstrap scripts (FFTW, PortAudio, Vulkan SDK…) from official URLs; not run on Linux or by tests |
| `curl … sh.rustup.rs \| sh` | `scripts/setup/setup-deepfilter.sh` (comment + echo) | Benign: printed installation hint only |
| `dict(os.environ)` | `tools/verify_slice0_rx.py` | Benign: env for a child process in a dev tool |
| committed binary | `third_party/fftw3/bin/libfftw3-3.dll` | Windows FFTW runtime shipped for Windows builds; never loaded on Linux |
| "secret-paths" ×11 | "local state" comments, zlib FAQ | False positives |

What was executed here: CMake configure + `make` of `aethercore` and `hl2_*` test targets; `ctest -R hl2_`; `tools/check_*.py`.
