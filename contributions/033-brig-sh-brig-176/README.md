# brig-sh/brig#176 — Completion never offers `--json` on `ls`, `agent ls` or `secret ls`

| Field | Value |
|---|---|
| Issue | https://github.com/brig-sh/brig/issues/176 |
| Tier | 新锐 |
| Labels | bug, good first issue (milestone M2) |
| Status | ✅ ready — patch + PR text done |
| Duplicate-PR check | none. Checked the open PR list, PR searches "completion" and "json" (incl. closed), and the issue timeline (no assignee, no comments, no linked PR) — at start and again right before finishing (2026-09-24). |
| Base | `main` @ `039aabe` (2026-09-21) |
| Patch | `0001-fix-cli-offer-json-when-completing-ls-agent-ls-and-s.patch` |

## 为什么这个项目符合「新锐」

- **brig-sh/brig**：Go 写的 AI coding agent 沙箱工具（macOS 上用 hull microVM，Linux 上用 nerdctl），管理凭据转发和宿主目录挂载的安全边界。
- 约 **130 stars**，2026-08 下旬才开始公开开发（仓库很新），已发布 v0.2.0。
- **多名真实维护者**：最近 80 个 commit 里有 Panagiotis Moustafellos (34)、Alexandros Sapranidis (25)、Anastassios Nanos (9)、Maria Gkoutha (3)、Vangelis Katsikaros、Spiros Economakis、PanagiotisMavrikos 等；本周内（9/16–9/21）都有提交和合并，PR 走 review + `Reviewed-by`。
- 工程规范严格（CONTRIBUTING、AI_POLICY、DCO 检查、smoke test、"测试不许消失"检查），不是 issue farm：good-first-issue 只有 5 个，都是维护者 pmoust 手写的具体 bug。

## 需要提交者注意

- **AI 政策**（`AI_POLICY.md`）：明确欢迎 AI 辅助和 agentic 贡献，**不要求披露**，但要求提交者对改动负责、真的跑过测试、不能夸大验证结果；"External automation must not flood issues/PRs"。本 PR 只有一个小改动，符合要求。PR 里保留了我们的 motivation/disclosure 段落（政策允许描述所用工具）。
- **DCO 必须**：CONTRIBUTING 要求每个 commit `git commit -s`，CI 有 DCO 检查。补丁里**没有** `Signed-off-by`，请用 `git am --signoff` 应用（见下）。
- **以 draft 打开 PR**，CI 绿了再 mark ready（CONTRIBUTING 要求）。
- PR 模板要求：不适用的 checklist 项用 `~~删除线~~` 划掉，不要删掉。
- commit 规范：Conventional Commits，header ≤72 字符，body 讲 why，trailer 用 `Fixes: #176` —— 补丁已照做。
- 另一个候选 #307（`brig sh` 参数被 `bash -lc` 重新解析）已有 open PR #308，所以没做。

## 问题理解

`brig ls --json`、`brig agent ls --json`、`brig secret ls --json` 都能用（各自的报错信息也写着 "takes no arguments other than -q and --json"/"other than --json"），但 shell 补全一个都不提示：

```
$ brig __complete ls -        -> :names --quiet -q
$ brig __complete agent ls -  -> :none
$ brig __complete secret ls - -> :none
```

原因：`cmd/brig/completion.go` 里 `ls` 的 flag 列表硬编码成 `{"--quiet", "-q"}`（注释还写着过时的 "One flag, no operand"），`groups` 表里 agent 和 secret 的 `{name: "ls"}` 没有声明任何 flag。
`TestGroupsTableCoversEveryGroupFlag` 没抓到，因为这三个 ls 都是手工解析参数（没有 `flag.FlagSet`），而且该测试只检查 flag 名"在表里某处出现"，不检查挂在哪个子命令上。

## 合理性判断

- 维护者 pmoust 提的 bug，标 `good first issue`、milestone M2，issue 里直接给出了修法；代码在当前 main 上仍然是 issue 描述的样子。
- `brig policy ls` 不接受 `--json`（`rejectPolicyTail`），`telemetry status` 也没有，所以只改 issue 列出的三处，没扩大范围。
- #145（把 verb 表统一成一份）是更大的重构，不在本 issue 范围内。

## 改动

- `cmd/brig/completion.go`：`ls` 的候选改为 `{"--quiet", "-q", "--json"}`，更新过时注释（说明它手工解析、drift 测试看不到，要和 `listSandboxes` 保持同步）；`groups` 表 agent/secret 的 `ls` 行加 `flags: []string{"--json"}`。
- `cmd/brig/completion_test.go`：`TestCompletePositions` 表里加 3 个用例（`ls -`、`agent ls -`、`secret ls -` 必须精确给出对应 flag），并把旧用例名 "ls takes one flag and no operand" 改为 "ls takes no operand"（子测试名，不影响 `check-tests-kept.sh`，它只看顶层 `func Test*`）。
- 文档无需改：`docs/completions.md` 没有逐 verb 列 flag。

## 验证

环境：Go 1.26.0（go.mod 要求），linux/amd64，root 用户，`GOCACHE`/`GOMODCACHE` 放在 `/home/user/work/brig-cache`（已删除）。

Red（未修复代码 + 新测试）：
```
$ go test ./cmd/brig/ -run TestCompletePositions
--- FAIL: TestCompletePositions/ls_offers_--json_beside_--quiet: candidates [--quiet -q], want exactly [--quiet -q --json]
--- FAIL: TestCompletePositions/agent_ls_offers_--json: directive ":none", want ":names" (candidates [])
--- FAIL: TestCompletePositions/secret_ls_offers_--json: directive ":none", want ":names" (candidates [])
FAIL
```
Green（修复后）：
```
$ go test ./cmd/brig/ -run 'TestComplete|TestGroupsTable' -v   -> 全部 PASS（含 3 个新用例、TestGroupsTableCoversEveryGroupFlag）
```
真实二进制（`make build`）：
```
brig __complete ls -        -> :names --quiet -q --json
brig __complete ls --       -> :names --quiet --json
brig __complete agent ls -  -> :names --json
brig __complete secret ls - -> :names --json
brig __complete policy ls - -> :none   (不变，policy ls 本来就不收 --json)
```
CI 各步骤（CONTRIBUTING "What CI checks"）：
- `gofmt -l .` → 无输出 ✅
- `go vet ./...` → ok ✅
- `go test -race -covermode=atomic ./...` → 除 `internal/wrap` 外全部 ok。`internal/wrap` 的 `TestWorkspaceBehindATrustedLinkThroughWritableTerritoryIsRefused` 失败，**在未修改的 base 上同样失败**（本机以 uid 0 运行，root 拥有的临时目录被当成"可信"，属环境问题；本补丁不碰 `internal/wrap`）。另有 "no such tool covdata" 提示出现在无测试的包上，是本机 toolchain 下载缺该工具，不影响结果。
- `script/smoke.sh` → patched 4 次：第 1 次有 1 项 `FAIL argv names the variables only`，后 3 次 339/339 全 ok；base 跑 5 次全 ok。该项检查 run 路径（本补丁不涉及），stub 用多次 `printf` 追加写 `argv.log`，并发调用时行可能交错，判断为既有的偶发 flake，与本改动无关。
- `script/check-tests-kept.sh HEAD~1 HEAD` → "every test present at 039aabe is still here" ✅
- 交叉编译 `GOOS=darwin GOARCH=arm64 go build ./...`、`GOOS=linux GOARCH=amd64 go build ./...` ✅
- 未运行：`goreleaser check`/snapshot（本机无 goreleaser，且本改动不涉及发布配置）；真实 runtime（hull/nerdctl）—— 本改动不碰 run/exec/credential 路径。

## 如何提交

```bash
git clone https://github.com/brig-sh/brig.git && cd brig
git checkout -b fix/complete-ls-json origin/main
git am --signoff /path/to/0001-fix-cli-offer-json-when-completing-ls-agent-ls-and-s.patch   # adds the DCO Signed-off-by
make all && script/smoke.sh
git push -u <your-fork> fix/complete-ls-json
# open the PR as a DRAFT against main; mark ready once CI is green
```

---

## PR title

```
fix(cli): offer --json when completing ls, agent ls and secret ls
```

## PR body

```markdown
## Summary

`brig ls`, `brig agent ls` and `brig secret ls` all accept `--json` (their own refusals even say so), but completion offered it on none of them: `brig __complete ls -` answered only `--quiet -q`, and `agent ls -` / `secret ls -` answered `:none`. `completion.go` hard-coded `ls`'s flags as `{"--quiet", "-q"}`, and the `ls` rows of the agent and secret groups declared no flags.

`TestGroupsTableCoversEveryGroupFlag` could not catch this: all three listings read their arguments by hand rather than through a `flag.FlagSet`, and the test only checks that a registered flag appears somewhere in the table, not on which subcommand. So the fix adds `--json` in the three places the issue names, and pins each listing with its own case in `TestCompletePositions`. `policy ls` takes no `--json` and is left alone.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issues

Closes #176. Refs #145 (one verb table would remove the hand-kept copy this bug lived in).

## Changes

- `cmd/brig/completion.go`: offer `--json` after `brig ls` alongside `-q`/`--quiet`, and declare `--json` on the `agent ls` and `secret ls` rows of the groups table; replace the stale "One flag, no operand" comment with one saying why the drift test cannot see these flags.
- `cmd/brig/completion_test.go`: three new `TestCompletePositions` cases (`ls -`, `agent ls -`, `secret ls -`), each failing before the change; the old "ls takes one flag and no operand" case is renamed "ls takes no operand" (a subtest name only).

## Checklist

- [x] `make all` passes (vet, test, build) — `gofmt -l .` clean, `go vet ./...` ok, `go test -race ./...` ok except `internal/wrap`'s `TestWorkspaceBehindATrustedLinkThroughWritableTerritoryIsRefused`, which fails identically on the unpatched base on my machine (I ran as uid 0, so the root-owned temp dirs read as trusted); this change does not touch `internal/wrap`
- [x] `script/smoke.sh` passes — 339/339 ok (one earlier run had a single failure in "argv names the variables only" on the run path, not reproduced in 3 more runs; unrelated to completion)
- [x] I have added or updated tests covering the change — red before the fix, green after
- [ ] ~~I have run `go test ./... -race`, if the change touches concurrency, subprocesses or the daemon~~ (ran anyway, see above)
- [ ] ~~I have exercised the change against a real runtime (`brig run <agent>`), if it touches the run, exec or credential path~~
- [ ] ~~I have updated the affected docs~~ — `docs/completions.md` does not list per-verb flags, so nothing to change

Also checked with the built binary: `brig __complete ls -` → `--quiet -q --json`, `ls --` → `--quiet --json`, `agent ls -` → `--json`, `secret ls -` → `--json`, `policy ls -` → `:none` (unchanged). `script/check-tests-kept.sh` passes; darwin/arm64 and linux/amd64 cross-builds pass.
```
