# Malicious-code audit — TheAlgorithms/C-Plus-Plus @ b64d5ec (master, 2026-09-30)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/C-Plus-Plus` (416 text files), then manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks / committed binaries | none reported | — |
| `graphics/CMakeLists.txt:7` `ExternalProject_Add` | downloads official freeglut 3.8.0 release tarball from github.com/freeglut with pinned SHA256, only when OpenGL is found but GLUT is not; builds it as a static lib | benign (and not triggered here: only `doxygen` was run, no CMake configure of the graphics dir) |
| `scripts/file_linter.py` | runs clang-format/clang-tidy over changed files listed in `git_diff.txt` (CI only) | benign, not run |
| `.github/workflows/*.yml` | standard CI: cmake build, clang-format lint, doxygen → gh-pages | benign |
| `doc/Doxyfile` | plain Doxygen config; no `INPUT_FILTER`/`FILTER_PATTERNS` commands executing external programs | benign |

Verdict: **no malicious code found**. Only `doxygen` (Debian package) was run on the sources, which does not execute any repo code.
