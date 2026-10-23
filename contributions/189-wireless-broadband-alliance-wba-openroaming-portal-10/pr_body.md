Before: `Dockerfile`, `DockerfileDev` and `DockerfileTests` build on `php:8.4-fpm-alpine3.21` / `php:8.4-alpine3.21`. The official PHP images stopped updating the Alpine 3.21 variants in November 2025 (last push 2025-11-22), so a rebuild with `--no-cache` still produces **PHP 8.4.15**. That is affected by PHP2Shell (CVE-2026-109618 / CVE-2026-109619), which is fixed in 8.4.27. The published `ghcr.io/wireless-broadband-alliance/wba-openroaming-portal:1.14.1` image reports PHP 8.4.15 as well. This is the case asked about in #10.

After: the three Dockerfiles use the `alpine3.23` variants, which are still maintained and currently ship **PHP 8.4.27**.

How: `alpine3.21` → `alpine3.23` in the five `FROM` lines; nothing else changes. I tried `alpine3.24` first, but its gpgme 2.x no longer has the trust-list API that the pinned `gnupg-1.5.0` PECL extension uses, so the extension fails to compile there. Alpine 3.23 has gpgme 1.24 and builds unchanged.

**Verification** (local Docker, arm64):
- `Dockerfile`, `DockerfileDev` and `DockerfileTests` all build; each image reports PHP 8.4.27.
- `php -v`: published 1.14.1 image **8.4.15**, patched image **8.4.27**. `php -m` lists the same extensions in both (gnupg, memcached, ldap, intl, soap, …).
- I ran both images side by side with the repo's compose setup (MySQL 8.0 + memcached, `.env` from `.env.sample`): `doctrine:migrations:migrate` and `doctrine:fixtures:load` succeed, `/` returns 200, `/login` redirects, and the dashboard login with the fixture super-admin works on both, ending at the same 2FA / installation-wizard redirects. The published image ran under amd64 emulation.

I did not add a CHANGELOG entry because entries there are written per release; happy to add one if you'd like.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to help projects affected by the PHP2Shell CVEs. This change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

🤖 Generated with [Claude Code](https://claude.com/claude-code)
