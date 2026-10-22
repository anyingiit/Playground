# AUDIT — Forceu/barcodebuddy-docker @ 08f2ba8 and Forceu/barcodebuddy @ 98a8649 (2026-10-22)

`python3 tools/audit_repo.py` on both clones: no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

| Surface | Reviewed | Verdict |
|---|---|---|
| Dockerfile / Dockerfile.dev | installs Alpine packages, downloads the BarcodeBuddy release tarball (or clones the repo) from github.com/Forceu | benign |
| supervisor/ (Go) | starts redis, php-fpm, nginx, websocket server, cron; sed edits of config files | benign |
| .github/workflows | manual multi-arch build + push to Docker Hub, not run | n/a |
| barcodebuddy app | composer.json has no scripts; vendored PHP code only executed inside containers | benign |

All code ran only inside Docker containers (image builds + smoke tests). Verdict: no malicious code found.
