# Malicious-code audit — modelcontextprotocol/php-sdk @ 3175614 (main)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/php-sdk` (118 text files) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (composer scripts, npm lifecycle) | `composer.json` has no `scripts`; `allow-plugins`: `php-http/discovery: false`, `phpdocumentor/shim: true` (official phar shim, and composer plugins are disabled in this session anyway) | benign |
| Committed binaries | none | benign |
| `examples/server/oauth-keycloak/docker-compose.yml:18` "reverse-shell" pattern (`/dev/tcp/127.0.0.1/8180`) | Docker healthcheck that sends `GET /health/ready` to local Keycloak on localhost; standard bash-only healthcheck idiom; never run by us | benign |
| `Makefile` | Wrappers around composer/php-cs-fixer/phpstan/phpunit; conformance targets use docker + `npx @modelcontextprotocol/conformance` (not run here) | benign |
| `.php-cs-fixer.dist.php` | Plain rule config (@Symfony, header_comment) | benign |
| `phpunit.xml.dist` | No bootstrap file; only testsuite directories | benign |
| `.github/workflows/*.yaml` | Standard setup-php / composer-install / phpunit / conformance via npx; no secrets exfiltration | benign |
| `src/Client/Transport/StdioTransport.php` `proc_open` | Product feature: client launches the MCP server process given by the user | benign |
| `base64_decode` in `src/Server/Stateless/RequestStateCodec.php`, `src/Schema/Wire/McpHeader.php`, `src/Capability/Registry.php` | Decoding of cursors / state tokens / headers; no `eval` | benign |

Conclusion: nothing malicious found. Safe to run `composer install`, phpunit, php-cs-fixer, phpstan.
