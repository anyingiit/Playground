# Audit — getsentry/sentry-laravel @ b6a56ed (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/sentry-laravel` — no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

Manual review:

| Item | Reviewed | Verdict |
|---|---|---|
| composer.json `scripts` | only `check`/`tests`/`cs-check`/`cs-fix`/`phpstan` (vendor/bin tools); no `post-install-cmd`/`post-update-cmd` hooks | benign |
| Makefile | composer install/update, git submodule, git config | benign (not used) |
| scripts/craft-pre-release.sh, scripts/versionbump.php | release-time version bump of Version.php | benign, not run |
| grep `exec/shell_exec/system/passthru/proc_open/base64_decode/eval` in src/ and test/ | no hits (only `new ...Filesystem(` false positives) | benign |
| .github/workflows | CI only, not executed locally | n/a |

Third-party dependencies are installed via `composer install` from Packagist (standard Laravel/Orchestra/phpunit stack).

Verdict: nothing malicious; safe to run `composer install`, phpunit, php-cs-fixer, phpstan.
