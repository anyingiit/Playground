<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon**_

## Description

Before: the published image (`wardy784/erugo:latest`, v0.2.15) and any image rebuilt from `docker/alpine/Dockerfile` runs **PHP 8.3.14**. The Dockerfile pins `alpine:3.19`, which reached end of life on 2025-11-01, so its `php83` package is frozen and rebuilding does not pick up security fixes. That leaves Erugo exposed to PHP2Shell (CVE-2026-109618 / CVE-2026-109619, unauthenticated RCE in PHP-FPM, fixed upstream in 8.3.36).

After: the image is based on `alpine:3.24`, whose `php83` is **8.3.36-r0**. Rebuilding and republishing the image is enough to ship the fix.

How: `alpine:3.19` → `alpine:3.24` and the matching `v3.19/community` → `v3.24/community` repository line, in both `docker/alpine/Dockerfile` and `docker/dev/Dockerfile`. The package lists are unchanged; every package (including `php83-json`) still resolves on 3.24. Caddy moves from 2.7.6 to 2.11.4 as a side effect; the existing Caddyfile works unchanged in my tests.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to help projects affected by the PHP2Shell CVEs. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #293
Related: #292

## Checklist

- [x] Built `docker/alpine/Dockerfile` locally (`docker buildx build --load`), then compared it with the current `wardy784/erugo:latest` under the same conditions (fresh storage volume):
  - `php -v`: published image **8.3.14**, patched image **8.3.36**
  - `php-fpm83 -t` passes; `php -m` lists the same extensions (json, redis, memcached, mongodb, imap, ldap, intl, …)
  - `GET /api/health` → 200 on both
  - first-user setup (`POST /api/setup`) and `POST /api/auth/login` succeed on both
  - tus upload through Caddy (`POST`/`PATCH /files/`), `create-share-from-uploads`, and `GET /api/shares/{id}/download` return the identical file on both
- [x] `docker/dev/Dockerfile`: its full package list resolves on Alpine 3.24 (`apk add --simulate`)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, no changelog in the repo
- [ ] Documentation is updated (if applicable) — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)
