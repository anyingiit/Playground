# AUDIT — github-linguist/linguist (shallow clone, HEAD of default branch) + uiua-lang/uiua-vscode (grammar)

Command: `python3 /home/user/Playground/tools/audit_repo.py <dir>`

## linguist

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-exec hooks / npm lifecycle | none found | n/a |
| Committed binaries `test/fixtures/Binary/{git.exe,foo.bin,foo bar.jar}` | test fixtures for binary detection, never executed (28 B dummies + small exe fixture) | benign |
| hex-escaped-blob x26 `samples/Go/embedded.go` | go-bindata gzip blobs in a language *sample* file; only read as text by the classifier | benign |
| pipe-to-shell `tools/grammars/Dockerfile:5` (nodesource setup) | upstream grammar-compiler Docker image build; not run here (no Docker daemon) | benign / not executed |
| powershell-download x6 (Cakefile, mvnw.cmd, ObjC header, base64 PNG in water.tsx) | all inside `samples/` / `test/fixtures/` data files, never executed | benign |
| secret-paths x6 (`.npmrc` scope names, `id_rsa` in sample configs) | language names / sample config text, no real secrets | benign |
| What I run | `bundle install` (gemspec deps: rugged, charlock_holmes, licensed, ...from rubygems), `rake` (compiles `ext/linguist` flex tokenizer C ext — reviewed `extconf.rb`, plain `create_makefile`), `rake samples`, minitest suite; `go run` of `tools/grammars/cmd/grammar-compiler` (reads grammars, writes `grammars/`), `script/update-ids` (YAML rewrite) | benign |

## uiua-lang/uiua-vscode (to be added as grammar submodule)

No hits (15 text files). Only its `syntaxes/uiua.tmLanguage.json` + `license` (MIT) are consumed by linguist; no code from it is executed.

Verdict: nothing malicious; safe to proceed.
