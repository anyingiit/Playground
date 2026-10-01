# AUDIT — jgrossi/elephpant.me (shallow clone @ 51b4582)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/elephpant.me` (43 text files scanned) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `.tugboat/config.yml:8` `curl -sL https://deb.nodesource.com/setup_12.x \| bash -` | Tugboat preview-environment init (stale PHP 7.3 config), official NodeSource installer; never run by tests/composer | benign, not executed here |
| npm lifecycle hooks | none in package.json | n/a |
| composer.json scripts | `post-autoload-dump` → Laravel `package:discover` (standard); `post-root-package-install` / `post-create-project-cmd` standard skeleton; `docs` → scribe | benign |
| Composer plugins (lock) | `pestphp/pest-plugin` only; composer plugins also disabled in this non-interactive session | benign |
| `.cursor/mcp.json`, `boost.json` | Laravel Boost MCP config (`php artisan boost:mcp`), editor-only | benign, not executed |
| `tests/Pest.php`, `phpunit.xml`, `Makefile` | standard Pest/RefreshDatabase bootstrap, sqlite `:memory:` env; Makefile only wraps pest/composer/artisan | benign |
| CI `.github/workflows/ci.yml` | pint / phpstan / rector / pest / scribe+redocly / JSON schema | benign |
| Committed binaries | none (0 bytes) | n/a |

**Verdict: no malicious code found; safe to install deps and run tests.**
