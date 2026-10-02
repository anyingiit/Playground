# celler-cache/celler #75 — Validate existence of config file after login

| 项 | 值 |
|---|---|
| Issue | https://github.com/celler-cache/celler/issues/75 |
| Tier | 自由 |
| Labels | enhancement, good first issue, help wanted |
| Status | ✅ ready — patch + PR text done |
| 重复 PR 检查 | 开始前和完成前各查一次（2026-09-24）：open PR 只有 #94（object_store）、#95（watch-store），都与本 issue 无关；issue 无 assignee、无评论、无关联 PR/分支 |
| Base | `main` @ 8d1ea58 |
| Patch | `0001-client-fail-login-if-the-config-file-cannot-be-saved.patch` |

## 问题理解
`celler login` 通过 `Config::as_mut()` 返回的 `ConfigWriteGuard` 修改配置，并依赖 guard 的 `Drop` 自动保存。
`Drop` 无法返回错误，只能 `tracing::error!("Could not save modified configuration: …")`，因此写入失败时 login 仍返回 0。
另外，若 XDG 配置路径无法确定（`get_config_path()` 失败，`path == None`），`Config::save()` 直接 `Ok(())`，完全静默。
结果：用户（issue 中是权限受限的 CI 环境）以为 login 成功，后续命令才报 `Error: No servers are available.`。

## 合理性判断
- Issue 为用户报告，维护者打了 `good first issue` + `help wanted`，诉求明确：login 后确认配置已写入。
- 仓库为 Attic 的活跃 fork（最近提交 2026-09-14），维护者（blitz）合并外部 PR（如 #91/#92 sbruder、#83 poly2it、#68 Noi0103）。
- AI 政策：仓库无 CONTRIBUTING / AGENTS.md / CLAUDE.md / PR 模板；grep `LLM|AI-generated|Copilot|ChatGPT|claude` 无结果 → 无限制。PR 描述中照常披露。

## 改动
- `client/src/config.rs`
  - `Config::save()`：无配置路径时返回错误 `Could not determine the configuration file path`；写文件错误加上下文 `Failed to write configuration to <path>`（写逻辑抽成私有 `Config::write`，行为不变）。
  - 新增 `ConfigWriteGuard::save(self) -> Result<()>`：显式保存并把错误返回给调用者（用 `ManuallyDrop` 跳过 `Drop` 中的二次保存）。`Drop` 自动保存保留，行为不变（仅在无路径时也会记录错误而非静默）。
  - 新增单元测试：`test_save_without_path_fails`、`test_guard_save_reports_write_error`、`test_guard_save_writes_config`（含 0600 权限检查）。
- `client/src/command/login.rs`：结尾由 `Ok(())` 改为 `config_m.save()`。
- `CHANGELOG.md`：Unreleased → Fixed 加一条。
- 提交信息沿用仓库风格 `client: …`（无 DCO 要求）。

## 验证
环境：`CARGO_HOME`/`CARGO_TARGET_DIR` 均在 `/home/user/work/w32/`（用后已删除）。

| 命令 | 结果 |
|---|---|
| `cargo test -p attic-client`（补丁后） | 8 passed, 0 failed（含 3 个新测试） |
| base + 仅加入 `test_save_without_path_fails` | **FAILED**（red）：base 在无路径时 `save()` 返回 Ok |
| `cargo fmt --all -- --check` | 通过 |
| `cargo clippy -p attic-client --all-targets` | 无警告（base 同样无警告） |

端到端（`target/debug/celler login test http://localhost:8080 tok`）：

| 场景 | base | 补丁后 |
|---|---|---|
| A: `$XDG_CONFIG_HOME/celler/config.toml` 不可写（悬空 symlink 指向不存在的目录；以 root 运行无法用 chmod 模拟） | 打印 ERROR 日志，**exit=0** | `Error: Failed to write configuration to …/config.toml` / `Caused by: No such file or directory`，exit=1 |
| B: `XDG_CONFIG_HOME` 是普通文件（无法确定配置路径） | 仅 WARN，**exit=0**，什么都没写 | `Error: Could not determine the configuration file path`，exit=1 |
| 正常目录 | exit=0，写入 0600 的 config.toml | 同左 |

未运行：server 相关 crate 及 nix VM integration-tests（改动仅限 client crate；server 编译需要额外 ~2GB 磁盘）。

## 如何提交
```bash
git clone https://github.com/celler-cache/celler && cd celler
git checkout -b client-login-save-errors origin/main
git am /path/to/0001-client-fail-login-if-the-config-file-cannot-be-saved.patch
git push <fork> client-login-save-errors   # 然后对 main 开 PR
```

## 需要提交者注意
- 仓库无 AI 政策、无 PR 模板、无 DCO；PR 描述已含披露段落。
- 提交信息中不含 AI 署名/co-author。

---

## PR title
client: fail `celler login` if the config file cannot be saved

## PR body
```markdown
## Description

`celler login` modifies the configuration through `ConfigWriteGuard` and relies on its `Drop` impl to save it. `Drop` can only log errors, so when the config file can't be written (e.g. insufficient permissions, as in #75) login still exits with status 0, and the problem only shows up later as `Error: No servers are available.`. When no config path can be determined at all (`get_config_path()` fails), `Config::save()` returned `Ok(())` without writing anything.

This PR:

- adds `ConfigWriteGuard::save(self) -> Result<()>`, which saves explicitly and returns the error (the guard's `Drop` auto-save is skipped in that case, and is otherwise unchanged);
- makes `Config::save()` return an error when there is no config path, and adds the file path as context to write errors;
- uses the new method at the end of `celler login`, so it now fails with e.g.
  `Error: Failed to write configuration to /…/celler/config.toml` / `Caused by: <OS error>` (e.g. `Permission denied`);
- adds unit tests for `Config`/`ConfigWriteGuard` saving and a CHANGELOG entry.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #75

## Checklist

- [x] Tests pass locally (`cargo test -p attic-client`: 8 passed, including 3 new tests; `test_save_without_path_fails` fails on `main`; `cargo fmt --all -- --check` and `cargo clippy -p attic-client --all-targets` clean). Manually: with an unwritable `config.toml` or an unusable `XDG_CONFIG_HOME`, `celler login` exited 0 before and now exits 1 with the error above; the normal case still writes a `0600` config file.
- [x] `CHANGELOG.md` is updated (if applicable) — entry under Unreleased → Fixed
- [ ] Documentation is updated (if applicable) — n/a
```
