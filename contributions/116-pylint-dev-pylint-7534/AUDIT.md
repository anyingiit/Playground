# Audit — pylint-dev/pylint @ 8e75f579113a0e774d0eab2d5fee4354a56664a8

工具：`python3 tools/audit_repo.py /home/user/work/pylint`（扫描 2783 个文本文件）

| Hit | 复核 | 结论 |
|---|---|---|
| `.pre-commit-config.yaml` | 只有标准 hook（ruff/black/isort/mypy 等），本次没有运行 pre-commit | benign |
| `tox.ini`、`tests/config/functional/tox/unrecognized_options/tox.ini` | tox 环境定义；后者是配置解析测试的数据文件 | benign |
| `pylint/config/_pylint_config/setup.py` | 不是 setuptools 的 setup.py，是 `pylint-config` 命令的 argparse 设置代码 | benign |
| `tests/conftest.py` | 只有 PyLinter fixture、环境变量清理、pytest 选项和 skip 标记，无网络/子进程 | benign |
| `tests/checkers/conftest.py`、`tests/config/conftest.py` | 只定义路径常量 / fixture | benign |
| `tests/message/conftest.py`、`tests/pyreverse/conftest.py` | 只 import pylint/astroid/pytest，构造测试对象 | benign |
| 构建后端 | `pyproject.toml`：`setuptools.build_meta`，无自定义构建脚本 | benign |
| npm hooks / 二进制 / 可疑模式 | 无 | — |

结论：未发现恶意代码，可以安装并运行测试。
