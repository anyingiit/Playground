# Malicious-code audit: floci-io/floci @ bc2592e

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/floci` (5103 text files scanned). Every hit was reviewed by hand before anything was built or run.

| Hit | Reviewed | Verdict |
|---|---|---|
| pom.xml build plugins (quarkus-maven-plugin, maven-compiler, surefire, checkstyle 14.1.0, enforcer) | Read the whole `<build>` section. There is no exec/antrun plugin and no `<executable>`. Surefire only sets -Xmx6g and the JBoss log manager | benign, standard Quarkus build |
| `.mvn/wrapper/maven-wrapper.properties` / `mvnw` | Downloads Maven 3.9.16 from repo.maven.apache.org, pinned with sha256 | benign |
| `mvnw.cmd:135` powershell DownloadFile | This is the standard Maven wrapper Windows script that downloads the distribution URL above. It is not run on Linux | benign |
| `compatibility-tests/sdk-test-node/vitest.config.ts`, `compatibility-tests/sdk-test-python/conftest.py` | These belong to separate compat suites and are not part of the Maven build. They were not run here | benign, not executed |
| destructive `"; rm -rf / ;"` in EksPodNetworkRoutingTest | A string literal passed to `assertThrows(IllegalArgumentException...)`. It is an input-validation test and is never executed | benign |
| reverse-shell `/dev/tcp/127.0.0.1/4566` in docker/healthcheck.sh | This is the container health probe. It connects to localhost:4566 (the Floci port) and sends `GET /_floci/health` | benign |
| raw-ip-url 169.254.169.254 / 169.254.170.x (28) | IMDS/ECS credential endpoints used in emulator code and in tests, including SSRF-block tests. All targets are link-local and there is no external host | benign |
| long-base64-blob in a cognito SRP fixture | `aaaa...` placeholder SRP_A value | benign |
| secret-paths (~/.docker, ~/.aws, ~/.kube) | Javadoc comments and error messages that describe config resolution. Nothing reads or exfiltrates them | benign |
| Committed binaries / npm lifecycle hooks | none | n/a |

Verdict: nothing malicious was found. It is safe to run `./mvnw test -Dtest=...` and `./mvnw checkstyle:check`.

## Re-check at f1d718c (2026-10-01)

The repo moved from bc2592e to f1d718c, so I re-ran `audit_repo.py` (5156 files). The hit categories and files are the same as above: destructive string in the EKS test, SRP fixture, mvnw.cmd, healthcheck `/dev/tcp`, 28 link-local IMDS/ECS URLs, and secret-path comments. `pom.xml` still has no exec, antrun or `<executable>`. `tools/docs/*.py`, which `make docs-check` runs, has no subprocess, network or `os.system` calls. Verdict unchanged: benign. Also ran: `make docs-check` and `make partition-check` (local Python scripts).
