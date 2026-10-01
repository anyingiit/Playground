# AUDIT — infection/infection @ 8fc651d (shallow clone, master)

`python3 tools/audit_repo.py /home/user/work/infection`: no auto-exec hooks, no npm hooks, no committed binaries, no pattern findings.

Manual review (extra checks because the tool only scanned 271 of 2532 files):

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `composer.json` scripts | none defined; allow-plugins = phpstan/extension-installer, infection/extension-installer (well-known) | benign |
| `phpunit.xml.dist` bootstrap | `vendor/autoload.php` + `Webmozarts\StrictPHPUnit` extension | benign |
| `setup_environment.sh` | symlinks `devTools/pre-push` hook only (not run) | benign, not executed |
| `Makefile` `wget` of box / php-cs-fixer | downloads release phars from GitHub releases of the official tools | benign (only phar download; not needed — used vendor tools) |
| `resources/debug-runtime.php` `base64_decode` | decodes a JSON command passed as CLI arg for the "debug" test framework | benign |
| tests `base64_decode('abc', true)` | produce invalid UTF-8 for tests | benign |
| grep for `eval(base64`, `curl|sh`, `/dev/tcp`, `fsockopen` | no hits | — |

Verdict: nothing malicious found; OK to `composer install` and run PHPUnit / static analysis.
