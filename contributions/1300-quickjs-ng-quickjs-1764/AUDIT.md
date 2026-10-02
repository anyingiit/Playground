# AUDIT — quickjs-ng/quickjs (shallow clone @ 6a9b531, 2026-10-01)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/quickjs-ng-quickjs` (203 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing install/build/test hooks | none reported | benign |
| npm lifecycle hooks | none (no package.json in build path) | benign |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |
| Manual: `CMakeLists.txt`, `Makefile` grep for `download/FetchContent/ExternalProject/execute_process/curl/wget` | no matches; plain C compile of in-tree sources | benign |
| Manual: `Makefile` `test` target | runs in-tree `run-test262 -c tests.conf` (only `tests/*.js`) | benign |
| Manual: `unicode_download.sh` | not invoked by build/test (only manual Unicode table regeneration) | not run |

Verdict: no malicious code found; safe to build with cmake and run `tests/`.
