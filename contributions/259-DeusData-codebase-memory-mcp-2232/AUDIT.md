# Malicious-code audit — DeusData/codebase-memory-mcp @ 0f52d30c (main, 2026-09-30)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/codebase-memory-mcp` (2069 text files), then manual review of everything that runs on build/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface | tool reports none (no setup.py/conftest/build.rs) | — |
| `pkg/npm/package.json` postinstall `node install.js` | npm wrapper that downloads the release binary from GitHub Releases with checksum verification; not used by the C build/tests, not run here | benign |
| `vendored/nomic/code_vectors.bin` (31 MB) | committed embedding data file read by the product; never executed | benign |
| `tests/test_security.c` `rm -rf /`, `curl ... \| sh` strings | inputs to `cbm_validate_shell_arg` asserted to be REJECTED | benign |
| env-dump `dict(os.environ)` in scripts/tests (*.py) | copies env to spawn the product binary under test; nothing sent anywhere | benign |
| `install.sh` curl\|bash comments | documented user install path; not run | benign |
| `test-infrastructure/vm/provision-windows.sh`, `scripts/setup-windows.ps1` Invoke-WebRequest | Windows VM/dev provisioning with hash checks; not run | benign |
| secret-paths (`.ssh`, `.gnupg`, `.aws`) | deny-lists for sensitive dirs and test fixtures for that classifier | benign |
| `Makefile.cbm` | compiler invocations only; only network use is `npm ci` in the frontend target (not used); test targets just build and run `build/c/test-runner` | benign |
| `scripts/test.sh` / `scripts/clean.sh` | clean.sh `rm -rf` limited to repo build dirs/node_modules and the user's own `/tmp/cbm_*`/`/tmp/cli-*` dirs | benign |
| `.github/workflows/*` | build/test/lint/DCO/CodeQL; not run locally | benign |

Verdict: **no malicious code found**. Only built and ran `make -f Makefile.cbm` test/lint targets (`test-focused`, `lint-ci`) in /home/user/work/codebase-memory-mcp.
