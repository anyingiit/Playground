# floci-io/floci #4740: Lambda ESM default BatchSize per source

| 项 | 值 |
|---|---|
| Issue | https://github.com/floci-io/floci/issues/4740 |
| Tier | 新锐 |
| Labels | bug, lambda, sqs |
| Status | ⏭ skipped (2026-10-01 review): competing PR #4851 by @abdulwalidal (open, "Closes #4740", same fix: SQS 10 / others 100) appeared after prep; patch itself applied cleanly on main@f1d718c |
| 重复 PR 检查 | 2026-10-01 在 `/pulls?q=4740` 和 `/pulls?q=BatchSize` 都没有找到处理此 issue 的 PR（唯一的 open PR #4739 是 CloudFormation mapping 测试，和本 issue 无关）。issue 没有 assignee，也没有评论 |
| Base | `main` @ f1d718c |

## 问题理解
`LambdaService.createEventSourceMapping` 用的是 `toInt(request.get("BatchSize"), 10)`，所以所有 source 的默认值都是 10。AWS 只有 SQS 默认 10，Kinesis、DynamoDB Streams、Kafka、MQ 和 DocumentDB 默认都是 100。

## 合理性判断
这是 maintainer 标了 bug 的 issue，AWS 文档里也写明了默认值，要求是合理的。CloudFormation 和 SAM 的 ESM 也走这个 service 方法，所以改这一处就够了。`UpdateEventSourceMapping` 不传 BatchSize 时保留原值，这是对的，不用改。

## 改动
- `LambdaService`：新增 `defaultBatchSize(eventSourceArn)`。ARN 含 `:sqs:` 时返回 10，否则返回 100（self-managed Kafka 没有 ARN，也是 100）。
- 测试：
  - `LambdaServiceTest` 新增 SQS→10、Kinesis→100、Kafka→100、显式值优先 这几个用例；
  - 原有 Kafka 原子更新测试的期望值从 10 改为 100（它原本断言的就是错误的默认值）；
  - `EsmIntegrationTest` 新增一个 DynamoDB Streams 的 HTTP 端到端用例（Create 和 Get 都返回 100）。
- `docs/services/lambda.md` 的 ESM 一节写明了默认值。

## 验证
环境：Temurin JDK 25（项目强制要求 JDK 25），本地没有 Docker。
- Red（只加测试、不加修复）：`./mvnw test -Dtest='LambdaServiceTest#createEventSourceMapping_*+updateEventSourceMapping_invalidLaterField*'` → 14 个测试里 3 个失败，`expected: <100> but was: <10>`。
- Green：`./mvnw test -Dtest='io/github/hectorvent/floci/services/lambda/*Test'` → 共 882 个测试，ESM 相关的全部通过：LambdaServiceTest 163、EsmIntegrationTest 58、Kinesis/Sqs/DynamoDbStreams poller 测试。另外 `LambdaEventSourceMappingCfnProvisionerTest`（33）、`SamTransformProcessorTest`（71）也通过。
- 剩下 4 个类失败：LambdaVersionIntegrationTest、LambdaReactiveSyncIntegrationTest、LambdaFunctionUrlAccountRoutingTest、ContainerLauncherTest。它们依赖 Docker 或真实 runtime，或者读取沙箱的 AWS 环境变量。在 base 上不带改动跑，同样是 5 failures + 1 error，和本改动无关。
- `./mvnw checkstyle:check` ✅；`make docs-check` ✅（提交之后跑）；`make partition-check` ✅。
- 没有跑完整的 `./mvnw test`（全量太大，资源受限）。

## 需要提交者注意
- AGENTS.md 规定：commit 里不要加 AI 的 `Co-Authored-By` trailer。仓库没有 DCO 要求，也没有 AI trailer 要求，所以 patch 里没有 Signed-off-by / Assisted-by。
- PR body 用的是仓库自己的模板（Summary / Type of change / AWS Compatibility / Checklist），里面加了 motivation/disclosure 段。
- 首次贡献者的 CI 需要 maintainer 批准后才会运行。

## 如何提交
```bash
git clone https://github.com/floci-io/floci && cd floci
git checkout -b fix/lambda-esm-default-batch-size origin/main
git am /path/to/contributions/258-floci-io-floci-4740/0001-fix-lambda-default-ESM-BatchSize-per-event-source.patch
# 或者直接用脚本：
tools/submit_pr.sh contributions/258-floci-io-floci-4740 floci-io/floci main fix/lambda-esm-default-batch-size contributions/258-floci-io-floci-4740/pr_title.txt contributions/258-floci-io-floci-4740/pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
