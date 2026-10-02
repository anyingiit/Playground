# prometheus/blackbox_exporter#1687 — Have --config.check validate referenced local files

| 项 | 值 |
|---|---|
| Issue | https://github.com/prometheus/blackbox_exporter/issues/1687 |
| Tier | 高星（~5k+ stars，Prometheus 官方，非常活跃） |
| Labels | 无（issue 2026-09-30 由 LionelTrichet 开，尚无维护者回复/分类） |
| Status | ✅ ready — patch + PR text done (not submitted); independently reviewed 2026-10-01 23:5x UTC |
| Base | `master` @ 2bd1bf8 (2026-09-29, "Bump github.com/andybalholm/brotli ... (#1683)") |
| Duplicate-PR check | 2026-10-01 23:3x UTC：issue open、0 评论、未指派、无关联 PR；`pulls?q=1687` 仅命中无关的 dependabot #1374；`pulls?q=config.check` 仅命中已关闭（stale）的 #1138（probe type 校验，与本需求无关）；最新 10 个 PR（#1675–#1688）无相关内容 |

## 问题理解

`blackbox_exporter --config.check` 目前只做 YAML 解析 + 各 probe 的 `UnmarshalYAML` 校验，不检查配置里引用的本地文件。于是 `body_file`、TLS `ca_file/cert_file/key_file`、`password_file`、`credentials_file` 等指向不存在文件的配置也会 “Config file is ok”，直到真正 probe 时才失败。Issue 希望 `--config.check` 作为部署前预检（systemd / k8s / 容器启动）时能发现这些问题，**只做本地检查，不做网络访问**。

## 合理性判断

- 需求明确、范围小，与 Prometheus 生态一致（`promtool check config` 也会检查引用文件是否存在）。
- 维护者尚未回复（issue 只开了一天），存在维护者希望不同实现/不接受的风险——PR 描述里已写明可随意关闭。
- AI 政策：仓库无 CONTRIBUTING/AGENTS/CLAUDE.md；`.github/` 只有 ISSUE/PR 模板、dependabot、workflows；grep `LLM/AI-generated/Copilot/ChatGPT/agent` 无相关命中（只有 CHANGELOG 中 “User-Agent” 等无关词）；Issue 无 label。未发现 AI 禁令。
- PR 模板要求：标题 `area: short description`；**DCO sign-off（`git commit -s`）**；导出 API 需要注释；release-notes 块。

## 改动

- `config/config.go`：新增导出方法 `(*Config).CheckFiles() error`，按模块名排序遍历，检查：
  - `http.body_file`
  - http 与 `websocket.http_config` 的 HTTPClientConfig：`basic_auth.username_file/password_file`、`authorization.credentials_file`（`bearer_token_file` 会被 common 的 `Validate()` 转成它，所以不单独检查）、`oauth2.client_secret_file/client_certificate_key_file/tls_config.*`、`tls_config.ca_file/cert_file/key_file`、`http_headers.<name>.files`
  - `websocket.headers.<name>.files`
  - tcp / unix / dns / grpc 的 `tls_config.*`
  - 用 `os.Open` + `Stat` 判断存在、可读、不是目录；所有错误 `errors.Join` 一次性返回，带 `module "x": <yaml路径>:` 前缀。
- `main.go`：只在 `--config.check` 分支调用 `CheckFiles()`，失败时 `logger.Error` 并返回 1；flag help 文案更新。正常启动/热加载行为**不变**。
- `README.md`：补充一段 `--config.check` 说明。
- `config/config_test.go` + `config/testdata/check-files-good.yml`、`check-files-missing.yml`、`files/body.txt`：新增 `TestCheckFiles`（存在的文件→nil；缺失文件/目录→逐条匹配错误信息）。

## 验证

环境：`GOCACHE/GOMODCACHE` 指向 `/home/user/work/s2-1259/`，go1.26.0（go.mod 要求，自动下载 toolchain）。

| 命令 | 结果 |
|---|---|
| 仅回退 `config/config.go`（保留新测试）：`go test -count=1 ./config/ -run TestCheckFiles` | **red**：`sc.C.CheckFiles undefined (type *Config has no field or method CheckFiles)` → build failed（新 API，红的形式为编译失败） |
| 应用修改：`go test -count=1 ./config/ -run TestCheckFiles -v` | **green**：`--- PASS: TestCheckFiles` |
| `go test -count=1 -p 2 ./config/ .` | `ok .../config`、`ok .../blackbox_exporter` |
| `go vet ./config/ .` | 无输出 |
| `gofmt -l .` | 无输出 |
| `golangci-lint run -j 2 ./config/... .`（按 Makefile.common 版本 v2.13.1 本地 `go install`，仓库 `.golangci.yml`） | `0 issues.`（第一次提示 revive receiver-naming，已把 receiver 改为 `s` 与现有方法一致） |
| `yamllint config/testdata/check-files-*.yml`（仓库 `.yamllint`） | ok |
| 手动：`cd config && blackbox_exporter --config.file testdata/check-files-missing.yml --config.check` | rc=1，`level=ERROR msg="Error checking files referenced in config" err="module \"http_post_body_file\": http.body_file: open testdata/files/missing-body.txt: no such file or directory\n...\nmodule \"websocket_auth\": websocket.http_config.authorization.credentials_file: testdata/files is a directory"` |
| 手动：`--config.file testdata/check-files-good.yml --config.check` / 根目录 `--config.file blackbox.yml --config.check` | rc=0，`Config file is ok exiting...` |
| `git am` 到干净 master worktree | 正常应用，7 files changed, 167 insertions(+), 1 deletion(-) |

未运行：`./prober/...` 测试（未改动 prober 包，且需要网络/ICMP 权限）、`make style check_license unused`（等价的 gofmt / 新文件无 .go 新增 → license 头不受影响已人工确认）。

## 需要提交者注意

- **DCO 必需**：PR 模板要求每个 commit `Signed-off-by`。patch 里**没有**加，`git am` 时请用 `git am -s`（或之后 `git commit --amend -s --no-edit`）用你自己的身份签署。
- 维护者尚未回复该 issue；可能希望把检查放到 `ReloadConfig` 里（影响运行时 reload）或只在 check 模式——本 PR 选了最保守的“仅 check 模式”，PR 描述里已解释。
- 对 `tls_config` 只要写了文件路径就检查（即使该 probe 未开启 `tls: true`）；若维护者觉得过严可再收窄。
- 不在 commit 中写 AI 署名；PR 描述含 disclosure 段落。

## 独立复核（2026-10-01）

- 全新 `git clone --depth 1`（master @ 2bd1bf8）后 `git am` 正常应用；作者 `anyingiit <49945850+anyingiit@users.noreply.github.com>`；patch 中无 AI 模型名。
- 回退 `config/config.go`/`main.go`/`README.md`：`TestCheckFiles` 编译失败（red）；应用后 PASS；`go test ./config/ .` ok；`gofmt -l .`、`go vet` 无输出；golangci-lint v2.13.1 `0 issues.`。
- 复查 issue：仍 open、无评论/指派/关联 PR；open PR 列表中无相关实现。
- 结论：覆盖 issue 列出的 TLS/body_file/credential 文件，只在 check 模式运行、无网络访问，符合需求，无需修改。

## 如何提交

```bash
git clone https://github.com/<you>/blackbox_exporter.git && cd blackbox_exporter
git remote add upstream https://github.com/prometheus/blackbox_exporter.git
git fetch upstream && git checkout -b config-check-files upstream/master
git am -s /path/to/contributions/167-prometheus-blackbox_exporter-1687/0001-config-check-referenced-local-files-with-config.chec.patch
go test ./config/ .
git push -u origin config-check-files
# 打开 PR：标题见 pr_title.txt，正文见 pr_body.md（填入 PR 模板）
```

## PR title

见 `pr_title.txt`：`config: check referenced local files with --config.check`

## PR body

见 `pr_body.md`。
