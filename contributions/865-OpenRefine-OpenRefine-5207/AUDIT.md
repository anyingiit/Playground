# Malicious-code audit — OpenRefine/OpenRefine @ c8d04c3c7f03f3fe321954134c468c18ae21d13e

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/openrefine` (1535 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none found | — |
| `main/webapp/package.json` postinstall = `node copy-dependencies.js` | Read `copy-dependencies.js`: reads `dependencies.json` and copies listed files from `node_modules/` into `modules/core/3rdparty/`. No network, no exec. | benign |
| Committed binary `server/lib-local/native/windows/jdatapath.dll` | Long-standing Windows native helper used by the launcher to find the user data path; Windows-only, never loaded on Linux. | benign (not executed here) |
| `powershell-download` pattern in `extract-operations-dialog.js:103,108` | Browser-side `downloadFile()` helper that creates a `data:` link to save history JSON (StackOverflow snippet, attributed). False positive. | benign |

Additional manual review of things that run during build/test:
- Root `pom.xml`: standard plugins (compiler, resources, surefire, jacoco, formatter, impsort, source/javadoc, gpg/nexus only for releases); `exec-maven-plugin` is configured with `<skip>true</skip>`.
- `main/pom.xml`: build-helper, surefire, dependency copy, jar, clean, git-commit-id, jacoco — nothing that downloads/executes arbitrary code.
- Cypress: `cypress.config.js`, `cypress/plugins/index.js` (no-op), `cypress/support/*.js` (test commands calling the local OpenRefine HTTP API only).
- `refine` shell script: wraps mvn/npm/yarn/cypress; nothing unusual.

Verdict: **no malicious code found**; safe to build and test.
