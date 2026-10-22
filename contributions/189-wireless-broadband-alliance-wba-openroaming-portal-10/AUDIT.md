# AUDIT — wireless-broadband-alliance/wba-openroaming-portal @ 452944a (master) / develop (2026-10-22)

`python3 tools/audit_repo.py`: no auto-executing hooks, no npm lifecycle hooks, no committed binaries. 8 "secret-paths" pattern hits, all `apk add/del .gnupg-build-deps` lines in the Dockerfiles (false positives: virtual package name contains "gnupg").

| Surface | Reviewed | Verdict |
|---|---|---|
| Dockerfile / DockerfileDev / DockerfileTests | Alpine packages, mlocati extension installer, pecl gnupg, composer install; also downloads a PaloAlto SSL-inspection CA from tetrapi.pt with `--no-check-certificate` and trusts it (`|| true` if unreachable) | upstream's own corporate-proxy workaround, not malicious; noted in README |
| composer.json scripts | standard Symfony auto-scripts (cache:clear, assets:install, importmap) | benign |
| .github/workflows/docker-publish.yml | build + push to ghcr, cosign; not run | n/a |

All code ran only inside Docker containers. Verdict: no malicious code found.
