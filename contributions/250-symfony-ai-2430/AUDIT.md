# Malicious-code audit — symfony/ai @ 9209a92553f9230f0b51045d2f2a6fcd490dd359

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/symfony-ai` (1036 text files scanned), plus manual review of everything that runs during `composer install` / `phpunit` / `phpstan` / `php-cs-fixer`.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported | n/a |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | n/a |
| `.upsun/config.yaml:39` `curl -fs https://get.symfony.com/cloud/configurator \| bash` | Upsun (Platform.sh) deploy build hook for the ai.symfony.com website; official Symfony Cloud configurator. Never runs locally. | benign, not executed |
| `.github/workflows/tests.yaml:73` `curl -fsSL .../asg017/sqlite-vec/releases/download/v0.1.9/install.sh \| sh` | CI-only step installing the sqlite-vec extension from the upstream project's pinned release (PHP 8.5 matrix only). Not run locally. | benign, not executed |
| root `composer.json` | require-dev only (deptrac, php-cs-fixer shim, symfony components); no `scripts`, no custom repositories | benign |
| `src/platform/composer.json` | no `scripts` section, no custom repositories; Composer plugins are disabled in this non-interactive session anyway | benign |
| `src/platform/phpunit.xml.dist` | bootstrap = `vendor/autoload.php` only | benign |
| `.php-cs-fixer.dist.php` | pure rule configuration (header comment, @Symfony rules, finder) | benign |
| `src/platform/phpstan.dist.neon` | static analysis config only | benign |

Conclusion: nothing malicious found; safe to run `composer install`, `phpunit`, `phpstan`, `php-cs-fixer`.
