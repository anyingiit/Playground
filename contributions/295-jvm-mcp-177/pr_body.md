## Summary

Adds the ArchUnit rule from #177 to `CoreArchitectureTest`, so no class in `core` can write to `System.out` or `System.err`. Four existing `System.err.println` calls in `core` broke the rule, so they now log through `System.Logger`, as `JvmAttachService` already does.

## Changes

- `CoreArchitectureTest`: new rule `coreMustNotWriteToStandardStreams`, using `GeneralCodingRules.NO_CLASSES_SHOULD_ACCESS_STANDARD_STREAMS` with a `because` about the stdio transport. That rule also catches `Throwable.printStackTrace()`.
- `ActuatorClient`: the insecure-TLS warning and the two batch-metrics failure messages are `WARNING` logs.
- `HikariMXBeanClient`: the "skipping unreadable pool" message is a `WARNING` log.

## Motivation & Architecture Context

`System.Logger` keeps `core` free of logging dependencies. With no logging configured, it goes to `java.util.logging`'s default console handler, which writes `WARNING` to stderr, so these messages still show up, now with JUL's timestamp and source line instead of the `[jvm-mcp]` prefix. Applications embedding `core` can route or silence them through their own logging setup.

## Testing & Verification

- [x] Added / updated unit tests under `core/src/test/java` or `mcp-server/src/test/java`
  - With only the new rule, `CoreArchitectureTest` fails and lists the four `System.err` accesses (`HikariMXBeanClient.java:53`, `ActuatorClient.java:111`, `:329`, `:342`). With the logging change, it passes.
- [x] Ran `./mvnw clean verify` locally (all compilation, JaCoCo, and test gates pass)
  - `mvn verify` with Maven 3.9 and JDK 21 (the same goals as the wrapper): core 366 tests, mcp-server 279 tests, 0 failures, JaCoCo checks met.
- [x] Verified zero new heavy runtime dependencies introduced in `core` module
- [ ] Tested against a live JVM process (PID verification) or hermetic in-memory doubles (H2 / MockWebServer)

## Related Issues

Fixes #177

I prepared this with help from an AI coding assistant (Claude Code) and reviewed the change myself.
