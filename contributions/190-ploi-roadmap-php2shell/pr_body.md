Before: `docker/Dockerfile` builds on `php:8.4-fpm-alpine3.21`. The official PHP images stopped updating the Alpine 3.21 variants in November 2025, so `docker-compose up -d --build` still produces **PHP 8.4.15**, even with `--no-cache`. That version is affected by PHP2Shell (CVE-2026-109618 / CVE-2026-109619, remote code execution in PHP-FPM), fixed in 8.4.27.

After: the image is built on `php:8.4-fpm-alpine3.24`, which is maintained and currently ships **PHP 8.4.27**. Future PHP patch releases will also arrive with a normal rebuild.

How: a one-line change of the `FROM` tag. The rest of the Dockerfile is unchanged.

**Verification** (local Docker, arm64), comparing the image built from `main` with the image built from this branch:
- Both images build. `php -v` gives **8.4.15** on `main` and **8.4.27** on this branch, and `php -m` lists the same extensions (gd, intl, zip, pdo_mysql, sockets, …).
- With the repo mounted as in `docker-compose.yml`, I ran `composer install`, `npm ci && npm run build`, and then `vendor/bin/pest` inside each image. Both give **1150 passed** (2603 assertions).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to help projects affected by the PHP2Shell CVEs. This change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

🤖 Generated with [Claude Code](https://claude.com/claude-code)
