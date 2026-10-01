# Audit — EvoScientist/EvoScientist @ 9ef018e (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/EvoScientist` (456 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/conftest.py` (auto-run) | read in full (163 lines) | Benign — plain fixtures (sample dicts, tmp workspace, RUNTIME isolation under tmp_path, deepagents patch reset, dotenv isolation). No network/subprocess. |
| `.pre-commit-config.yaml` | read | Benign — only ruff-check / ruff-format from astral-sh. Not installed/run here. |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| pipe-to-shell (47) | sampled | Benign — onboarding TinyTeX install hint strings (user-triggered), and test fixtures asserting the dangerous-command guard *rejects* `curl x \| bash`. |
| secret-paths (1) `cli/file_mentions.py:348` | read | Benign — comment about not leaking `~/.ssh/id_rsa` via @-mentions. |
| webhook (1) `channels/telegram/probe.py:24` | read | Benign — Telegram Bot API `getMe` probe with user-configured token. |

Verdict: no malicious code found; safe to install deps with `uv sync --dev` and run pytest/ruff.
