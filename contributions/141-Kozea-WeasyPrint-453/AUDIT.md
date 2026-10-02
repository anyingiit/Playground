# Audit — Kozea/WeasyPrint @ 369b153 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/WeasyPrint` — 165 text files scanned, 0 committed binaries, no npm hooks.

| Hit | Reviewed | Verdict |
|---|---|---|
| `tests/conftest.py` (auto-run by pytest) | Read fully: fixtures + `document_write_png` runs local `gs` (Ghostscript) on a temp PDF to rasterise it; no network, no writes outside tempfile | benign |
| `weasyprint/text/constants.py:153` `'iwr': 'heb'` (powershell-download pattern) | Language-code mapping table (ISO 639 → OpenType tag) | false positive |
| `pyproject.toml` build backend | `flit_core` only, no custom build hooks | benign |

Verdict: nothing malicious; safe to install and run tests.
