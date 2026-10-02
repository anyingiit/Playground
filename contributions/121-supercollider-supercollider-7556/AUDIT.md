# Audit — supercollider/supercollider @ develop 7e6f20928cc4

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/supercollider` (5247 text files scanned).

| Hit | Review | Reached here? |
|---|---|---|
| `.pre-commit-config.yaml` | Standard pre-commit-hooks (check-merge-conflict/case-conflict) + local hooks calling `tools/clang-format.py` and `tools/remove_trailing_blank_lines.py`. Only runs when a developer installs pre-commit. | No — pre-commit not installed/run. |
| `platform/windows/lib/libsndfile.dll` (325 KB) | Prebuilt Windows libsndfile shipped for Windows builds. | No — never loaded on Linux. |
| `external_libraries/portaudio/CMakeLists.txt:40` `file(DOWNLOAD https://www.steinberg.net/asiosdk)` | Downloads the official Steinberg ASIO SDK from the vendor URL, only inside the Windows/ASIO branch of the portaudio build. | No — Linux, portaudio not built. |

No npm lifecycle hooks, no obfuscated code, no suspicious network calls in code paths touched.

Submodules fetched for the build (pinned commits from `git ls-tree`): nova-simd b61e579, nova-tt b497ec3, yaml-cpp 56e3bb5, utf8proc b3e0f28. `audit_repo.py` on each: no hooks, no binaries, no findings, except utf8proc `CMakeLists.txt:82-83 file(DOWNLOAD unicode.org test data)` which is inside `if(UTF8PROC_ENABLE_TESTING)` (off; SC adds it via `add_subdirectory` without testing) and a commented-out appveyor line — not reached.

What was actually executed:
- `g++` compiling a standalone harness that `#include`s `server/plugins/LFUGens.cpp`;
- `cmake -G Ninja` (Linux, Qt/IDE/supernova/HID/Link/avahi off) + `ninja -j2` in `build/` — reviewed top-level CMake: no downloads on this path (the ASIO download is Windows only);
- the built `scsynth` / `sclang` running `TestCoreUGens` against a local `jackd --no-realtime -d dummy`;
- `clang-format` on the changed hunk.
apt packages installed from Ubuntu archive: libsndfile1-dev libfftw3-dev libjack-jackd2-dev libasound2-dev libreadline-dev jackd2 cmake ninja-build.

**Verdict: safe** for the verification performed.
