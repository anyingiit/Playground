#!/usr/bin/env python3
"""Summarize the state of every submitted upstream PR listed in contributions/submissions.json.

Usage: python3 tools/pr_status.py [--since ISO_DATE]

Needs a `gh` login with repo scope; the Codespaces GITHUB_TOKEN is dropped because it is repo-restricted.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = {k: v for k, v in os.environ.items() if k not in ("GITHUB_TOKEN", "GH_TOKEN")}
FIELDS = "state,isDraft,reviewDecision,mergeable,statusCheckRollup,comments,reviews,updatedAt"


def gh_pr(url):
    out = subprocess.run(["gh", "pr", "view", url, "--json", FIELDS],
                         capture_output=True, text=True, env=ENV)
    return json.loads(out.stdout) if out.returncode == 0 else {"error": out.stderr.strip()}


def checks(rollup):
    tally = {}
    for c in rollup or []:
        s = c.get("conclusion") or c.get("state") or c.get("status") or "?"
        tally[s] = tally.get(s, 0) + 1
    return " ".join(f"{k}:{v}" for k, v in sorted(tally.items())) or "-"


def main():
    since = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else ""
    subs = json.loads((ROOT / "contributions" / "submissions.json").read_text())
    for nn, url in subs.items():
        if not url:
            print(f"{nn}  (not submitted)")
            continue
        d = gh_pr(url)
        if "error" in d:
            print(f"{nn}  {url}  ERROR {d['error']}")
            continue
        others = [c for c in d["comments"] + d["reviews"]
                  if c["author"]["login"] != "anyingiit" and (c.get("createdAt") or c.get("submittedAt") or "") > since]
        state = d["state"] + ("/draft" if d["isDraft"] else "")
        print(f"{nn}  {state:12} review={d['reviewDecision'] or '-':17} checks[{checks(d['statusCheckRollup'])}]"
              f"  new_feedback={len(others)}  {url}")


if __name__ == "__main__":
    main()
