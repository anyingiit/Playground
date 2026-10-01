# AUDIT — github-linguist/linguist (shallow clone @ 5fbdfcb, 2026-09-29)

`python3 tools/audit_repo.py /home/user/work/linguist` — 1217 text files scanned. No npm lifecycle hooks, no committed binaries flagged by the auto-exec section.

| Hit | Reviewed | Verdict |
|---|---|---|
| hex-escaped-blob ×26 (`samples/Go/embedded.go`) | Gzip blobs in a go-bindata sample used as classifier training data; never executed | benign |
| pipe-to-shell `tools/grammars/Dockerfile:5` (`curl nodesource setup_22.x \| bash`) | Standard Node install in the grammar-compiler Docker image (used by `script/add-grammar` / grammar checks) | benign (upstream official installer) |
| powershell-download ×6 | Sample/fixture files (Cakefile, mvnw.cmd, ObjC header, base64 PNG in XML sample) — text data only | benign |
| secret-paths ×6 | `.npmrc` language entry / grammar scope; `~/.ssh/id_rsa` strings inside SSH Config / INI samples | benign |
| Rakefile `fetch_ace_modes` | Reads `api.github.com/repos/ajaxorg/ace/...` read-only into a test fixture; rescues network errors | benign |
| ext/linguist (C extension built by rake-compiler, flex tokenizer) | Normal native extension build | benign |

Also cloned `uiua-lang/uiua-vscode` (grammar source, MIT): only `syntaxes/uiua.tmLanguage.json` is consumed (JSON data); its JS/TS extension code is not executed.

Verdict: nothing malicious; OK to build/test.
