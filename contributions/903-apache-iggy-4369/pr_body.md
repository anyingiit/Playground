## Which issue does this PR address?

Closes #4369

## Rationale

The Rust SDK exposes `SegmentClient::delete_segments`, but the Java SDK had no way to send the `DeleteSegments` command, so Java users could not trim old segments of a partition.

## What changed?

The Java SDK had no `DeleteSegments` (code 503) command, although the transport already knew how to route it (`VsrOperation` maps 503 to `DELETE_SEGMENTS`).

`deleteSegments(StreamId, TopicId, Long partitionId, Long segmentsCount)` (plus a numeric-id overload) is added to the blocking and async `PartitionsClient`. The TCP clients send `CommandCode.Segment.DELETE` with stream id, topic id, then partition id and segments count as little-endian `u32`, matching `DeleteSegmentsRequest`; the HTTP client calls `DELETE /streams/{stream_id}/topics/{topic_id}/partitions/{partition_id}?segments_count=N`. `PartitionsClientBaseTest` gets a test that runs for both the TCP and HTTP clients.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Local Execution

- Passed: `./gradlew :iggy:spotlessCheck :iggy:checkstyleMain :iggy:checkstyleTest :iggy:test` in `foreign/java` against an `apache/iggy:edge` server (`USE_EXTERNAL_SERVER=1`) — BUILD SUCCESSFUL, 1355 tests, 0 failures, 0 errors, 4 skipped. The new `shouldDeleteSegmentsWithoutRemovingActiveSegment` passes for both `PartitionsTcpClientTest` and `PartitionsHttpClientTest`; without the main-code change the test does not compile (`cannot find symbol: deleteSegments`).
- Pre-commit hooks ran: `prek run --files <changed files>` — all applicable hooks passed (mixed line ending, license headers, trailing whitespace/newline, binary artifacts, typos).

## AI Usage

1. Claude Code.
2. It drafted the implementation and the test, following the existing `deletePartitions` pattern and the Rust `DeleteSegmentsRequest` wire format.
3. I ran the Java SDK's full test suite, spotless and checkstyle locally against a real server, plus `prek`, as listed above.
4. Yes.
