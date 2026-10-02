# Audit — repowise-dev/repowise @ 14ff7670 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/repowise` + manual review of every auto-executing surface (pytest conftests, pre-commit, build backends).

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` | Standard pre-commit-hooks, ruff, mypy mirrors, local `uv run pytest` on pre-push; not installed/run by us | benign / not run |
| `packages/*/vitest.config.ts` (5) | JS test configs; frontend not touched, not run | benign / not run |
| `tests/conftest.py` (autouse fixtures) | Monkeypatches telemetry `_post` to a no-op, sets `REPOWISE_SKIP_EDITOR_SETUP=1`, snapshots/restores DB-URL env vars, resets caches and structlog config. Protective, no network/exec | benign |
| `tests/unit/change_health/conftest.py:18` `subprocess.run` | Runs `git -C <tmp repo> ...` to build throwaway fixture repos | benign |
| `tests/unit/change_health/conftest.py:118-121` "network-call" | Python source string literals (`fetch(row)`) used as fixture content | benign (false positive) |
| other conftests (providers, generation, server, persistence, cli, distill, ingestion/parser, test_providers, server/mcp, server/services) | Only imports of repo modules, MockProvider/MockEmbedder, in-memory SQLite, httpx ASGITransport (`http://test`, in-process) | benign |
| env-dump `dict(os.environ)` in 2 tests | Copies env to pass to subprocess in tests; nothing sent anywhere | benign |
| `pickle.loads` (12) | Parse/walk caches (sealed with `unseal`) and pickle round-trip tests | benign |
| pipe-to-shell (8) | Install-hint strings for opencode, Dockerfile comment, test strings for a rewrite-hook guard | benign |
| secret-paths (9) | Matches on "local state"/"nonlocal statements" in comments | false positive |
| Build backends | root `setuptools.build_meta`, packages `hatchling`; no setup.py / custom hatch build hooks; no npm lifecycle hooks; no committed binaries | benign |

Verdict: nothing malicious; safe to `uv sync` and run `uv run pytest tests/unit/ingestion/...`, `tests/providers/`, `tests/unit/` and `ruff check .`.
