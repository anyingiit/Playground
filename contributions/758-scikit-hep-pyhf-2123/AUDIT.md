# Audit — scikit-hep/pyhf @ efa6eb09 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pyhf` (247 text files) + manual review of every auto-executing hook and of the tbump-related release files.

| Hit | Reviewed | Verdict |
|---|---|---|
| .pre-commit-config.yaml | Standard public hooks only (pre-commit-hooks v6.0.0, pygrep-hooks, ruff, blacken-docs, mypy, codespell, check-jsonschema, zizmor); no local/script hooks | benign |
| noxfile.py | Sessions lint (prek), tests (pip/uv install `.[all]` + pytest), coverage, regenerate, docs, notebooks, build; no network/shell beyond package installs | benign |
| src/conftest.py | doctest fixtures only (tarfile JSON reader, events/backends reset) | benign |
| tests/conftest.py | backend parametrization fixtures, datadir copytree, sets `CUDA_VISIBLE_DEVICES=""` | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| Pattern findings | none | n/a |
| Build backend | hatchling + hatch-vcs (pyproject.toml), no custom build hooks besides vcs version file | benign |
| ci/validate-version.py, .github/workflows/release-{prepare,tag}.yml | read `tbump.toml` via tomllib / run `uvx tbump`; no secrets used outside environment-gated steps | benign (will be touched by the change) |

Verdict: nothing malicious; safe to install `tbump` in a throwaway venv and run `tbump --dry-run` / `tbump current-version` and `ci/validate-version.py` locally. Not required to run the full pyhf test suite (config-only change).
