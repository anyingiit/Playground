# Audit — infection/infection @ 8fc651d (shallow clone, 2509 tracked files)

`python3 tools/audit_repo.py /home/user/work/infection`: no auto-executing hooks, no npm lifecycle hooks, 0 committed binaries, no pattern findings.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| composer.json `scripts` | none defined | benign |
| composer `allow-plugins` | phpstan/extension-installer, infection/extension-installer (well-known, first-party/ecosystem) | benign |
| `setup_environment.sh` | only symlinks devTools/pre-push into .git/hooks; NOT run | benign (not executed) |
| phpunit.xml.dist bootstrap | `vendor/autoload.php` + StrictPHPUnit extension | benign |
| Makefile | standard targets (cs, phpstan, phpunit, box/php-scoper downloads for compile); only `cs`/`phpstan`/unit-test targets used | benign |

Verdict: nothing suspicious; safe to `composer install` (Composer run with plugins disabled except as noted) and run PHPUnit/PHP-CS-Fixer/PHPStan.

Later additions: `.tools/php-cs-fixer` phar downloaded from the official FriendsOfPHP GitHub release URL pinned in the Makefile (v3.92.5); `phpstan/phpstan` dist fetched via `git fetch` of the locked commit from github.com/phpstan/phpstan (API zipball blocked).
