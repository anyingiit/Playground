# open-policy-agent/conftest #1022 — `conftest pull git::...` fails if folder already exists

| 项 | 内容 |
|---|---|
| Issue | https://github.com/open-policy-agent/conftest/issues/1022 |
| Tier | 自由（~3k stars） |
| Labels | enhancement |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | `/pulls?q=1022` 无相关 PR；issue 无评论、无指派、无关联 PR（2026-10-01 复核） |
| Base | `master` @ 8345c40 |

## 问题理解
第二次执行 `conftest pull git::<repo>`（目标目录 `policy/` 已存在且已是 git checkout，URL 无 `?ref=`）时，go-getter（v1.8.9）的 GitGetter 走 `update` 分支：`git fetch origin -- ""` → reset → `checkout("")`，空 ref 失败（旧 git 报 `empty string is not a valid pathspec`，当前版本报 `invalid ref: ""`）。clone 分支会通过 `findRemoteDefaultBranch` 回退到默认分支，update 分支没有。go-getter main 分支至今未改。

## 合理性判断
- `downloader.go` 现有注释明确写了 git 源的既有目录“expected to already be a checkout that go-getter will update in place”，即维护者本意就是支持重复 pull 原地更新 → 本 issue 是真实 bug。
- 仓库无 AI 政策（CONTRIBUTING/DEVELOPMENT/.github 中均无 AI/LLM 规则），无 PR 模板。

## 改动
`downloader/downloader.go`：新增 `withDefaultGitRefForUpdate`——仅当 git 源、目标目录已含 `.git`、URL 无 `ref`、且不是 `//subdir` 源时，在 URL 上加 `ref=HEAD`，update 时就拉取远端默认分支（与 clone 结果一致）。其余情况（显式 ref、子目录、空目录/非 checkout 目录）行为不变，既有测试 `TestDownloadFailsWithPreexistingEmptyGitDestination` 等仍通过。
`downloader/downloader_test.go`：新增回归测试 `TestDownloadGitUpdatesExistingCheckoutWithoutRef` + helper `writeAndCommit`。

## 验证（GOFLAGS=-p=2，Go 工具链按 go.mod 自动下载 go1.27.1）
- 红：未修复时 `go test ./downloader/ -run 'Git|Empty'` → `FAIL ... client get: error downloading 'file:///tmp/...': invalid ref: ""`
- 绿：修复后 `go test ./downloader/ -count=1 -v` → 7 个测试全部 PASS
- 全量：`go test ./... -count=1` → 全部 ok
- `go vet ./downloader/`、`gofmt -l downloader` 干净
- `golangci-lint run ./...`（v2.13.2，CI 同版本，CI 用 only-new-issues）→ downloader/ 0 问题；剩余 12 个在 master 上同样存在
- 未运行：`make test-acceptance`（bats）、`test-examples`、OCI e2e（与本改动无关）

## 需要提交者注意
- 仓库要求 **DCO**：patch 已含 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`，提交时**不要**再加 `--signoff`（避免重复）。
- 要求 Conventional Commit 前缀（PR 标题会被 `validate-conventional-commit-prefix.sh` 校验），标题已为 `fix: ...`。
- 仓库无 AI 政策，PR body 中已含 disclosure 段落。

## 如何提交
```bash
tools/submit_pr.sh contributions/500-open-policy-agent-conftest-1022 open-policy-agent/conftest master fix-pull-existing-git-checkout contributions/500-open-policy-agent-conftest-1022/pr_title.txt contributions/500-open-policy-agent-conftest-1022/pr_body.md
```
手动方式：fork → `git checkout -b fix-pull-existing-git-checkout origin/master` → `git am 0001-*.patch` → push → 开 PR（base `master`）。

## PR
- Title: 见 `pr_title.txt`
- Body: 见 `pr_body.md`
