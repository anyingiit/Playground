# Audit — pyinstaller/pyinstaller @ cea3915d (develop, 2026-09-29)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pyinstaller` (1225 text files scanned). Reviewed before running anything.

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/functional/conftest.py`, `tests/unit/conftest.py`, `PyInstaller/utils/conftest.py` (pytest conftest) | Read: fixtures for building/running frozen test apps, compiling a test ctypes dylib from bundled C source, no network access | benign |
| `PyInstaller/utils/conftest.py:503` `eval(f.read())` | Evaluates the repo's own `tests/functional/logs/*.toc` pattern lists for multipackage tests | benign (test data in repo) |
| `PyInstaller/utils/conftest.py` subprocess/psutil | Launches the frozen test executables and kills their process tree on timeout | benign |
| `hatch_build.py` | Hatch build hook: if no bootloader for the platform, runs `python ./waf configure all` in `bootloader/` (local C build) | benign; not triggered (package not installed, tests run from source tree) |
| test-fixture `setup.py` files (4) | Tiny setuptools stubs used as test data | benign |
| committed binaries: Windows bootloaders `run*.exe`, 2–23 byte test stubs (.so/.dll/.dylib/.pyc) | Official prebuilt Windows bootloaders shipped by the project; tiny stubs are fake test files | benign, not executed |
| env-dump `dict(os.environ)` (waf, one test script) | Build tool copying env for subprocesses | benign |
| marshal/pickle loads | Core PyInstaller reading its own .pyc/archives; modulegraph test pickling | benign |
| `bootloader/Vagrantfile` powershell downloads (cygwin, chocolatey) | Developer VM provisioning only, not run by tests | benign, not used |

Verdict: **no malicious code found.** Only ran: a venv with the runtime deps (`altgraph`, `packaging`, `pyinstaller-hooks-contrib`, `setuptools`) plus pytest, executing tests from the source tree.
