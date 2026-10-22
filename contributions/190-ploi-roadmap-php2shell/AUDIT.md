# AUDIT — ploi/roadmap @ main (2026-10-22)

`python3 tools/audit_repo.py`: no auto-executing hooks, no npm lifecycle hooks, no committed binaries. 5 "powershell-download" pattern hits, all Welsh strings in lang/cy.json ("adnodd", "Defnyddiwr") — false positives.

| Surface | Reviewed | Verdict |
|---|---|---|
| docker/Dockerfile | official PHP image, apk packages, `npm install -g n`, composer | benign |
| composer.json scripts | standard Laravel post-autoload / key:generate / package:discover | benign |
| package.json scripts | vite dev/build only | benign |

All code (composer install, npm ci, vite build, pest) ran only inside Docker containers. Verdict: no malicious code found.
