# Mozart2234/herdr-agent-pulse#1 — Singleton lock: pidfile unlink races with a starting daemon

| Item | Value |
|---|---|
| Issue | https://github.com/Mozart2234/herdr-agent-pulse/issues/1 |
| Tier | 自由 |
| Labels | bug, help wanted |
| Status | ✅ ready — patch + PR text done |
| Duplicate-PR check | 2026-09-24 (before and after implementing): issue has no comments/assignee/linked PRs; only PR in repo is #11 "docs: align runtime behavior descriptions" (unrelated) |
| Base | `main` @ 971ca17 |

## 候选选择
- pugsley76/glassbox #970/#966：标签 "Stellar Wave"，仓库有近千个自动生成式 issue（issue-farm 特征），放弃。
- herdr-agent-pulse：新仓库（2026-09-24 创建，作者 Alexei Mamani），真实的并发 bug，标注 help wanted，验收标准明确。仓库尚无已合并的外部 PR（太新），但有 PR 模板、CONTRIBUTING、CI，欢迎贡献。

## 问题理解
`SingletonLock.release()` 先 `flock(LOCK_UN)` 再 `os.remove(pidfile)`。`bin/ensure-daemon` 在每次 agent 状态事件时最多 32 个并发启动 daemon：
1. 在 unlock 和 unlink 之间启动的 daemon B 锁住同一个 inode 并写入 pid；随后 A 把文件删掉 → 路径上不再有 pidfile，下一个 daemon C 创建新文件并加锁 → B、C 同时运行（而且 ensure-daemon 看不到 B 的 pidfile，会继续拉起新 daemon）。
2. 即便先 unlink 再 unlock，仍有第二种交错：B 在 A 释放前 `open()` 了旧 inode，但在 A 删除+解锁后才 `flock()` 成功 → B 锁的是已被删除的孤儿 inode，C 同样可以锁新文件。

## 合理性判断
Bug 真实存在（已用确定性单测和 16 进程压力测试复现），与 issue 给出的方案 (1) 一致，并补上方案 (1) 单独无法覆盖的第二种交错。只用 stdlib，符合项目"stdlib only"硬规则；CONTRIBUTING 要求 Strict TDD（先 RED 后 GREEN）、Conventional Commits，均已遵守。

## 改动
- `agent_pulse/daemon.py`
  - `release()`：在仍持有锁时删除 pidfile，然后再 unlock/close。
  - `acquire_singleton_lock()`：拿到 flock 后用 `_is_same_file()` 比较句柄 `fstat` 与路径 `stat` 的 `(st_dev, st_ino)`；不一致（或路径已不存在）说明锁到的是被删除的旧 inode，关闭并重试（最多 `LOCK_ACQUIRE_ATTEMPTS = 5` 次）。这是经典的 "lock-then-verify-inode" pidfile 模式。
  - 正确性：路径只会被持锁者在持锁期间删除，因此任何通过校验的持锁者在其释放前，路径一直指向它的 inode；两个持锁者要么锁同一 inode（flock 互斥），要么需要路径在其中一个持有期间改变（不可能）。
- `tests/test_daemon.py`：`SingletonLockTests` 新增两个回归测试，分别覆盖上面两种交错（通过 `mock.patch.object` 在 `os.remove` / `fcntl.flock` 处注入"另一个 daemon 正在启动"），断言 B/C 中恰好只有一个持锁。
- `CHANGELOG.md`：新增 `[Unreleased] / Fixed` 条目（Keep a Changelog 格式）。

## 验证
在 `/home/user/work/herdr-agent-pulse`（Python 3，无需安装任何依赖）：

| 命令 | 结果 |
|---|---|
| `python3 -m unittest tests.test_daemon.SingletonLockTests -v`（仅加测试，未修复） | **RED**：2 个新测试均 FAIL `AssertionError: 2 != 1 : two daemons hold the singleton lock at once` |
| 同上，只调换 release 顺序、不加 inode 校验 | 仍有 1 个 FAIL（`..._opened_pidfile_before_release_...`）→ 证明两部分都必要 |
| 同上，完整修复 | **GREEN**：6/6 OK |
| `sh -n bin/ensure-daemon` | OK |
| `python3 -m py_compile agent_pulse/*.py` | OK |
| `python3 -m unittest discover -s tests -v`（CI 同命令） | `Ran 93 tests … OK (skipped=2)`（2 个 skip 为 `test_schema_smoke`，需要真实 herdr 二进制，CI 上同样 skip） |
| 16 进程 × 300 次 acquire/release 压力脚本（scratchpad，未提交） | 修复前：186 次持锁中 50 次时间重叠；修复后：0 次重叠 |

未运行：macOS / Python 3.9 矩阵（本地只有 Linux Python 3；代码仅用 3.9 可用语法：for-else、`unittest.mock`）。

## 如何提交
```sh
git clone https://github.com/<you>/herdr-agent-pulse && cd herdr-agent-pulse
git checkout -b fix/singleton-lock-release-race origin/main
git am /path/to/0001-fix-close-singleton-lock-race-between-pidfile-unlink.patch
git push -u origin fix/singleton-lock-release-race   # then open PR against Mozart2234/herdr-agent-pulse:main
```
仓库不要求 DCO/Signed-off-by。

---

## PR title
fix: close singleton lock race between pidfile unlink and a starting daemon

## PR body
```markdown
## Description

### What

- `SingletonLock.release()` now unlinks the pidfile **while still holding** the flock, then unlocks.
- `acquire_singleton_lock()` now, after winning the flock, checks that the handle's `(st_dev, st_ino)` still matches what is at the pidfile path. If it doesn't (or the path is gone), it locked an inode a releasing daemon just unlinked, so it closes it and retries on whatever is at the path now (bounded to `LOCK_ACQUIRE_ATTEMPTS = 5`).
- `CHANGELOG.md`: `[Unreleased] / Fixed` entry.

### Why

As described in #1, unlocking before unlinking lets a daemon started by `bin/ensure-daemon` in that gap lock the same inode; the unlink then leaves the path empty, so the next daemon creates and locks a fresh pidfile and two daemons run at once (and `ensure-daemon` can't see the first one's pid anymore).

Reordering alone (option 1 in the issue) isn't quite enough: a daemon that `open()`s the pidfile before the holder releases but reaches `flock()` only after the unlink + unlock still succeeds on the orphaned inode. The post-lock inode check closes that second window too — this is the standard "lock, then verify the path still points at what you locked" pidfile pattern. Since the path is only ever unlinked by the current holder while it holds the lock, any holder that passed the check keeps owning the path until it releases.

Still a single `daemon.pid` file, stdlib only, and `bin/ensure-daemon` is unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1

## Checklist

- [x] Added tests that failed before this change (RED) and pass after it (GREEN) — two new `SingletonLockTests` cases, one per interleaving (a daemon starting mid-release; a daemon that opened the pidfile before release but locked after). Before the fix both fail with `AssertionError: 2 != 1 : two daemons hold the singleton lock at once`; with only the release reorder, the second still fails.
- [x] `python3 -m unittest discover -s tests -v` passes locally — `Ran 93 tests … OK (skipped=2)` (the two skips are the live `herdr` schema smoke tests); `sh -n bin/ensure-daemon` and `python -m py_compile agent_pulse/*.py` also pass. Additionally, a throwaway 16-process × 300 acquire/release stress script showed 50 overlapping lock holds before the fix and 0 after.
- [x] No fixtures added or changed.
- [x] `CHANGELOG.md` is updated — `[Unreleased] / Fixed`.
- [ ] Documentation is updated — n/a (no user-facing behavior change).
```
