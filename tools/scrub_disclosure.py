#!/usr/bin/env python3
"""Find and remove private project disclosure from PR text.

Some PR bodies and comments were posted with a block the cloud harness
adds by default: a `claude-projects-attribution` HTML comment, a
"_Requested by **name** · [project thread](https://claude.ai/code/...)_"
line, and private claude.ai session/project links. The owner does not want
any of that upstream.

  scrub_disclosure.py check FILE...      exit 1 if any file has disclosure
  scrub_disclosure.py fix FILE...        rewrite files in place
  scrub_disclosure.py upstream [--apply] [--login anyingiit] [--urls FILE]
      Walk every PR/issue the login authored or commented on (GitHub search,
      plus any github.com issue/PR URLs listed in FILE), clean PR/issue
      bodies, issue comments, review comments and review bodies written by
      the login, and list PR commits whose messages carry Claude-Session or
      claude.ai links (commits are only reported, never rewritten).
      Without --apply it is a dry run. Writes scrub_report.json/.md to cwd.
"""
import json
import os
import re
import subprocess
import sys

# A claude.ai URL that carries an identifier (session, project, artifact, chat...).
# The bare product page https://claude.ai/code is public and left alone.
PRIVATE_URL = r"https?://claude\.ai/(?:code/)?(?:session_|project/|projects/|artifact/|artifacts/|chat/|share/)[^\s)>\]]*"
LINE_PATTERNS = [
    re.compile(r"claude-projects-attribution"),
    re.compile(r"^\s*_?\s*Requested by \*\*"),
    re.compile(r"^\s*(?:Claude-Session|Co-Authored-By:\s*Claude)\b", re.I),
    re.compile(r"^\s*<?" + PRIVATE_URL + r">?\s*$"),
]
MD_LINK = re.compile(r"\[([^\]]*)\]\(" + PRIVATE_URL + r"\)")
BARE = re.compile(r"<?" + PRIVATE_URL + r">?")
# Used by submit_pr.sh: refuse anything that would leak again.
GUARD = re.compile(r"claude-projects-attribution|Requested by \*\*|Requested by winshyon|claude\.ai/|Claude-Session", re.I)


def scrub(text):
    if not text:
        return text
    lines = [l for l in text.split("\n") if not any(p.search(l) for p in LINE_PATTERNS)]
    out = "\n".join(lines)
    out = MD_LINK.sub(r"\1", out)
    out = BARE.sub("", out)
    out = re.sub(r"[ \t]+\n", "\n", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    out = out.strip("\n")
    # a trailing '---' rule left with nothing under it
    out = re.sub(r"\n+---\s*$", "", out)
    if text.endswith("\n"):
        out += "\n"
    return out


def has_disclosure(text):
    return bool(text) and scrub(text) != text


# ---------------------------------------------------------------- upstream

def gh(*args, data=None):
    env = {k: v for k, v in os.environ.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN")}
    p = subprocess.run(["gh", *args], input=json.dumps(data) if data is not None else None,
                       capture_output=True, text=True, env=env)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout).strip()[:300])
    return p.stdout


def api_list(path):
    out = gh("api", "--paginate", "--slurp", path)
    pages = json.loads(out)
    items = []
    for page in pages:
        items.extend(page["items"] if isinstance(page, dict) and "items" in page else page)
    return items


def search(q):
    return api_list(f"search/issues?per_page=100&q={q}")


def item_key(url):
    m = re.match(r"https://(?:api\.)?github\.com/(?:repos/)?([^/]+/[^/]+)/(?:pull|pulls|issues)/(\d+)", url)
    return (m.group(1), int(m.group(2))) if m else None


def upstream(apply, login, urls_file):
    targets = {}
    for q in (f"author:{login}+is:pr", f"author:{login}+is:issue", f"commenter:{login}"):
        for it in search(q):
            k = item_key(it["html_url"])
            targets.setdefault(k, {"is_pr": "pull_request" in it})
    if urls_file:
        for u in re.findall(r"https://github\.com/[\w.-]+/[\w.-]+/(?:pull|issues)/\d+", open(urls_file).read()):
            k = item_key(u)
            targets.setdefault(k, {"is_pr": "/pull/" in u})
    print(f"{len(targets)} issues/PRs to inspect", file=sys.stderr)

    report = {"edited": [], "would_edit": [], "failed": [], "commits": [], "inspect_failed": []}

    def fix(kind, url, method, path, field, old):
        new = scrub(old)
        if new == old:
            return
        rec = {"kind": kind, "url": url}
        if not apply:
            report["would_edit"].append(rec)
            return
        try:
            gh("api", "-X", method, path, "--input", "-", data={field: new})
            report["edited"].append(rec)
        except Exception as e:
            rec["error"] = str(e)
            report["failed"].append(rec)

    for i, ((repo, n), meta) in enumerate(sorted(targets.items())):
        if i % 20 == 0:
            print(f"  {i}/{len(targets)} {repo}#{n}", file=sys.stderr)
        try:
            issue = json.loads(gh("api", f"repos/{repo}/issues/{n}"))
            is_pr = "pull_request" in issue
            if issue["user"]["login"].lower() == login.lower():
                fix("pr-body" if is_pr else "issue-body", issue["html_url"], "PATCH",
                    f"repos/{repo}/issues/{n}", "body", issue.get("body") or "")
            for c in api_list(f"repos/{repo}/issues/{n}/comments?per_page=100"):
                if c["user"]["login"].lower() == login.lower():
                    fix("comment", c["html_url"], "PATCH", f"repos/{repo}/issues/comments/{c['id']}",
                        "body", c.get("body") or "")
            if not is_pr:
                continue
            for c in api_list(f"repos/{repo}/pulls/{n}/comments?per_page=100"):
                if c["user"]["login"].lower() == login.lower():
                    fix("review-comment", c["html_url"], "PATCH", f"repos/{repo}/pulls/comments/{c['id']}",
                        "body", c.get("body") or "")
            for r in api_list(f"repos/{repo}/pulls/{n}/reviews?per_page=100"):
                if r["user"] and r["user"]["login"].lower() == login.lower() and r.get("body"):
                    fix("review", r["html_url"], "PUT", f"repos/{repo}/pulls/{n}/reviews/{r['id']}",
                        "body", r["body"])
            if issue["user"]["login"].lower() == login.lower():
                for c in api_list(f"repos/{repo}/pulls/{n}/commits?per_page=100"):
                    msg = c["commit"]["message"]
                    if GUARD.search(msg) or re.search(r"Co-Authored-By:\s*Claude", msg, re.I):
                        report["commits"].append({
                            "pr": issue["html_url"], "state": issue["state"],
                            "merged": bool(issue.get("pull_request", {}).get("merged_at")),
                            "sha": c["sha"][:12],
                            "lines": [l for l in msg.split("\n")
                                      if GUARD.search(l) or re.search(r"Co-Authored-By:\s*Claude", l, re.I)],
                        })
        except Exception as e:
            report["inspect_failed"].append({"item": f"{repo}#{n}", "error": str(e)})

    json.dump(report, open("scrub_report.json", "w"), indent=1, ensure_ascii=False)
    with open("scrub_report.md", "w") as f:
        f.write(f"# Disclosure scrub ({'applied' if apply else 'dry run'})\n\n")
        f.write(f"inspected {len(targets)} issues/PRs\n\n")
        for key in ("edited", "would_edit", "failed", "inspect_failed"):
            rows = report[key]
            f.write(f"## {key} ({len(rows)})\n\n")
            for r in rows:
                f.write("- " + " ".join(str(v) for v in r.values()) + "\n")
            f.write("\n")
        f.write(f"## commits with Claude-Session / claude.ai / Co-Authored-By Claude ({len(report['commits'])})\n\n")
        for c in report["commits"]:
            f.write(f"- {c['pr']} ({'merged' if c['merged'] else c['state']}) {c['sha']}: {' | '.join(c['lines'])}\n")
    print(json.dumps({k: len(v) for k, v in report.items()}), file=sys.stderr)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, rest = argv[0], argv[1:]
    if cmd == "check":
        bad = [f for f in rest if GUARD.search(open(f).read())]
        for f in bad:
            print(f"disclosure found: {f}", file=sys.stderr)
        sys.exit(1 if bad else 0)
    if cmd == "fix":
        for f in rest:
            s = open(f).read()
            t = scrub(s)
            if t != s:
                open(f, "w").write(t)
                print(f"scrubbed {f}")
        return
    if cmd == "upstream":
        login, urls = "anyingiit", None
        if "--login" in rest:
            login = rest[rest.index("--login") + 1]
        if "--urls" in rest:
            urls = rest[rest.index("--urls") + 1]
        upstream("--apply" in rest, login, urls)
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
