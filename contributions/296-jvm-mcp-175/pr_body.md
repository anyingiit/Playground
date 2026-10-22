## Summary

`find_slow_queries` always returned the top 20 statements from `pg_stat_statements`. This adds the limit proposed in #175 to the core reader, the MCP tool and the CLI.

## Changes

- `PostgresSchemaReader`: new `findSlowQueries(int limit)`, clamped with `Math.clamp(limit, 1, 100)`. `findSlowQueries()` keeps its behaviour and delegates with the default of 20. The query now binds the limit as a `PreparedStatement` parameter (`LIMIT ?`) instead of a literal.
- `find_slow_queries` tool: optional `limit` integer in the input schema (`minimum` 1, `maximum` 100, `default` 20), read with `ToolArgs.getIntArg`, which clamps out-of-range values the same way.
- CLI: `jvm-mcp pg --action slow-queries --limit <n>` (default 20).
- README: the tool table lists `limit`, with a short CLI example after the missing-index one.

## Motivation & Architecture Context

The constants `DEFAULT_SLOW_QUERY_LIMIT` and `MAX_SLOW_QUERY_LIMIT` sit next to `DEFAULT_MIN_TABLE_SIZE_BYTES`, and the overload follows `findMissingIndexes(schema)` / `findMissingIndexes(schema, minTableSizeBytes)`. Out-of-range values are clamped rather than rejected, as the issue suggests and as `get_heap_histogram`'s `limit` already does.

## Testing & Verification

- [x] Added / updated unit tests under `core/src/test/java` or `mcp-server/src/test/java`
  - `PostgresSchemaReaderValidationTest`: the clamp (5, 20, 100, 101 → 100, 0 → 1, -3 → 1).
  - `PostgresToolHandlerTest`: the default call uses 20, `limit` values are passed through or clamped, and the schema describes `limit`.
  - `PgCommandTest`: the default call uses 20, and `--limit 5` reaches the reader.
- [x] Ran `./mvnw clean verify` locally (all compilation, JaCoCo, and test gates pass)
  - Ran the equivalent `mvn verify` with Maven 3.9 and JDK 21: core 371 tests, mcp-server 285 tests, 0 failures, JaCoCo checks met.
- [x] Verified zero new heavy runtime dependencies introduced in `core` module
- [ ] Tested against a live JVM process (PID verification) or hermetic in-memory doubles (H2 / MockWebServer)
  - The Testcontainers-based `PostgresSchemaReaderIT` was skipped, since I had no Docker, so the `LIMIT ?` query hasn't run against a real PostgreSQL here.

## Related Issues

Fixes #175

I prepared this with help from an AI coding assistant (Claude Code) and reviewed the change myself.
