# complytime/complyctl#881 — provider discovery tests fail when system providers are installed

| 项 | 值 |
|---|---|
| Issue | https://github.com/complytime/complyctl/issues/881 |
| Tier | 自由 |
| Labels | Test, bug, good first issue (Priority: Low, Effort: Low, milestone "ComplyTime improvements") |
| Status | ✅ ready — patch + PR text done |
| Base | `main` @ `20fc2d4` (Merge pull request #878) |
| Duplicate-PR check | 2026-09-24（开始时与结束前各查一次）：无针对 #881 的 PR；issue 未指派、0 评论。唯一提到 #881 的是维护者的 #882（MappingReferences），只是在 Review Hints 里把这 4 个失败测试标注为 "tracked in #881"，并不修复它。 |

## 问题理解
`pkg/provider/discovery.go` 的 `DiscoverProviders()` 扫描完用户目录后，**总是**再扫描写死的
`complytime.SystemProviderDir`（`/usr/libexec/complytime/providers`），无法覆盖/关闭。
在装了 provider RPM 的机器上，假定 provider 集为空/可控的单元测试会失败。Issue 由维护者
marcusburghardt 撰写，建议沿用已有的 env var override 模式（`XDG_CACHE_HOME`、`XDG_DATA_HOME`、`COMPLYTIME_WORKSPACE`）。

实测发现受影响的不止 issue 列出的 4 个测试：`internal/doctor` 的 `TestCheckProviders_NonExistentUserDir`、
`TestCheckProviders_EmptyUserDir` 以及 `cmd/complyctl/cli` 的 `TestProvidersOptions_Run_EmptyProviderDir`
也会因同一原因失败，一并修复。

## 合理性判断
- 维护者本人开的 bug + good first issue，明确给出修复方向；最新维护者 PR #882 也把它当作已知的既有失败。
- RPM spec 使用 `%gocheck2` 跑单元测试，开发者机器上装 RPM provider 是真实场景。
- 项目宪章 `.specify/memory/constitution.md` 允许 AI 辅助贡献（要求 `Assisted-by` trailer），见下方注意事项。

## 改动
- `internal/complytime/consts.go`：新增 `SystemProviderDirEnvVar = "COMPLYTIME_SYSTEM_PROVIDER_DIR"` 与
  `ResolveSystemProviderDir()`（env 非空时用 env，否则回退到 `SystemProviderDir`；与 XDG 一样把空值视为未设置）。
- `pkg/provider/discovery.go`：系统目录改用 `ResolveSystemProviderDir()`。
- `internal/doctor/doctor.go`："no providers found in …" 提示信息使用实际解析后的路径。
- 测试：受影响的 7 个测试用 `t.Setenv` 指向空临时目录；新增 `TestDiscoverProviders_SystemDirFromEnv`
  （覆盖 env 覆盖 + 用户目录优先级，走真实 `DiscoverProviders()` 而非复制逻辑），以及
  `TestResolveSystemProviderDir_Default/_EnvOverride`。doctor 测试改为断言消息包含覆盖后的路径。
- 文档：README 环境变量表、`docs/man/complyctl.md` 与 `docs/man/complyctl.1`（手工按 pandoc 输出格式同步）、
  `CHANGELOG.md` Unreleased/Fixed。

## 验证
环境：Go 1.26.8（go.mod 要求），`GOFLAGS=-mod=vendor`，以 root 运行。为复现 issue，在
`/usr/libexec/complytime/providers/` 放了一个假的可执行 `complyctl-provider-fakesys`（验证后已删除）。

1. **Base，无系统 provider**：`go test -count=1 -run "TestDiscoverProviders|TestManager_EmptyProviderDir|TestCheckProviders" ./pkg/provider/ ./internal/doctor/` → ok / ok
2. **Base，有假系统 provider（RED，复现 issue）**：同上命令 →
   FAIL `TestDiscoverProviders_EmptyDir`、`_NonPrefixedExecutables`、`_ValidProvider`、`TestManager_EmptyProviderDir`、
   `TestCheckProviders_NonExistentUserDir`、`TestCheckProviders_EmptyUserDir`；另外 `TestProvidersOptions_Run_EmptyProviderDir` 也 FAIL。
3. **只回退 discovery.go 的修复、保留新测试（RED）**：5 个 provider 测试失败，含新测试 `TestDiscoverProviders_SystemDirFromEnv`。
4. **Patched，有假系统 provider（GREEN）**：`go test -count=1 -race -v -run "TestDiscoverProviders|TestManager_EmptyProviderDir|TestCheckProviders|TestResolveSystemProviderDir" ./pkg/provider/ ./internal/doctor/ ./internal/complytime/` → 全部 PASS。
5. **完整单元测试（= `make test-unit` 的 `go test -race ./...`）**，patched，分别在无/有假系统 provider 时运行：
   除 `internal/policy` 的 `TestInvalidateForEvaluator_UnreadableFile` 外全部 ok。该测试依赖 0000 权限文件不可读，
   **以 root 运行时在 unpatched base 上同样失败**（与本改动无关，非 root CI 下应通过）。
6. `gofmt -l cmd internal pkg`（无输出）、`go vet ./...`（通过）、`git diff --check`（通过）。
   未运行：org 级 reusable CI（golangci-lint / megalinter / commitlint）、e2e/behavioral/acceptance（需构建二进制/容器）。

## 需要提交者注意
- **DCO**：宪章要求每个 commit 带 `Signed-off-by`。请用 `git am` 后 `git commit --amend -s` 自行签名（本 patch 未加）。
- **AI 披露**：宪章要求 AI 辅助的 commit 带 `Assisted-by` trailer，"identifying the tool and model"（历史示例：`Assisted-by: OpenCode (claude-opus-4-6)`）。
  按本仓库规则 commit 中不写模型名，patch 里只写了 `Assisted-by: Claude Code`；如需完全符合宪章，提交前可自行补上模型名。
- Commit 标题遵循 Conventional Commits（commitlint config-conventional）。
- PR 需两位维护者 approve。

## 如何提交
```bash
git clone https://github.com/<you>/complyctl && cd complyctl
git checkout -b fix/881-system-provider-dir-override origin/main
git am /path/to/0001-fix-provider-allow-overriding-the-system-provider-di.patch
git commit --amend -s --no-edit   # DCO sign-off
go test -race ./...                # 可选复核
git push -u origin HEAD
```

## PR title
`fix(provider): allow overriding the system provider directory`

## PR body
```markdown
## Summary

`DiscoverProviders()` always scans the hard-coded system directory `/usr/libexec/complytime/providers` after the user provider directory, with no way to override it. On machines with providers installed from RPM packages, unit tests that expect an empty or controlled provider set fail.

This PR follows the approach suggested in the issue and the existing env override pattern (`XDG_DATA_HOME`, `COMPLYTIME_WORKSPACE`):

- New `COMPLYTIME_SYSTEM_PROVIDER_DIR` env var, resolved by `complytime.ResolveSystemProviderDir()`. An unset or empty value falls back to `SystemProviderDir`, so default behaviour is unchanged.
- `DiscoverProviders()` and the doctor "no providers found in ..." message use the resolved path.
- Tests that assume no system providers point the variable at an empty temp dir via `t.Setenv`. Besides the 4 tests listed in the issue, the same problem affected `TestCheckProviders_NonExistentUserDir`, `TestCheckProviders_EmptyUserDir` (internal/doctor) and `TestProvidersOptions_Run_EmptyProviderDir` (cmd/complyctl/cli), so they are isolated too.
- New `TestDiscoverProviders_SystemDirFromEnv` exercises discovery from an overridden system dir through the real `DiscoverProviders()` (including user-dir precedence), plus unit tests for `ResolveSystemProviderDir()`.
- Documented the variable in the README env table, the man page (`.md` and `.1`), and CHANGELOG (Unreleased / Fixed).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related Issues

- Closes #881

## Review Hints

- To reproduce the original failure, place any executable named `complyctl-provider-<x>` in `/usr/libexec/complytime/providers/` and run `go test -race -run "TestDiscoverProviders|TestManager_EmptyProviderDir|TestCheckProviders|TestProvidersOptions_Run_EmptyProviderDir" ./pkg/provider/... ./internal/doctor/... ./cmd/complyctl/cli/...`. On `main` 7 tests fail; with this PR all pass.
- `go test -race ./...` passes with and without a system provider installed. (Running as root, `internal/policy` `TestInvalidateForEvaluator_UnreadableFile` fails because root can read a mode-0000 file. It fails the same way on `main` and is unrelated to this change.)
- `gofmt` and `go vet ./...` are clean. `docs/man/complyctl.1` was edited by hand to match the pandoc output for the new `.md` entry.
- If you'd rather not add a user-facing variable, the same resolver could stay test-only. I went with the env var because the issue suggested it, and it may also help packagers who install providers elsewhere.
```
