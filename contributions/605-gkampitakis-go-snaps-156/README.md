# gkampitakis/go-snaps #156 — Snapshot file names should be sanitized

| 项 | 值 |
|---|---|
| Issue | https://github.com/gkampitakis/go-snaps/issues/156 |
| Tier | 自由（go-snaps 约 2k stars，个人维护的 pet project） |
| Labels | bug |
| Status | ✅ ready |
| 重复 PR 检查 | /pulls?q=156 → 0 结果；issue 无评论、无指派、时间线无关联 PR（2026-10-01） |
| Base | `main` @ 07ef1d2 |
| AI 政策 | 仓库中（contributing.md、.github、labels）未发现任何 AI/LLM 相关规定；无 PR 模板，无 DCO，无 AI trailer 要求 |

## 问题理解
standalone 快照（`MatchStandalone*`）的文件名直接取自 `t.Name()`，原实现只把 `/` 换成 `_`。测试名中的 `:` `<` `>` `"` `|` `?` `*` `\` 会进入文件名，在 Windows 上非法。另外文件名会经过 `fmt.Sprintf(snapPath, n)`（`_%d` 编号），测试名含 `%` 时路径会被破坏 —— 同一处的潜在 bug，一并处理。

## 合理性判断
维护者已打上 `bug` 标签；改动局限在 `constructFilename`，不含特殊字符的测试名生成的文件名与之前完全一致，向后兼容。用户显式设置的 `snaps.Filename(...)` 不做处理（保持用户意图）。

## 改动
- `snaps/snapshot.go`：新增 `sanitizeFilename`（`strings.Map`，把 `/ \ : * ? " < > | %` 及控制字符替换为 `_`），`constructFilename` 改用它；更新 `snapshotPath` 注释。
- `snaps/snapshot_test.go`：`TestSnapshotPath` 新增子测试 `should return standalone snapPath with sanitized test name`。

## 验证
（GOCACHE/GOMODCACHE 置于 /home/user/work，Go 1.24.7）
- Red：`git stash push snaps/snapshot.go && go test ./snaps -run TestSnapshotPath -count=1` → 新子测试 FAIL（收到 `TestFunction_a:b<c>d"e\f|g?h*i%j_%d.snap`）
- Green：恢复后同命令 → PASS
- `make test`（`go test -race -count=10 -shuffle on -cover ./...`）→ 全部 ok
- `make test-trimpath` → ok
- `golangci-lint run ./...`（v2 latest）→ 0 issues
- `gofumpt -l -w -extra .` 与 `golines . -w` → 无改动

## 需要提交者注意
- 行为变化：已有快照文件名里含上述字符的用户（Linux/macOS 上原本能用），升级后会生成新的 sanitized 文件名，旧文件会被 `snaps.Clean` 标为 obsolete。已在 PR 描述中说明，若维护者介意可讨论。
- 不同测试名 sanitized 后可能映射到同一文件（如 `a:b` 与 `a_b`），这与原先 `a/b` 与 `a_b` 冲突的情况相同，未额外处理。
- 仓库无 CHANGELOG、无 PR 模板、无 DCO 要求，提交信息遵循 Conventional Commits（`fix: ...`）。

## 如何提交
```bash
git clone https://github.com/gkampitakis/go-snaps && cd go-snaps
git checkout -b fix/sanitize-snapshot-filenames origin/main
git am /path/to/605-gkampitakis-go-snaps-156/0001-fix-sanitize-standalone-snapshot-file-names.patch
make test && golangci-lint run ./...
# 或用工具脚本：
tools/submit_pr.sh contributions/605-gkampitakis-go-snaps-156 gkampitakis/go-snaps main fix/sanitize-snapshot-filenames contributions/605-gkampitakis-go-snaps-156/pr_title.txt contributions/605-gkampitakis-go-snaps-156/pr_body.md
```

## PR
Title: 见 `pr_title.txt`；Body: 见 `pr_body.md`。
