# go-git/go-git #1518 — split fetch/push code out of `remote.go`

Status: ✅ ready — patch + PR text done (owner still has to add DCO sign-off, see 需要提交者注意)

| 项 | 值 |
|---|---|
| Issue | https://github.com/go-git/go-git/issues/1518 |
| Tier | 高活跃高Star (go-git 7.8k★, commits every day, human maintainers pjbgf / aymanbagabas / hiddeco) |
| Labels | good first issue, help wanted, tech debt |
| Status | open, no assignee, "Development: no branches or pull requests" |
| Duplicate-PR check | 2026-09-24: PR search `remote_fetch OR remote_push OR 1518` → only an unrelated dependabot PR (#1232). None of the 130 open PRs splits remote.go. The only claim was mhagger (the reporter) in 2025-04 ("after #1512 has landed"); he never opened one. The bot closed the issue 2025-11-18, and pjbgf reopened it the same day **and added `good first issue` + `help wanted`**, so it's open to anyone |
| Base | `main` @ `a5f9c22` (2026-09-24) |
| Patch | `0001-git-remote-Split-fetch-and-push-code-out-of-remote.g.patch` |

## 选题过程（简记）
- GitHub search 的次级限流很严重（和其他 agent 共享额度），所以改用 `r.jina.ai` 渲染 GitHub 的 issue 列表和 issue 页面，这样能看到评论和 linked PR。
- 跳过的候选：openbao（`AGENTS.md`/`CONTRIBUTING` 禁止 AI 生成的代码）、beets #6984（维护者说要自己做）、mypy #19660、nushell #19003、pyrefly #4299、webpack-bundle-analyzer #727（都已有 PR）、falcon 的 good-first-issue（多人已认领）、pyqtgraph #3011（已修复）、isort #2462（已在 9.0.0a2 实现）、gatus #508（`alerting.discord.title` 已经存在）、go-git #1526 / #1787（相关代码已重写，问题已过时或无法复现）。

## 问题理解
`remote.go` 有 1769 行，把 fetch、push 和两者都用的代码混在一起，但 fetch 和 push 其实几乎不共享代码。issue 提议拆成三个文件：`remote.go` 放共用部分，`remote_fetch.go` 和 `remote_push.go` 各放一边，测试也同样拆成 `remote_fetch_test.go` / `remote_push_test.go`。两位维护者都同意了（pjbgf: "sensible"，aymanbagabas: "Good idea! I don't have any concerns"）。

## 合理性判断
- 维护者明确认可，并且特意重新打开、打上 good first issue/help wanted 标签。
- `AI_POLICY.md`：允许 AI 辅助，前提是人对每一行负责、在 PR 里披露，并在 commit 里加 `Assisted-by:` trailer。
- issue 原文的函数清单是按 2025 年 `v6-transfer` 分支写的，现在的 main 已经演进了（多了 `recordPromisor`、`transportProtocol`、`usableRemoteRef`、`unstorableRefName` 等）。所以我按**当前的实际调用关系**重新做了分配（用 grep 查了每个 helper 的调用点）：
  - 被两边都用、或者被其他文件用的留在 `remote.go`：`referenceStorageFromRefs`（push 和 fetch 都调用）、`usableRemoteRef`、`unstorableRefName`、`peeledSuffix`（fetch 和 `list` 用）、`newClient`（archive.go 也用）、`transportProtocol`、`isFastForward`（worktree.go/repository.go 也用）、`List*`。
  - 导出的 sentinel error `var (...)` 块整体留在 `remote.go`，保持 godoc 分组不变（issue 原本建议把它们也拆开，在 PR 里说明了为什么不拆）。

## 改动
- `remote.go`：1769 → 297 行；`remote_fetch.go`（810 行）；`remote_push.go`（701 行）。
- `remote_test.go`：2706 → 160 行（suite 定义、TestString、TestList*、TestReferenceStorageFromRefsDropsUnusableNames）；`remote_fetch_test.go`、`remote_push_test.go`。被注释掉的 `TestUpdateShallows` 块（fetch 相关）跟着 fetch 测试走。
- **纯移动**：用一个基于 `go/ast` 的小工具（`regen/splitter.go`）按声明原样搬字节，每个文件内保持原来的相对顺序，只删掉没用到的 import，然后跑 gofmt。唯一的手工改动是把 const 块拆成两个单独的 const（`maxHavesToVisitPerRef` 只有 fetch 用，放进 `remote_fetch.go`；`peeledSuffix` 留在原处）。
- 验证纯移动：用 python 按行做 multiset 对比。`remote_test.go` 这组 2256 行完全一致；`remote.go` 这组唯一的差异就是上面说的 const 块。

## 验证（Go 1.26.0，git 2.43.0，以 root 运行）
| 命令 | main | 分支 |
|---|---|---|
| `go build ./...` / `go vet .` / `gofmt -l remote*.go` | ok | ok |
| `GOOS=windows go build .` | ok | ok |
| `go test -race -count=1 -v -run 'TestRemoteSuite\|TestFetchFastForwardForCustomRef' .` | ok, 120 PASS / 0 FAIL / 3 SKIP | ok, 120 PASS / 0 FAIL / 3 SKIP，**测试集合完全相同**（按名字 diff 了 `--- PASS/SKIP` 行） |
| `golangci-lint run .`（v2.13.1，仓库自带的 `.golangci.yaml`，用 `go install` 装的，没用 curl\|sh） | 0 issues | 0 issues |
| `go test -race -count=1 .`（整个根包） | — | 只有 `TestWorktreeSuite/TestCheckoutIndexOS` 失败；**在 main 上同样失败**（以 root 运行时断言 UID/GID != 0 不成立），跟本改动无关 |
- 这是纯重构，没有 bug 修复，所以不需要 red→green 回归测试；保证手段是"移动后测试集合和结果不变"再加上面的逐行对比。
- 没跑的：`plumbing/...` 等其他包（没改动）；`make test` 里需要 `git daemon` 的 transport 测试；`GOOS=js` 的 vet 在 main 上本来就坏（`osfs.FromRoot` 未定义，open PR #2406 正在修），跟本改动无关。

## 需要提交者注意
1. **DCO 必须签**：CI 的 `check-dco` 要求每个 commit 都有 `Signed-off-by:`。`git am` 之后运行 `git commit --amend -s --no-edit`（sign-off 必须由你本人加，我没加）。
2. **AI 披露 trailer**：go-git 的 `AI_POLICY.md` / `AGENTS.md` 要求 AI 辅助的 commit 带 `Assisted-by:` trailer，比如 `Assisted-by: Claude Code <noreply@anthropic.com>`。按我们 brief 的规定，commit 里不写模型名，所以我没加。请你按仓库政策自己在 amend 时加上（写法参考仓库最近的 commit，比如 `Assisted-by: Claude Opus 5 (1M context)`）。PR 正文里已经做了披露。
3. **commit 标题格式**：`<package>: <subpackage>, <what>. Fixes #N`，已符合 CI 的正则 `^(\*|docs|…|git|…): .+`。
4. **冲突风险**：有几个 open PR 也改了 `remote.go`（例如 #2373、#2414）。如果 rebase 时冲突，最省事的做法是在新的 main 上重新生成：`go build -o /tmp/splitter regen/splitter.go`（需要一个带 `go.mod` 的临时目录）→ 在 go-git 根目录跑 `/tmp/splitter remote.go regen/assign_remote.txt` 和 `/tmp/splitter remote_test.go regen/assign_test.txt` → 手工移动 `maxHavesToVisitPerRef` 这个 const 和注释掉的 `TestUpdateShallows` 块 → `gofmt -w remote*.go`。新增的函数要么补进 assign 文件，要么默认留在 `remote.go`，工具会对不存在的名字给出警告。
5. 维护者可能更希望在其他 remote 相关 PR 合并后的"安静期"再合入。PR 正文里已经说明，他们可以选择合入时机，或者直接关掉。

## 如何提交
```bash
git clone https://github.com/<you>/go-git && cd go-git
git checkout -b split-remote-fetch-push origin/main   # base: main
git am /path/to/0001-git-remote-Split-fetch-and-push-code-out-of-remote.g.patch
git commit --amend -s --no-edit     # DCO (+ add Assisted-by trailer per AI_POLICY)
go test -race -run 'TestRemoteSuite|TestFetchFastForwardForCustomRef' .
git push -u origin split-remote-fetch-push   # open PR against go-git/go-git:main
```

---

## PR title
```
git: remote, Split fetch and push code out of remote.go. Fixes #1518
```

## PR body
```markdown
## Description

`remote.go` had grown to ~1.8k lines mixing fetch, push and the few helpers they share. As proposed in #1518 (and agreed by @pjbgf and @aymanbagabas there), this splits it by direction:

- `remote.go`: the `Remote` type, `NewRemote`/`Config`/`String`, the exported sentinel errors, `List`/`ListContext`/`list`, and the helpers used by both directions or by other files: `referenceStorageFromRefs` (push and fetch), `usableRemoteRef`, `unstorableRefName`, `peeledSuffix`, `newClient` (also used by `archive.go`), `transportProtocol`, and `isFastForward` (also used by `worktree.go`/`repository.go`).
- `remote_fetch.go`: `Fetch`/`FetchContext`/`fetch` and everything only they reach (`fetchRefPrefixes`, `depthChanged`, `recordPromisor`, `pruneRemotes`, `getHaves*`, `calculateRefs`, `getWants`, `objectExists`, `isSupportedRefSpec`, `updateLocalReferenceStorage`, `buildFetchedTags`, `maxHavesToVisitPerRef`, `refspecAllTags`).
- `remote_push.go`: `Push`/`PushContext`/`sendPack` and their helpers (`addReachableTags`, `addReferencesToUpdate`, `checkForceWithLease`, `checkTagUpdate`, `checkFastForwardUpdate`, `objectsToPush`, `pushHashes`, `checkRequireRemoteRefs`, …).
- The tests follow the same split: `remote_fetch_test.go`, `remote_push_test.go`, and `remote_test.go` keeps the suite definition plus the `String`/`List`/shared-helper tests.

The issue's function list was written against the 2025 `v6-transfer` branch, so I redid the assignment from the current call graph on `main`. I also kept the exported error `var (...)` block together in `remote.go` so its godoc grouping doesn't change.

**It's a pure move.** Every declaration is carried over byte for byte and keeps its original relative order within its new file; only unused imports were dropped. The one edit is splitting the `const (...)` block, because `maxHavesToVisitPerRef` is fetch-only while `peeledSuffix` is shared. `git diff --color-moved` should show that. I also checked with a line-multiset comparison of old against new. Nothing changes in behaviour or API.

I'm aware this conflicts with open PRs touching `remote.go`. If you'd rather land it at a quieter moment, I'm happy to regenerate it on top of a newer `main`. The split was done mechanically, so redoing it is cheap.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1518

## Checklist

- [x] Tests pass locally: `go test -race -count=1 -v -run 'TestRemoteSuite|TestFetchFastForwardForCustomRef' .` gives 120 PASS / 3 SKIP / 0 FAIL, the same set of test names as on `main`. `go build ./...`, `GOOS=windows go build .`, `go vet .` and `golangci-lint run .` (v2.13.1, repo config: 0 issues) all pass. A full `go test -race .` fails only `TestWorktreeSuite/TestCheckoutIndexOS`, which fails the same way on `main` when run as root (UID/GID are 0).
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, internal file reorganisation only
- [ ] Documentation is updated (if applicable): n/a
```
