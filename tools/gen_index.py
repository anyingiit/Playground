#!/usr/bin/env python3
"""Regenerate contributions/INDEX.md from each folder's README.md."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "contributions"
rows, counts = [], {"高星": 0, "新锐": 0, "自由": 0}
for d in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")):
    readme = d / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    m = re.search(r"https://github\.com/([^/\s)]+/[^/\s)]+)/issues/(\d+)", text)
    issue = f"[{m.group(1)}#{m.group(2)}](https://github.com/{m.group(1)}/issues/{m.group(2)})" if m else d.name
    head = "\n".join(text.splitlines()[:25])
    tier = "高星" if ("高活跃" in head or "高星" in head) else "新锐" if "新锐" in head else "自由"
    status_line = next((l for l in text.splitlines() if re.search(r"\bStatus\b|状态", l)), "")
    ready = "🚧" not in status_line and bool(list(d.glob("*.patch")))
    if ready:
        counts[tier] += 1
    rows.append(f"| {d.name.split('-')[0]} | {tier} | {issue} | {'✅' if ready else '🚧'} |")
total = sum(counts.values())
out = [
    "# Contributions index",
    "",
    "Target: **60 = 12 高活跃高Star + 12 新锐 + 36 自由**.",
    f"Ready: **{total}** (高星 {counts['高星']} · 新锐 {counts['新锐']} · 自由 {counts['自由']}).",
    "Each folder: `README.md` (analysis, verification, submit steps, PR text, **需要提交者注意**), `0001-*.patch`, `AUDIT.md`.",
    "Rules: [`docs/CONTRIBUTION_BRIEF.md`](../docs/CONTRIBUTION_BRIEF.md). Tools: [`tools/`](../tools/).",
    "",
    "| # | Tier | Issue | Status |",
    "|---|---|---|---|",
    *rows,
    "",
]
(root / "INDEX.md").write_text("\n".join(out), encoding="utf-8")
print(out[3])
