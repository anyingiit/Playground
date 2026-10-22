# Audit — ssrajadh/sentrysearch @ ab688137 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/sentrysearch` + manual review of pytest hooks, build backend and lockfile sources.

| Hit | Reviewed | Verdict |
|---|---|---|
| tests/conftest.py (pytest conftest, runs every session) | Imports only math/subprocess/pytest and sentrysearch modules; fixtures provide fake embedders/stores and synthetic videos | benign |
| tests/conftest.py:91, :112 `subprocess.run(` | Runs the imageio-ffmpeg bundled ffmpeg with `-f lavfi testsrc2` to generate 3s/10s 64x64 test MP4s into pytest tmp dirs; no network, no shell | benign |
| Build backend (pyproject.toml) | `hatchling`, no custom build hooks, no sitecustomize/.pth | benign |
| uv.lock sources | 165 from pypi.org, 9 from download.pytorch.org/whl/cu124 (torch for `local` extra only, not installed by `uv sync --group test`), 1 editable `.` | benign |
| npm hooks / committed binaries | none | n/a |

Verdict: nothing malicious; safe to run `uv sync --group test` and `uv run pytest`.
