# Audit — highlightjs/highlight.js @ fc3f0639 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/highlight.js` + manual review of npm lifecycle hooks, package-lock install scripts, and `child_process` use in tools/ and test/.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm lifecycle hooks | audit tool: none; package.json has no pre/post/install/prepare scripts; no .npmrc, no .husky | benign |
| package-lock.json `hasInstallScript` | only `node_modules/fsevents` (optional macOS dep, not installed on Linux) | benign |
| src/languages/powershell.js:63 "powershell-download" pattern (`iwr ...`) | keyword list string inside the PowerShell grammar, not executed | false positive |
| tools/build_browser.js `execSync("git rev-parse --short=10 HEAD")` | stamps git sha into browser build; we only run the node build | benign |
| tools/perf.js `execSync('npm run build' / mocha / checkAutoDetect)` | local perf helper, not run by build/test scripts | benign / not run |
| Committed binaries | none | ok |

Verdict: nothing malicious; safe to `npm ci`, `node tools/build.js -t node <langs>`, `npm run test-markup`, `npm run lint-languages`.
