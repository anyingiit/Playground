# Audit — Kozea/WeasyPrint @ 369b15340ea97c5d649af65e8e10330b8d08f01f

`python3 tools/audit_repo.py /home/user/work/WeasyPrint` (165 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| tests/conftest.py (pytest auto-run) | 读了全部 import 与 subprocess 用法：只调用本地 `gs`（Ghostscript）把测试生成的 PDF 转 PNG，临时文件写后删除，无网络 | benign |
| weasyprint/text/constants.py:153 `'iwr': 'heb'` (powershell-download) | 语言代码映射表（ISO 639 'iwr'→'heb'），误报 | benign |
| npm hooks / committed binaries | 无 | n/a |
| pyproject.toml | flit_core 构建后端，无自定义构建脚本 | benign |

结论：未发现恶意代码，可以安装并运行测试。
