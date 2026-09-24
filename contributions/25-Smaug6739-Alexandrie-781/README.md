# Smaug6739/Alexandrie#781 — Backend should not abort when S3 storage does not support PutBucketPolicy

| | |
|---|---|
| Issue | https://github.com/Smaug6739/Alexandrie/issues/781 |
| Tier | 自由 |
| Labels | backend, bug, good first issue |
| Status | ✅ ready |
| Duplicate-PR check | 2026-09-24: no open/closed PR for #781 (searched `781`, `bucket policy`, listed all 14 open PRs — none related); issue unassigned, 0 comments. Re-checked before finishing. |
| Base branch | `main` @ ccf5603 |

## 问题理解
Issue 作者用 Garage 作为 S3 兼容存储部署 Alexandrie 8.14.2，后端启动时报
`s3 | Failed to set bucket policy: Unimplemented action: PutBucketPolicy` 并退出。
原因：`backend/app/minio.go` 的 `setupPublicBucket()` 在 `SetBucketPolicy()` 失败时直接 `os.Exit(1)`。
Garage 官方兼容性文档中 PutBucketPolicy 标记为未实现，Garage 的公开读取需通过其自身的 website/`bucket allow` 配置完成。

## 合理性判断
- 项目文档/README 称支持 "S3-compatible object storage"（RustFS/MinIO-compatible），Garage 属于此类；
- 同文件中备份桶的 `SetBucketLifecycle` 失败已经只是 `logger.Warn`，本修复保持一致；
- 公开读策略只是便利设置，管理员可在存储端手动配置，不是后端运行的必要前提 → 请求合理。
- 仓库无 AI 贡献政策（grep AGENTS/CLAUDE/CONTRIBUTING/.github 无相关条款）；维护者经常合并外部 PR（#780、#766、#764、#760…）。
- 提交风格：Conventional Commits（`fix(scope): ...`），squash 时自动附 `(#PR)`。

## 改动
- `backend/app/minio.go`：`SetBucketPolicy` 失败时改为两条 `Warn`（错误本身 + 提示管理员在 S3 端开启公开读取），然后 `return`，不再 `os.Exit(1)`。
- `backend/app/minio_test.go`（新增）：用 `httptest` 起一个假 S3（接受建桶，对 `PUT ?policy` 返回 Garage 同样的 `501 NotImplemented / Unimplemented action: PutBucketPolicy`），调用 `setupPublicBucket`，断言函数正常返回且确实发出了 PutBucketPolicy 请求。

## 验证
环境：Go 1.24.7 + `GOTOOLCHAIN=auto`（go.mod 要求 go 1.26.0，自动下载工具链），GOPATH/GOCACHE 放在 work 目录。

| 命令 (in `backend/`) | 修复前 | 修复后 |
|---|---|---|
| `go test ./app/ -run TestSetupPublicBucket -v` | **FAIL** — 打印 `Failed to set bucket policy: Unimplemented action: PutBucketPolicy` 后进程被 `os.Exit(1)` 杀死 (`FAIL alexandrie/app`) | **PASS** |
| `go vet ./app/` | – | ok |
| `gofmt -l app` | – | 无输出 |
| `go build ./...` | – | ok |
| `go test $(go list ./... \| grep -v /tests)` | – | `ok alexandrie/app` |
| `go test ./tests/` | FAIL（`connection refused localhost:8201`，需运行中的后端+MySQL） | 同样 FAIL，原因相同，与本改动无关 |

仓库 CI（`.github/workflows/pr-check.yml`）只对 `frontend/**` 跑 lint/typecheck；本改动仅涉及 backend，故前端检查不适用。

## 如何提交
```bash
git clone https://github.com/<you>/Alexandrie && cd Alexandrie
git checkout -b fix/s3-bucket-policy-not-fatal origin/main
git am /path/to/0001-fix-s3-do-not-abort-startup-when-PutBucketPolicy-is-.patch
git push -u origin fix/s3-bucket-policy-not-fatal   # 然后对 Smaug6739/Alexandrie:main 开 PR
```

## 需要提交者注意
- 无 DCO / 签名要求；无 AI 政策。
- 可选：先在 issue 下留言表示在处理（CONTRIBUTING 未强制）。

---

## PR title
`fix(s3): do not abort startup when PutBucketPolicy is unsupported`

## PR body
```markdown
## Description

With an S3-compatible store that does not implement `PutBucketPolicy` (e.g. Garage), the backend exits on startup with `s3 | Failed to set bucket policy: Unimplemented action: PutBucketPolicy`, because `setupPublicBucket()` in `backend/app/minio.go` calls `os.Exit(1)` when `SetBucketPolicy` fails.

The public-read policy is a convenience: the same access can be configured on the storage side (for Garage via its own bucket/website settings). So this PR makes the failure non-fatal, the same way a failing lifecycle rule on the backup bucket is already handled: it logs a warning with the error and a hint that the bucket must be made publicly readable on the provider side, then continues startup. Bucket creation errors are still fatal, as before.

A unit test (`backend/app/minio_test.go`) starts an in-process fake S3 server (`httptest`) that accepts bucket creation but answers `PUT ?policy` with Garage's `501 NotImplemented` error, and checks that `setupPublicBucket` returns normally. Without the fix the test binary is killed by `os.Exit(1)`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #781

## Checklist

- [x] Tests pass locally (in `backend/`: `go test ./app/ -v` → new test FAILS before the fix (process exits via `os.Exit(1)`), PASSES after; `go vet ./app/`, `gofmt -l app` clean, `go build ./...` ok. The integration tests in `backend/tests` need a running server + MySQL and were not run)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (no changelog file; releases are generated)
- [ ] Documentation is updated (if applicable) — n/a (the new log message tells admins what to configure)
```
