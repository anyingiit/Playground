# Audit — scikit-hep/hist @ 52303af (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/hist` + manual review of auto-executing files.

| Hit | Reviewed | Verdict |
|---|---|---|
| tests/conftest.py | Sets matplotlib Agg backend and defines Hist/BaseHist/NamedHist (+ optional dask) fixtures; no I/O, no network, no subprocess | benign |
| noxfile.py | Sessions only run `session.install` (prek, pylint, `-e.[plot]`, dependency groups), pytest, mypy, sphinx; nothing downloaded outside PyPI | benign |
| .pre-commit-config.yaml | Standard public hooks (blacken-docs, pre-commit-hooks, ruff, mypy, codespell, pygrep-hooks, shellcheck-py) pinned to tags | benign |
| Build backend | hatchling + hatch-vcs (pyproject.toml); no custom build hooks | benign |

Pattern findings: none. Committed binaries: none. npm hooks: none.

Verdict: nothing malicious; safe to `uv sync` (PyPI deps), run pytest and the pre-commit hooks.
