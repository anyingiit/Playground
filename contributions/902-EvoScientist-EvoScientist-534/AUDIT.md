# AUDIT — EvoScientist/EvoScientist @ 9ef018e (shallow clone, 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/EvoScientist` → 456 text files scanned, 0 committed binaries, no npm hooks.

| Hit | Reviewed | Verdict |
|---|---|---|
| tests/conftest.py (auto-runs) | 全文审阅：仅 pytest fixtures、monkeypatch EvoScientist 内部模块（langgraph_dev.manager、deepagents patches），无网络/子进程/文件系统外部写入 | benign |
| .pre-commit-config.yaml | 仅 ruff-check / ruff-format（astral-sh/ruff-pre-commit v0.15.17）；本次不安装 pre-commit | benign |
| pyproject.toml build-system | setuptools 标准构建，无自定义 setup.py | benign |
| pipe-to-shell ×47 | 均为危险命令检测的测试字符串（`curl x \| bash`）或 onboarding 中可选的 TinyTeX 安装提示文案（用户主动触发，非安装/测试期执行） | benign |
| secret-paths ×1 (cli/file_mentions.py:348) | 注释，说明要保护 `~/.ssh/id_rsa` 这类敏感路径 | benign |
| webhook ×1 (channels/telegram/probe.py) | Telegram getMe 探针，用户配置 token 时才调用；测试中不触网 | benign |

结论：未发现恶意代码，可以运行 `uv sync --dev` / `uv run pytest` / `uv run ruff`。
