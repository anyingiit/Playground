# smol-machines/smolvm #1385 — read machine name from environment

| 项 | 值 |
|---|---|
| Issue | https://github.com/smol-machines/smolvm/issues/1385 |
| Tier | 高活跃高Star（6.3k★，~1000 merged PRs；原按自由类派发，按标准改归高星） |
| Labels | enhancement, good first issue, help wanted |
| Status | ✅ ready — patch + PR text done, verified (red→green, fmt, clippy, bin tests) |
| Duplicate-PR check | 无重复。开工前与完成前两次检查：`repo:smol-machines/smolvm 1385` → 0；`SMOLVM_MACHINE_NAME` → 0；关键词 "machine name environment" → 无相关 PR；issue 无评论、无 assignee、无关联 PR（2026-09-24） |
| Base | `main` @ c890ec3 (Bump the workspace to 1.18.1 (#1388)) |
| Patch | `0001-Read-the-target-machine-name-from-SMOLVM_MACHINE_NAM.patch` |

## 问题理解
Issue 作者用 AI coding agent 在多个项目里各跑一台长期存活的 smolvm machine，希望 `--name` 可以从环境变量（如 `SMOLVM_MACHINE_NAME`）读取，这样配合 direnv 可以按目录自动选择 machine，不用每次 `smolvm machine shell/exec --name xxx`。

## 合理性判断
- 维护者自己打了 `good first issue` + `help wanted` 标签，并放进项目 Backlog。
- 项目大量用 `SMOLVM_*` 环境变量做配置；同一天刚合并了外部贡献者的 #1376（通过 `SMOLVM_BRANCH_CONTINUE` 环境变量配置 branch-continue 策略），维护者评价 "very reasonable"。
- 仓库活跃（6.3k★，~1000 merged PRs），会合并外部 PR（Bnjoroge1、fgsch 等）。
- AI 贡献政策（brief 2b）：仓库无 CONTRIBUTING / PR 模板；README、docs、.github 里 grep `AI-generated / LLM / Copilot / AI contribution` 无任何限制条款。`AGENTS.md` 只是给 agent 用的产品命令参考，不含贡献政策。→ 未禁止 AI 贡献。

## 改动
- `src/cli/machine.rs`：新增常量 `MACHINE_NAME_ENV = "SMOLVM_MACHINE_NAME"`，给"作用于已有 machine、缺省为 `default`"的命令的 `--name` 加 `env = MACHINE_NAME_ENV`：exec, shell, start, stop, status, egress-events, resize, sync, monitor, network-test。显式 `--name` 优先；`--help` 自动显示 `[env: SMOLVM_MACHINE_NAME=]`。
- 有意**不**改：`machine run`（临时 machine，前台模式下 `--name` 会被警告忽略，隐式名字会造成困惑）、`create`/`delete`/`update`/`pause`/`resume`/`branch`/`images`/`data-dir`（创建/销毁/修改类或必填 name，避免环境变量让破坏性命令隐式作用于某台机器）。PR 描述里说明，维护者如需扩大范围很容易加。
- `Cargo.toml`：clap 启用 `env` feature（不引入新依赖，Cargo.lock 无变化）。
- `AGENTS.md`：Key Flags 表中 `--name` 行补充环境变量回退说明。
- 新单测 `cli::machine::tests::machine_name_falls_back_to_env_var`：无 env→None；设 env→10 个命令都取到；显式 `--name` 覆盖；`run` 不受影响；`delete`/`update` 仍要求 `--name`。测试会改进程环境变量，放在单个 test 内并在结束时还原（仓库已有同类 `set_var` 测试写法）。

## 验证
环境：rustc/cargo 1.98.1 stable（仓库 `rust-toolchain.toml` = stable），Linux x86_64，无 KVM（不跑 VM 集成测试）。`CARGO_TARGET_DIR` 放在 work 目录，`CARGO_PROFILE_DEV_DEBUG=0`。

| 命令 | 结果 |
|---|---|
| RED：只加测试（去掉 `env = ...` 与 clap `env` feature）`cargo test --bin smolvm machine_name_falls_back_to_env_var` | ❌ FAILED：`env fallback: ["exec", "--", "true"]  left: None  right: Some("proj-vm")` |
| GREEN：同一命令 + 修复 | ✅ 1 passed |
| `cargo fmt --all -- --check` | ✅ exit 0 |
| `cargo clippy --all-targets -- -D warnings`（CI Linux/mac 用的根包范围） | ✅ exit 0 |
| `cargo test --bin smolvm`（全部 CLI 单测，CI 未单独跑但 clippy 会编译） | ✅ 144 passed, 0 failed |
| `cargo test --lib`（CI 的 "Run unit tests"） | 980 passed, 1 failed, 8 ignored。失败的 `portable_checkpoint::tests::install_verifies_and_consumes_checkpoint` 报 `could not locate the libkrun library directory`（本地没拉 Git LFS 的 libkrun）；在 base commit c890ec3 上同样失败 → 环境问题，与本改动无关 |
| 手动：`smolvm machine status --help` | 显示 `-n, --name <NAME>  Machine to check (default: "default") [env: SMOLVM_MACHINE_NAME=]` |
| 手动：`smolvm machine status` / `SMOLVM_MACHINE_NAME=proj-vm smolvm machine status` / 再加 `--name other` | `Machine 'default': not running` / `Error: vm not found: proj-vm` / `Error: vm not found: other` ✅ |

备注：`SMOLVM_MACHINE_NAME=`（空字符串）时 clap 4 会把空值当作传入，报 `machine name cannot be empty`，与 `--name ""` 行为一致；PR 里说明了。

未运行：VM 集成测试（`tests/*.sh`、需要 /dev/kvm + libkrun）、macOS/Windows CI job。

## 需要提交者注意
- 仓库无 DCO / CLA / PR 模板 / CHANGELOG 要求；PR 多为 squash merge，标题风格为普通英文祈使句（如 "Allow configuring branch-continue policy via SMOLVM_BRANCH_CONTINUE"）。
- 无 AI 贡献限制；PR 中已有 disclosure 段落。

## 如何提交
```bash
git clone https://github.com/<you>/smolvm.git && cd smolvm
git checkout -b machine-name-env origin/main
git am /path/to/0001-Read-the-target-machine-name-from-SMOLVM_MACHINE_NAM.patch
cargo fmt --all -- --check && cargo clippy --all-targets -- -D warnings && cargo test --bin smolvm
git push -u origin machine-name-env   # 然后对 smol-machines/smolvm:main 开 PR
```

## PR title
Read the target machine name from SMOLVM_MACHINE_NAME

## PR body
```markdown
## Description

Adds an optional `SMOLVM_MACHINE_NAME` environment variable that supplies `--name` when the flag is omitted, so per-project tooling such as direnv can pick the machine and `smolvm machine shell` / `smolvm machine exec -- …` work without repeating `--name`.

Scope, on purpose: the variable only applies to commands that act on an **existing** machine and today fall back to `"default"` — `exec`, `shell`, `start`, `stop`, `status`, `egress-events`, `resize`, `sync`, `monitor` and `network-test`. An explicit `--name` always wins. `machine run` (ephemeral) and the commands that create, delete or modify a named machine (`create`, `delete`, `update`, `pause`, `resume`, `branch`, …) are unchanged, so an exported variable can never make a destructive command act on a machine implicitly. Happy to widen or narrow that list if you prefer a different cut.

Implementation is clap's built-in `env = …` on those `--name` args (a shared `MACHINE_NAME_ENV` constant), which also shows `[env: SMOLVM_MACHINE_NAME=]` in `--help`. This enables clap's `env` feature; it pulls in no new crates (`Cargo.lock` is unchanged). `AGENTS.md`'s flag table mentions the fallback. Note that, as with `--name ""`, an exported-but-empty variable is rejected with "machine name cannot be empty".

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1385

## Checklist

- [x] Tests pass locally (Linux x86_64, stable 1.98.1):
  - new `cli::machine::tests::machine_name_falls_back_to_env_var` fails without the change (`left: None, right: Some("proj-vm")`) and passes with it
  - `cargo test --bin smolvm` → 144 passed
  - `cargo fmt --all -- --check` and `cargo clippy --all-targets -- -D warnings` → clean
  - `cargo test --lib` → 980 passed; the only failure, `portable_checkpoint::tests::install_verifies_and_consumes_checkpoint` ("could not locate the libkrun library directory"), fails identically on `main` in my environment (no LFS libkrun), unrelated
  - manual: `SMOLVM_MACHINE_NAME=proj-vm smolvm machine status` → `vm not found: proj-vm`; adding `--name other` → `vm not found: other`
  - VM integration tests (`tests/*.sh`, need KVM) not run
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [x] Documentation is updated (if applicable) — `AGENTS.md` Key Flags table; `--help` shows the variable automatically
```
