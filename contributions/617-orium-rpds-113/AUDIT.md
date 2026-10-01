# AUDIT — orium/rpds (shallow clone of main @ d7c1205)

`python3 tools/audit_repo.py /home/user/work/rpds`: 54 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs, hooks) | none found; no build.rs in crate | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |
| tools/check.sh, tools/utils.sh | read manually: only runs cargo build/test/doc/fmt/clippy | benign |

AI-policy grep (LLM / AI-generated / Copilot / ChatGPT / agent) across the repo: no hits. CONTRIBUTING.md has no AI rules.

Verdict: safe to build and test.
