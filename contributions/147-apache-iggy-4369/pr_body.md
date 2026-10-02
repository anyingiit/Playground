## Which issue does this PR address?

Closes #4369

## Rationale

The Rust SDK has `SegmentClient::delete_segments`, the Java SDK had no equivalent.

## What changed?

Java users could not delete segments of a partition. This adds `CommandCode.Segment.DELETE` (503) and `deleteSegments(streamId, topicId, partitionId, segmentsCount)` to both the blocking and async `PartitionsClient`, with `Long`-id convenience overloads like the existing methods.

TCP follows the `deletePartitions` pattern: stream and topic identifiers, then `partition_id` and `segments_count` as u32 LE (matching `DeleteSegmentsRequest` in `binary_protocol`). HTTP sends `DELETE /streams/{stream_id}/topics/{topic_id}/partitions/{partition_id}?segments_count=N`. A `shouldDeleteSegments` case in `PartitionsClientBaseTest` runs for both TCP and HTTP.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Local Execution

- Passed. Run against `apache/iggy:edge` with `USE_EXTERNAL_SERVER=1`, as in CI:
  - `./gradlew check -x test` (foreign/java): BUILD SUCCESSFUL (spotless + checkstyle)
  - `./gradlew :iggy:test --tests '*Partitions*'`: 4/4 pass (`shouldDeleteSegments` for TCP and HTTP). Before the change the test does not compile (no `deleteSegments`).
  - `./gradlew :iggy:test`: 1355 tests, 0 failures, 4 skipped; no `LEAK:` in test results
  - Sanity check: pointing the test at a nonexistent partition (99) makes both TCP and HTTP throw `IggyResourceNotFoundException`, so the request really reaches the server.
- Pre-commit hooks: <!-- SUBMITTER: run `prek run` and update this line -->

## AI Usage

1. Claude Code.
2. Implementation and test were drafted with it, then reviewed by me.
3. Verified with the Gradle lint and test runs above against a live server.
4. Yes.

## Checklist

- [x] Tests pass locally (see Local Execution)
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the Java SDK has no changelog file
- [ ] Documentation is updated (if applicable): n/a, no Java SDK doc lists the partitions API
