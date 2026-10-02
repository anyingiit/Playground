# apache/iggy #4369: Java SDK: expose deleteSegments

| 项 | 值 |
|---|---|
| Issue | https://github.com/apache/iggy/issues/4369 |
| Tier | 新锐 |
| Labels | good first issue, java |
| Status | ✅ ready (patch + PR text 已就绪，等待提交者先认领 issue) |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论、无关联 PR；搜索 `deleteSegments` 无 open PR（只有 Go/JS/server 等其他语言的已合并 PR） |
| Base | `master` @ 985b0ac1fb4d0e2d0f92afae50c2e3014604c5ff |
| Patch | `0001-feat-java-add-deleteSegments-to-partitions-client.patch` |

## 需要提交者注意

1. **必须先认领 issue**：CONTRIBUTING.md 要求“Wait for the issue to be assigned to you”，AGENTS.md 写明 “The PR must link an issue the user is assigned to”。请先在 #4369 下评论认领，等维护者 assign 后再开 PR。
2. **AI 政策**：允许 AI 辅助，但提交者必须能解释每一行、自己回答 review 问题；维护者会关闭“像是在 reviewer 与模型之间传话”的 PR。PR 模板有 `## AI Usage` 小节，pr_body.md 已按实填写。请自行读懂 diff（共 ~100 行，见下文“改动”）。
3. **新人同一时间只开一个 PR**（CONTRIBUTING）。如果你在 iggy 已有 open PR，请先等它合并。
4. **prek**：AGENTS.md 要求开 PR 前跑 `prek run`（`cargo install prek && prek install`）。本环境没有跑 prek，只跑了它对 Java 调用的同一命令 `./gradlew check -x test`。请本地跑一次 prek，并把 pr_body.md 里 “Pre-commit hooks:” 那行改成实际结果（删掉 HTML 注释）。
5. 不需要 DCO / Signed-off-by（Apache 项目，无 DCO 检查）。commit 作者为 anyingiit <49945850+anyingiit@users.noreply.github.com>，消息中无 AI 名字。
6. AGENTS.md 要求避免 em dash 等“LLM 腔”，pr_body.md 已避开，修改时请注意。
7. 若维护者希望再加一个纯单元测试（不依赖服务器的 payload 编码测试，参考 `TopicsTcpClientPayloadTest`），可以按需补充。

## 问题理解

Rust SDK 有 `SegmentClient::delete_segments`，Java SDK 没有对应方法。issue 列出了步骤：CommandCode 新增 `Segment.DELETE(503)`；blocking/async `PartitionsClient` 加 `deleteSegments(StreamId, TopicId, Long partitionId, Long segmentsCount)`；TCP 按 `deletePartitions` 模式编码（partition_id、segments_count 为 u32 LE）；HTTP 用 `DELETE /streams/{s}/topics/{t}/partitions/{p}?segments_count=N`；在 `PartitionsClientBaseTest` 加测试。

## 合理性判断

- issue 由维护者按明确步骤写成，标 good first issue。
- 服务端已支持：`core/binary_protocol/src/requests/segments/delete_segments.rs`（stream_id, topic_id, partition_id u32 LE, segments_count u32 LE），HTTP handler `core/server/src/http/handlers.rs::delete_segments`（路径参数 partition_id，query 参数 segments_count）。Java 侧 `VsrOperation` 已经把 503 映射为 `DELETE_SEGMENTS`，只差客户端 API。
- Go/JS SDK 已有同功能（#3191、#1965）。

## 改动

- `serde/CommandCode.java`：新增 `enum Segment { DELETE(503) }`（放在 Partition 与 ConsumerGroup 之间，与代码编号顺序一致）。
- `client/async/PartitionsClient.java`、`client/blocking/PartitionsClient.java`：新增 `deleteSegments`（含 `Long` id 便利重载，与现有方法风格一致，async 带 Javadoc）。
- `client/async/tcp/PartitionsTcpClient.java`：编码 stream id + topic id + `writeIntLE(partitionId)` + `writeIntLE(segmentsCount)`，发送 `CommandCode.Segment.DELETE`。
- `client/blocking/tcp/PartitionsTcpClient.java`：委托 async。
- `client/blocking/http/PartitionsHttpClient.java`：`DELETE .../partitions/{partitionId}` + `segments_count` 查询参数。
- 测试 `PartitionsClientBaseTest.shouldDeleteSegments`：取分区 0 的 segmentsCount，调用 `deleteSegments(…, partition.id(), 1L)`，断言之后 segmentsCount 仍为正且不增加（与 Rust `system_scenario.rs` 的断言一致：只有活跃 segment 时不会被删）。TCP 与 HTTP 两个子类都会跑。

## 验证

环境：OpenJDK 21，Gradle 9.7.1（wrapper），服务器为 `apache/iggy:edge` Docker 镜像（`--network host`，与 CI 一样用 `USE_EXTERNAL_SERVER=1`；Testcontainers 在本沙箱中因 memlock ulimit 无法启动容器）。因 Maven Central 返回 429，用 init script 把仓库指向 Google 的 Maven Central 镜像（不影响 patch）。

在 `foreign/java` 下：

| 命令 | 结果 |
|---|---|
| (red) 只加测试：`./gradlew :iggy:compileTestJava` | 失败：`cannot find symbol method deleteSegments(StreamId,TopicId,Long,long)` |
| (green) `USE_EXTERNAL_SERVER=1 ./gradlew :iggy:test --tests '*Partitions*'` | BUILD SUCCESSFUL，4/4 通过（TCP、HTTP 各 2 个） |
| 健全性检查：临时把 partition id 改为 99 | TCP、HTTP 均抛 `IggyResourceNotFoundException`，说明请求确实被服务器处理 |
| `./gradlew check -x test`（CI lint 步骤，spotless + checkstyle，全部子项目） | BUILD SUCCESSFUL |
| `USE_EXTERNAL_SERVER=1 ./gradlew :iggy:test` | 1355 tests，0 failures，4 skipped；test-results 中无 `LEAK:` |

未运行：`prek run`（全仓库 hooks）、examples/java 与 bdd/java 的 lint（未改动这些目录）、TLS 测试（CI 中也单独跑）。

## 如何提交

```bash
# 先在 issue #4369 认领并等待 assign！
git clone https://github.com/anyingiit/iggy.git && cd iggy   # 先在 GitHub fork apache/iggy
git remote add upstream https://github.com/apache/iggy.git && git fetch upstream
git checkout -b java-delete-segments upstream/master
git am /path/to/contributions/147-apache-iggy-4369/0001-feat-java-add-deleteSegments-to-partitions-client.patch
cd foreign/java && ./gradlew check -x test && cd ../..
prek run --all-files   # 或 prek run，结果填进 pr_body.md
git push -u origin java-delete-segments
gh pr create --repo apache/iggy --head anyingiit:java-delete-segments --base master \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title

`feat(java): add deleteSegments to partitions client`

## PR body

见 `pr_body.md`：

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
