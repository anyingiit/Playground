# Audit — phpmyadmin/phpmyadmin @ QA_5_2 8dfc3dbf (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/phpmyadmin` (run on the QA_5_2 checkout) + manual review of composer/npm scripts, PHPUnit bootstrap, `scripts/`, CI workflows, and a grep for `curl|wget|base64_decode(|eval(|shell_exec|exec(|passthru|system(` in scripts/test bootstrap/workflows/composer.json.

| Hit | Reviewed | Verdict |
|---|---|---|
| jest.config.js (JS test runner config) | Plain jest project config (jsdom, local setup file `test/jest/test-env.js`); JS tests are not needed for this PHP fix and will not be run | benign / not run |
| package.json `postinstall = yarn run build` | Runs sass/postcss/rtlcss/babel over the repo's own themes and js/src; no network or downloads. We will not run `yarn install` | benign / not run |
| composer.json `scripts` | phpcs / phpstan / psalm / phpunit wrappers and baseline update; no install hooks (`post-install-cmd` etc. absent). `allow-plugins` only for phpcodesniffer-installer, phpstan extension-installer, package-versions-deprecated (well-known) | benign |
| phpunit.xml.dist bootstrap `test/bootstrap-dist.php` | Defines ROOT_PATH/TEST_PATH, ini/error_reporting/timezone, requires `libraries/constants.php` and the composer autoloader | benign |
| `scripts/*` (release, po, mo, vendor-sync helpers) | Maintainer release tooling, not invoked by composer/phpunit | benign / not run |
| `.github/workflows/tests.yml:46` `php$V-curl` | apt package name in CI matrix | benign |
| Committed binaries | none found (no .so/.dll/.exe/.bin/.phar/.jar tracked) | n/a |

Verdict: nothing malicious; safe to run `composer install` (plugins limited to the listed well-known ones) and `vendor/bin/phpunit` / phpcs / phpstan / psalm on targeted files.
