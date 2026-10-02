# Malicious-code audit — vimeo/psalm @ 79465b8 (master, 2026-09-23)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/psalm`
Result: auto-exec surface none, npm hooks none, committed binaries none, pattern findings none
(note: the script scanned only 51 non-PHP text files, so the PHP sources were reviewed manually below).

## Manual review (things that run during `composer install` / `phpunit`)

| Hit | Reviewed | Verdict |
|---|---|---|
| `composer.json` scripts | Only `cs`, `lint`, `phpunit`, `psalm`, `gen_*`, `build` helper scripts; **no** `post-install-cmd` / `post-update-cmd` / `pre-*` hooks | benign |
| `composer.json` allow-plugins: bamarni/composer-bin-plugin, phpcodesniffer-composer-installer | Well-known dev plugins; no `extra.bamarni-bin` auto-forward config, so vendor-bin/{bcc,box} are not installed automatically | benign |
| `phpunit.xml.dist` bootstrap `tests/autoload.php` | Requires `vendor/autoload.php`, enables `dg/bypass-finals` (test-only final-class bypass) | benign |
| `exec`/`shell_exec`/`popen`/`eval` in `tests/*.php` | All inside PHP code *strings* that Psalm statically analyses (ForbiddenCodeTest, TaintTest, UnusedVariableTest, ...); never executed | benign |
| `src/Psalm/Internal/ExecutionEnvironment/SystemCommandExecutor.php` `exec()` | Runs git commands for CI/build-info detection (Shepherd) | benign, legitimate feature |
| `src/Psalm/Plugin/Shepherd.php` `curl_exec` | Uploads results to shepherd.dev only when the Shepherd plugin/`--shepherd` is enabled; not used in tests run here | benign |
| `src/Psalm/Internal/LanguageServer/LanguageServer.php` `stream_socket_client` | LSP TCP mode, only when explicitly configured | benign |
| `src/Psalm/Internal/Cli/Review.php` `passthru` | `psalm-review` CLI opening an editor | benign, not run |
| `bin/ci/*.php`, `bin/hack-conformance/*` (`passthru`/`exec` docker) | Maintainer CI/release tooling, not invoked by tests | benign, not run |
| Network URLs in src | getpsalm.org schema namespace, shepherd.dev endpoint (see above) | benign |

**Verdict: no malicious code found. Safe to `composer install` and run PHPUnit / psalm self-analysis.**
