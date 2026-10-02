# Audit — getsentry/sentry-php @ b06d0bd1 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/sentry-php` (no auto-exec hooks, no npm hooks, no committed binaries, no pattern findings) + manual review of composer scripts, PHPUnit bootstrap, workflows and every `eval`/`proc_open`/`base64`/`curl|sh` hit.

| Hit | Reviewed | Verdict |
|---|---|---|
| composer.json `scripts` (check, tests, cs-check, cs-fix, phpstan, mago) | Only invoke vendor/bin tools (phpunit, php-cs-fixer, phpstan, mago); no install hooks (`post-install-cmd` etc. absent); `allow-plugins` sets php-http/discovery and tbachert/spi to false | benign |
| phpunit.xml.dist `bootstrap="tests/bootstrap.php"` | Requires vendor/autoload.php and registers ClockMock for a few classes | benign |
| tests/TestUtil/ClockMock.php:156 `eval(...)` | Symfony-style ClockMock: defines namespaced `time()/microtime()/sleep()/usleep()` shims that call a static mock; no external input | benign |
| tests/HttpClient/TestServer.php:51 `proc_open` | Starts `php -S localhost:<port> tests/testserver/index.php` for HTTP client tests | benign (local only) |
| tests/HttpClient/TestAgent.php:64 `proc_open` | Starts `php tests/HttpClient/agent-server.php <port> <file>` local test agent | benign (local only) |
| tests/Integration/RuntimeContextWorkerModeIntegrationTestCase.php:104 `proc_open` | Starts FrankenPHP/RoadRunner worker server for optional integration tests (binaries not installed here, tests skip) | benign |
| src/FrameBuilder.php:63 `eval()'d code` | Comment about parsing eval frame file names | benign |
| scripts/bump-version.sh | Release-only version bump via perl/grep on src/Client.php; never run here | benign / not run |
| .github/workflows (ci, static-analysis, publish-release, validate-pr) | CI only; validate-pr posts an advisory comment if external PR >100 lines lacks an issue discussion with author+maintainer | benign / not run |

Verdict: nothing malicious; safe to `composer install` (plugins stay disabled) and run phpunit / php-cs-fixer / phpstan / mago.
