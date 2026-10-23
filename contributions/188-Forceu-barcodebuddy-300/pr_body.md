Before: `f0rc3/barcodebuddy:latest` is built `FROM alpine:3.15` and runs **PHP 8.0.25**. Alpine 3.15 and PHP 8.0 are both end of life, so rebuilding the image no longer picks up PHP security fixes. That leaves the image exposed to PHP2Shell (CVE-2026-109618 / CVE-2026-109619, remote code execution in PHP-FPM), reported in Forceu/barcodebuddy#300.

After: the image is built `FROM alpine:3.24` and runs **PHP 8.3.36**, which contains both fixes. Rebuilding and pushing the image with the existing release workflow is enough to ship it.

How:
- `Dockerfile` and `Dockerfile.dev`: `alpine:3.15` → `alpine:3.24`, `php8-*` → `php83-*` (`php8-redis` is now `php83-pecl-redis`), `/var/log/php8`, `/usr/bin/php8` and `/etc/php8/php-fpm.d/www.conf` → their `php83` paths. `libressl3.4-libssl` no longer exists on 3.24 and nothing in the image needs it (the supervisor is a static Go binary), so it is dropped.
- `root/etc/php8/` → `root/etc/php83/` so `bbuddy-local.ini` still lands in PHP's `conf.d`.
- Supervisor: `/usr/bin/php8` → `/usr/bin/php83` (websocket server, cron), `/usr/sbin/php-fpm8` → `/usr/sbin/php-fpm83`, and the timezone is written to `/etc/php83/php.ini`.

**Verification.** I built the image locally and ran it side by side with the current `f0rc3/barcodebuddy:latest` (BarcodeBuddy 1.9.0.1 in both), each connected to the same Grocy (linuxserver/grocy v4.7.1):

| Check | `latest` (published) | this PR |
|---|---|---|
| `php -v` / Alpine | 8.0.25 / 3.15.11 | **8.3.36** / 3.24.3 |
| Redis, PHP-FPM, nginx, websocket server running | ✅ | ✅ |
| Create user, log in, Grocy setup | ✅ | ✅ |
| `/api/system/info`, settings, API management, `screen.php` | 200 | 200 |
| Scan unknown barcode (name lookup) | ✅ | ✅ |
| Switch to purchase mode, scan known barcode → Grocy stock +1 | ✅ | ✅ |
| `cron.php` | exit 0 | exit 0 |
| `TZ` written to php.ini, `bbuddy-local.ini` limits applied | n/a (no TZ set) | ✅ |
| PHP / nginx error log | clean | clean |

`Dockerfile.dev` also builds and runs PHP 8.3.36. The full package list resolves on Alpine 3.24 for `linux/386`, `linux/arm/v6`, `linux/arm/v7` and `linux/arm64` (`apk add --simulate`), so the multi-arch release workflow should keep working; I have only run the amd64 image.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to help projects affected by the PHP2Shell CVEs. This change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

🤖 Generated with [Claude Code](https://claude.com/claude-code)
