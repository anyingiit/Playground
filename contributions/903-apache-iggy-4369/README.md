# apache/iggy#4369 — Java SDK: expose deleteSegments

| 项 | 值 |
|---|---|
| Issue | https://github.com/apache/iggy/issues/4369 |
| Tier | 新锐 |
| Labels | good first issue, java |
| Status | ✅ ready（patch + PR 文案已完成；提交前须先认领 issue，见下） |
| 重复 PR 检查 | 无：PR 搜索 "4369" 0 结果；"deleteSegments" 只有已合并的其它 SDK PR（#3191 Go、#1965 JS、#1624 Rust 等）；issue 无 assignee、无评论（2026-10-01） |
| Base | `master` @ a08d0ca |

## 需要提交者注意

- **必须先认领**：CONTRIBUTING.md 要求「Create an issue or comment under existing → Wait for the issue to be assigned to you → Then code」，AGENTS.md 也写明 "The PR must link an issue the user is assigned to"。请先在 #4369 下留言认领，**等被 assign 后再开 PR**。
- **AI 政策**：允许使用 AI，但你必须能自己解释每一行、自己回答 review（否则维护者会以 "relay between reviewer and model" 关闭）。PR 模板有 `## AI Usage` 一节，pr_body.md 已按如实填写；`Rationale` 建议用自己的话再改一下（AGENTS.md: "The user should write the rationale in their own words"）。
- 新贡献者同一时间只开 **一个** PR。
- 不需要 DCO / Signed-off-by（ASF 项目）。commit 作者为 `anyingiit <49945850+anyingiit@users.noreply.github.com>`，无 AI 署名。
- 提交前请装 `prek`（`cargo install prek && prek install`），commit 时会自动跑。

## 问题理解

Rust SDK 有 `SegmentClient::delete_segments`（命令码 503），Java SDK 没有。issue 明确要求：`CommandCode` 增加 `Segment { DELETE(503) }`；blocking/async `PartitionsClient` 增加 `deleteSegments(StreamId, TopicId, Long partitionId, Long segmentsCount)`；TCP payload = stream id + topic id + partition id(u32 LE) + segments count(u32 LE)；HTTP 为 `DELETE /streams/{s}/topics/{t}/partitions/{p}?segments_count=N`；在 `PartitionsClientBaseTest` 加测试（TCP/HTTP 两个子类都会跑）。

## 合理性判断

维护者提的 good first issue，步骤写得很具体。核对了 Rust 端 `core/binary_protocol/src/requests/segments/delete_segments.rs`（编码顺序一致）和 `core/server/src/http/handlers.rs::delete_segments`（路径 + `segments_count` query 一致）。Java 传输层 `VsrOperation` 早已把 503 映射为 `DELETE_SEGMENTS`（并特殊处理为 partition group），所以只缺 API 层。

## 改动（7 文件，+116）

- `serde/CommandCode.java`：新增 `enum Segment { DELETE(503) }`
- `client/blocking/PartitionsClient.java`、`client/async/PartitionsClient.java`：新增 `deleteSegments`（含 `Long` id 的 default 重载 + javadoc）
- `client/async/tcp/PartitionsTcpClient.java`：编码并发送
- `client/blocking/tcp/PartitionsTcpClient.java`：委托到 async
- `client/blocking/http/PartitionsHttpClient.java`：DELETE + `segments_count`
- `PartitionsClientBaseTest.java`：`shouldDeleteSegmentsWithoutRemovingActiveSegment` — 写入 1 条消息，调用 `deleteSegments(…, partition.id(), 1)`，断言命令成功且 active segment 未被删除（segmentsCount=1、messagesCount=1）。测试容器使用默认 1GiB segment，无法在不改共享容器配置的前提下制造 sealed segment，所以测试验证的是「命令被 server 接受 + 语义正确」。

## 验证

环境：OpenJDK 21，Gradle wrapper 9.7.1；server 为 `apache/iggy:edge` docker 容器（本地 dockerd，去掉了 memlock ulimit/SYS_NICE），`USE_EXTERNAL_SERVER=1`。Maven Central 有 429 限流，临时在私有 GRADLE_USER_HOME 中加了 Google Maven Central 镜像 init 脚本（不影响仓库）。

- RED（stash 掉 main 改动）：`./gradlew :iggy:compileTestJava` → `PartitionsClientBaseTest.java:81: error: cannot find symbol`（deleteSegments），BUILD FAILED
- GREEN：`./gradlew :iggy:test --tests '*PartitionsTcpClientTest' --tests '*PartitionsHttpClientTest'` → 两个类各 2 个测试全过
- 全量：`./gradlew :iggy:spotlessCheck :iggy:checkstyleMain :iggy:checkstyleTest :iggy:test` → BUILD SUCCESSFUL，138 suites / 1355 tests，0 failures，0 errors，4 skipped（已 spotlessApply）
- `prek run --files <7 个改动文件>`（装了 typos、hawkeye 7.0.1）→ 所有适用 hook Passed
- 未跑：Rust/其它语言部分（未改动）

## 如何提交

```bash
git clone https://github.com/anyingiit/iggy.git && cd iggy   # 先 fork apache/iggy
git remote add upstream https://github.com/apache/iggy.git && git fetch upstream
git checkout -b java-delete-segments upstream/master
git am /path/to/0001-feat-java-add-deleteSegments-to-partitions-client.patch
git push -u origin java-delete-segments
gh pr create --repo apache/iggy --head anyingiit:java-delete-segments \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

（务必先在 issue 下被 assign。）

## PR title

见 `pr_title.txt`：`feat(java): add deleteSegments to partitions client`

## PR body

见 `pr_body.md`（按仓库 `PULL_REQUEST_TEMPLATE.md` 结构 + motivation/disclosure 段落）。
