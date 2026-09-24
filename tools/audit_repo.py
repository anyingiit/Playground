#!/usr/bin/env python3
"""Static "is this repo safe to clone, install and run tests from?" audit.

Heuristic, not a proof: it lists everything that would EXECUTE on install,
build or test, plus common malware/obfuscation/exfiltration markers, so a
human can review each hit. Usage:

    python3 tools/audit_repo.py <repo-dir> [--json]

Exit code is 0 always; read the report.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "target", ".venv", "venv", ".tox", "dist", "build",
    "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache", ".next",
}
TEXT_EXT = {
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".rs", ".go", ".sh",
    ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".cmake", ".toml", ".cfg", ".ini",
    ".yml", ".yaml", ".json", ".c", ".cc", ".cpp", ".h", ".hpp", ".rb", ".pl",
    ".java", ".kt", ".gradle", ".mk", "",
}
TEXT_NAMES = {"Makefile", "Dockerfile", "CMakeLists.txt", "Justfile", "Rakefile"}
BINARY_EXT = {".exe", ".dll", ".so", ".dylib", ".jar", ".class", ".pyc", ".node", ".bin", ".scr", ".msi"}

# Places whose code runs automatically during install / build / test.
EXEC_SURFACE = [
    (re.compile(r"(^|/)setup\.py$"), "python setup.py (runs on sdist install)"),
    (re.compile(r"(^|/)conftest\.py$"), "pytest conftest (runs on every test session)"),
    (re.compile(r"(^|/)build\.rs$"), "cargo build script (runs on build/test)"),
    (re.compile(r"(^|/)(tox|noxfile)\.(ini|py)$"), "tox/nox config"),
    (re.compile(r"(^|/)(jest|vitest|playwright)\.(config|setup)[^/]*$"), "JS test runner config"),
    (re.compile(r"(^|/)\.(husky|githooks)/"), "git hooks"),
    (re.compile(r"(^|/)\.pre-commit-config\.yaml$"), "pre-commit hooks"),
    (re.compile(r"(^|/)(global-setup|globalSetup|setupTests)[^/]*$"), "JS test global setup"),
]

PATTERNS = [
    # remote code execution / download-and-run
    ("pipe-to-shell", r"(curl|wget)[^\n|]{0,200}\|\s*(sudo\s+)?(ba|z)?sh\b"),
    ("powershell-download", r"(Invoke-WebRequest|iwr|DownloadString|DownloadFile)\b"),
    ("cmake-download", r"\b(file\s*\(\s*DOWNLOAD|FetchContent_Declare|ExternalProject_Add)\b"),
    # obfuscated execution
    ("eval-decoded", r"(eval|exec|Function)\s*\(\s*(atob|Buffer\.from|base64\.b64decode|codecs\.decode|bytes\.fromhex|zlib\.decompress|marshal\.loads)"),
    ("marshal/pickle-exec", r"\b(marshal\.loads|pickle\.loads)\s*\("),
    ("long-base64-blob", r"['\"][A-Za-z0-9+/]{300,}={0,2}['\"]"),
    ("hex-escaped-blob", r"(\\x[0-9a-fA-F]{2}){40,}"),
    ("js-obfuscator", r"_0x[0-9a-f]{4,6}\s*[\(\[=]"),
    # exfiltration / C2 endpoints
    ("webhook/paste/tunnel", r"(discord(app)?\.com/api/webhooks|api\.telegram\.org/bot|pastebin\.com|hastebin|ngrok\.io|ngrok-free\.app|requestbin|pipedream\.net|webhook\.site|transfer\.sh|0x0\.st)"),
    ("raw-ip-url", r"https?://(?!127\.0\.0\.1|0\.0\.0\.0|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)\d{1,3}(\.\d{1,3}){3}"),
    # credential harvesting
    ("secret-paths", r"(\.ssh/id_|\.aws/credentials|\.npmrc|\.pypirc|\.docker/config\.json|\.kube/config|Login Data|Local State|wallet\.dat|\.gnupg)"),
    ("env-dump", r"(JSON\.stringify\(\s*process\.env\s*\)|dict\(\s*os\.environ\s*\)|os\.environ\.copy\(\)\s*\)|printenv\s*\|)"),
    ("crypto-miner", r"(stratum\+tcp|xmrig|coinhive|cryptonight|minexmr)"),
    # destructive
    ("destructive", r"rm\s+-rf\s+(--no-preserve-root\s+)?(/|~|\$HOME)(\s|$|/\*)"),
    ("reverse-shell", r"(/dev/tcp/\d|nc\s+-e\s|bash\s+-i\s+>&|socket\.socket\([^)]*\)[^\n]{0,80}\.connect\([^\n]{0,80}subprocess)"),
]
PATTERNS = [(name, re.compile(rx, re.IGNORECASE)) for name, rx in PATTERNS]

# Only interesting inside auto-executing files (would be noise elsewhere).
EXEC_ONLY = [
    ("process-spawn", re.compile(r"\b(subprocess\.|os\.system|os\.popen|child_process|execSync|spawnSync|std::process::Command|Command::new)")),
    ("network-call", re.compile(r"\b(requests\.(get|post)|urllib\.request|urlopen|http\.client|fetch\(|axios|reqwest::|ureq::|curl\s|wget\s|socket\.)")),
]

NPM_HOOKS = ("preinstall", "install", "postinstall", "prepare", "prepublish", "preprepare", "postprepare")


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            yield Path(dirpath) / f


def rel(root: Path, p: Path) -> str:
    return str(p.relative_to(root))


def audit(root: Path) -> dict:
    report = {"repo": str(root), "exec_surface": [], "npm_hooks": [], "binaries": [],
              "findings": [], "files_scanned": 0}
    for path in iter_files(root):
        r = rel(root, path)
        suffix = path.suffix.lower()
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if suffix in BINARY_EXT:
            report["binaries"].append({"file": r, "bytes": size})
            continue
        is_exec_surface = None
        for rx, why in EXEC_SURFACE:
            if rx.search(r):
                is_exec_surface = why
                report["exec_surface"].append({"file": r, "why": why})
                break
        if path.name == "package.json":
            try:
                pkg = json.loads(path.read_text(encoding="utf-8", errors="replace"))
                scripts = pkg.get("scripts", {}) if isinstance(pkg, dict) else {}
                for hook in NPM_HOOKS:
                    if hook in scripts:
                        report["npm_hooks"].append({"file": r, "hook": hook, "cmd": scripts[hook]})
            except (ValueError, OSError):
                pass
        if not (suffix in TEXT_EXT or path.name in TEXT_NAMES) or size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        report["files_scanned"] += 1
        checks = list(PATTERNS) + (EXEC_ONLY if is_exec_surface else [])
        for lineno, line in enumerate(text.splitlines(), 1):
            if len(line) > 5000:
                line = line[:5000]
            for name, rx in checks:
                if rx.search(line):
                    report["findings"].append({
                        "rule": name, "file": r, "line": lineno,
                        "text": line.strip()[:200],
                        "in_exec_surface": bool(is_exec_surface),
                    })
    return report


def print_report(rep: dict) -> None:
    print(f"# Audit: {rep['repo']}  ({rep['files_scanned']} text files scanned)")
    print("\n## Auto-executing surface (install/build/test hooks)")
    for e in rep["exec_surface"] or [{"file": "-", "why": "none"}]:
        print(f"- {e['file']}: {e['why']}")
    print("\n## npm lifecycle hooks")
    for h in rep["npm_hooks"] or [{"file": "-", "hook": "none", "cmd": ""}]:
        print(f"- {h['file']}: {h['hook']} = {h['cmd']}")
    print("\n## Committed binaries")
    for b in rep["binaries"] or [{"file": "none", "bytes": 0}]:
        print(f"- {b['file']} ({b['bytes']} bytes)")
    print("\n## Pattern findings")
    by_rule: dict[str, list] = {}
    for f in rep["findings"]:
        by_rule.setdefault(f["rule"], []).append(f)
    if not by_rule:
        print("- none")
    for rule, hits in sorted(by_rule.items()):
        print(f"\n### {rule} ({len(hits)})")
        for h in hits[:25]:
            tag = " [EXEC-SURFACE]" if h["in_exec_surface"] else ""
            print(f"- {h['file']}:{h['line']}{tag}: `{h['text']}`")
        if len(hits) > 25:
            print(f"- ... {len(hits) - 25} more")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rep = audit(Path(sys.argv[1]).resolve())
    if "--json" in sys.argv:
        print(json.dumps(rep, indent=2))
    else:
        print_report(rep)
