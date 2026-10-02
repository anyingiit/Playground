# Malicious-code audit — pmd/pmd @ 251ef73 (shallow clone, main)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pmd` (3546 text files), plus manual review of everything that runs during `mvn ... -pl pmd-groovy -am test`.

| Hit / area | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm lifecycle hooks | none reported; `package.json` is only for docs/danger tooling, not used by Maven build | benign |
| `mvnw.cmd:135` powershell `DownloadFile` | standard Apache Maven Wrapper 3.3.4 script; `distributionUrl` in `.mvn/wrapper/maven-wrapper.properties` is `repo.maven.apache.org/.../apache-maven-3.9.16-bin.zip`. Not used here (system `mvn` used instead) | benign |
| Committed binaries (`pmd-java/src/test/resources/**.class`, `custom_java_lang.jar`, `pmd-dist/.../sample-source-java.jar`) | tiny (<2 KB) fixtures for symbol-resolution / dist tests, only read as data by tests in modules that are not built for this change | benign, not executed |
| Root `pom.xml` `maven-antrun-plugin` + `antlr4-wrapper.xml` / `javacc-wrapper.xml` | Ant scripts that post-process generated ANTLR/JavaCC parser sources (regex replace, touch stamp files); no `<exec>`, no network access | benign |
| Root `pom.xml` `exec-maven-plugin` | only declared in pluginManagement (version pin), not bound in pmd-core/pmd-test/pmd-lang-test/pmd-groovy | benign |
| Root `pom.xml` extra repository | `central.sonatype.com/repository/maven-snapshots/` (official Central Portal snapshots) | benign |
| `pmd-groovy` module | 5 Java sources + 1 test + test data; depends on pmd-core, org.apache.groovy:groovy, junit | benign |

Verdict: **no malicious code found**; safe to build and run the pmd-core/pmd-test/pmd-lang-test/pmd-groovy tests.
