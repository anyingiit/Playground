# prometheus/common#1005 — expfmt: OpenMetrics 1.0 输出中 unit 不是名字后缀导致整个 scrape 失败

| 项 | 值 |
|---|---|
| Issue | https://github.com/prometheus/common/issues/1005 |
| Tier | 自由 |
| Labels | 无（issue 2026-09-29 由 Rohilalala 开，0 评论） |
| Status | ✅ ready — patch + PR text done (not submitted); independently reviewed 2026-10-01 23:4x UTC |
| Base | `main` @ ca4f6e1 (2026-09-28) |
| Duplicate-PR check | 2026-10-01 23:1x UTC：`pulls?q=is:pr 1005` → 0 条；关键词 `unit` 的 PR 列表只有已合并的 #998/#969/#894/#877/#544 等，无针对本 issue 的；开放 PR 列表（#1007…#888）中无相关；issue 未指派、无认领评论、无关联分支/PR |

## 问题理解

PR #877 去掉了 `WithUnit()`（把 unit 自动追加到指标名的逻辑）之后，`MetricFamilyToOpenMetrics`（OM 0.0.1/1.0.0 编码器）在 `MetricFamily.Unit` 非空时直接写 `# UNIT <name> <unit>`，不管 unit 是否是名字的后缀。OpenMetrics 1.0 规范要求 unit 必须是 metric family 名字的后缀（MUST），Prometheus 的 OM 1.0 parser 会报 `unit "seconds" not a suffix of metric "request_duration"`，导致该 target 的**整个 scrape** 失败。client_golang v1.24.1 已能复现。

Issue 给了两个方案：(1) 编码器在 unit 不是后缀时省略 `# UNIT` 行（类比现有的“counter 没有 `_total` 就输出为 `unknown`”）；(2) 让 Prometheus parser 放宽到 OM 2.0 的 SHOULD。本补丁实现方案 (1)，这是本仓库内可以做的、最小且安全的修复（方案 2 属于 prometheus/prometheus，且旧版 Prometheus 仍会失败）。

## 合理性判断

- 现象可从代码直接确认：`openmetrics_create.go` 的 `if in.Unit != nil { ... }` 无任何校验；现有测试 `TestCreateOpenMetrics` #16 和 `TestEncode` #5–#7 甚至把无效输出（`# UNIT some_measure seconds`、`# UNIT foo_metric seconds`）写成了期望值。
- 函数文档本身承诺 “The output should be fully OpenMetrics compliant”，并对 `_total` 已有同类降级处理，方案 (1) 与现有设计一致。
- OM 2.0 编码器（`openmetrics_2_0_create.go`）不动——2.0 中后缀只是 SHOULD，`TestEncode` #8 (OM 2.0) 仍期望写出 UNIT 行。
- AI 政策：CONTRIBUTING.md、.github/、labels 页均无任何 AI/LLM 相关规定（仓库无 AGENTS.md/CLAUDE.md），无禁令。
- 风险：issue 作者 Rohilalala 近期在本仓库很活跃（#994/#995/#997/#998/#1006），有可能自己提 PR；目前未认领。维护者尚未在 issue 中表态选哪个方案。

## 改动

- `expfmt/openmetrics_create.go`：`# UNIT` 行仅在 `*in.Unit == ""`（保持原行为）或 `strings.HasSuffix(compliantName, "_"+*in.Unit)` 时写出。`compliantName` 是 counter 去掉 `_total` 后的 family 名，与 Prometheus parser 的检查一致（后缀前必须是 `_`）。文档注释新增一条说明。
- `expfmt/openmetrics_create_test.go`：#16 期望值去掉无效的 UNIT 行；新增 #18（issue 原例 `request_duration`+`seconds` → 省略）、#19（`request_durationseconds` 无 `_` → 省略）、#20（gauge `request_duration_seconds` → 保留）、#21（无 `_total` 的 counter `request_duration_seconds` → `unknown` + 保留 UNIT）。
- `expfmt/encode_test.go`：`TestEncode` 的 OM 0.0.1/1.0.0 用例（`foo_metric`+`seconds`）期望值去掉 UNIT 行；OM 2.0 用例不变。

## 验证

环境：Go 1.26.0（go.mod 指定），`GOCACHE/GOMODCACHE` 放在 `/home/user/work/s2-1254`，`GOFLAGS=-p=2`。

| 命令 | 结果 |
|---|---|
| 回退 `openmetrics_create.go`、保留新测试：`go test ./expfmt/ -run 'TestCreateOpenMetrics\|TestEncode$'` | **FAIL** — `TestEncode` 用例 4/5/6（索引从 0）多出 `# UNIT foo_metric seconds`；`TestCreateOpenMetrics` 16/18/19 多出 UNIT 行（例如 `got "# TYPE request_duration gauge\n# UNIT request_duration seconds\nrequest_duration 1.5\n"`）→ red |
| 打补丁后同一命令 `-v` | `--- PASS: TestEncode`、`--- PASS: TestCreateOpenMetrics`、OM2.0 测试全过；`ok github.com/prometheus/common/expfmt` → green |
| `go test ./...` | 除 `config` 外全部 ok；`config` 的 `TestProxyConfig_Proxy/proxy_from_environment_with_no_proxy` 失败是因为沙箱设置了 `HTTPS_PROXY` 等环境变量——**在未改动的 base 上同样失败**；`env -u HTTPS_PROXY -u HTTP_PROXY -u https_proxy -u http_proxy -u NO_PROXY -u no_proxy go test ./config/` → ok |
| `gofmt -l expfmt` | 无输出 |
| `go vet ./expfmt/` | ok |
| `golangci-lint run -j 2 ./expfmt/...`（v2.13.1，与 Makefile.common/CI 版本一致，仓库 `.golangci.yml`） | exit 0，0 issues |
| `git am` 到干净的 `ca4f6e1` | 成功 |

未做：没有拉 prometheus/prometheus 用真实 parser 做端到端验证（太重）；后缀判定规则按 issue 中引用的报错与 Prometheus parser 的“`_`+unit 后缀”规则实现。

## 需要提交者注意

- **DCO**：Prometheus 组织的仓库启用了 DCO 检查，补丁已带 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`（与作者身份一致）。如用其他邮箱提交请重新 `git commit --amend -s`。
- 提交信息遵循仓库惯例 `<pkg>: <描述>`；无 PR 模板，CONTRIBUTING 要求在 PR 描述中 @ 维护者（MAINTAINERS.md：@roidelapluie @gotjosh），已写在 pr_body.md 开头。
- CHANGELOG 由发布时整理（`## main / unreleased` 为空，近期 PR 不改它），未改。
- 这是**行为变化**：以前会输出（无效的）UNIT 行，现在省略；维护者可能更倾向方案 (2) 或其它做法（例如返回错误），PR 描述已说明理由，若维护者不同意可直接关闭。
- issue 作者近期很活跃，提交前请再看一眼 issue/PR 列表是否已有人提交。
- 仓库无 AI 禁令；PR 描述含 Claude Code 披露段落，提交信息中不含任何 AI 字样。

## 如何提交

```bash
git clone https://github.com/prometheus/common && cd common
git checkout -b expfmt-om1-unit-suffix origin/main
git am /path/to/0001-expfmt-omit-OpenMetrics-1.0-UNIT-line-if-unit-is-not.patch
go test ./expfmt/
git push <your-fork> expfmt-om1-unit-suffix   # PR 目标分支: main
# PR 标题见 pr_title.txt，正文见 pr_body.md
```

## 独立复核（2026-10-01 23:4x UTC）

- 全新 `git clone --depth 1`（main @ ca4f6e1）上 `git am` 成功；提交作者 `anyingiit <49945850+anyingiit@users.noreply.github.com>`，补丁中无 AI 模型名。
- 回退 `expfmt/openmetrics_create.go` 后 `go test ./expfmt/` 失败（TestEncode 4/5/6、TestCreateOpenMetrics 16）；打补丁后 `ok`。
- `gofmt -l expfmt` 无输出，`go vet ./expfmt/` ok，`golangci-lint` v2.13.1 `run ./expfmt/...` exit 0。
- 后缀判定（`_`+unit 为 counter 截断 `_total` 后名字的后缀，空 unit 照常输出）与 Prometheus OM parser 的 `unit %q not a suffix of metric %q` 检查一致；OM 2.0 编码器未改，符合 issue 方案 (1)。
- 再次查重：issue 仍 open、无指派、无评论、无关联 PR；最新 PR 列表（#1007…#980）中无相关 PR。

