# Audit — decompme/decomp.me @ 4ab701a (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/decomp.me` + manual review of the backend code that runs during tests.

| Hit / area | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (setup.py / conftest / build hooks) | none found | — |
| frontend/package.json `postinstall = next telemetry disable` | Only disables Next.js telemetry; frontend is not installed or run here | benign / not run |
| Committed binaries | none | — |
| Pattern findings | none | — |
| backend/pyproject.toml deps (`asm-differ`, `m2c`, `drf-extensions` from git+https GitHub) | Well-known upstream projects pinned via uv.lock; installed with `uv sync --locked` into a venv in the work dir | benign |
| backend/compilers/download.py (the file being changed) | Downloads compiler images from ghcr.io; tests mock `get_compiler_raw`, so no network access happens in the new tests | benign |
| backend/decompme/settings.py / manage.py | Standard Django settings from env vars; no network or shell on import | benign |

Verdict: nothing malicious; safe to run `uv sync`, `ruff`, `mypy` and `manage.py test` on the backend.
