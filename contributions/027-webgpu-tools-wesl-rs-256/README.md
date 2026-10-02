# webgpu-tools/wesl-rs #256 — `mat_ctor_ty` zero-value missing template has wrong error message

| Issue | Tier | Labels | Status | Duplicate-PR check |
|---|---|---|---|---|
| https://github.com/webgpu-tools/wesl-rs/issues/256 | 新锐 | good first issue, Bug | ✅ ready — patch + PR text done | None. Issue: no assignee, no comments, "Development: No branches or pull requests" (re-checked at the end). Open PRs (#299 Interner, #286 Wildcard imports, #285 overrides) are unrelated; PR search for "matrix" shows only old closed PRs. |

## 为什么这个项目符合"新锐"

- **webgpu-tools/wesl-rs**: WESL (WGSL Extended) 的 Rust 编译器/求值器，WESL 是 WebGPU 着色器语言工作组 (wgsl-tooling-wg) 推进的 WGSL 扩展（imports、条件编译等），被 Bevy 生态使用（仓库里就有 bevy-wgsl 测试）。
- ~135 stars，创建于 2024-08，MIT/Apache 双许可。
- 真实维护者：Mathis Brossier (k2d222, collaborator)、Benjamin Brienen、stefnotch 等；2026-07 以来人类提交者至少 9 人（Mathis Brossier 23、Benjamin Brienen 12、stefnotch 4、Stuart Parmenter、Lukas Kalbertodt、Jannik Obermann、JMS55、charlotte、bigwingbeat）。
- 本周有提交（2026-09-23: #301, #303）。非 issue farm：issue 由贡献者手写、有真实讨论/实现。

## 需要提交者注意

- 仓库没有任何 AI/LLM 贡献政策（grep AGENTS/CLAUDE/CONTRIBUTING/.github 无相关条款）；CONTRIBUTING 很简短，只建议去 Discord 提问。PR 正文里已做 disclosure。
- 无 DCO、无 CHANGELOG、无 PR 模板；提交信息风格为小写短句（如 "fix compiling file or directory by name directly (#303)"）。
- 开着的 PR #299 "Interner" 可能大面积改动 `wgsl-types`，如果先合并可能需要 rebase（本补丁只在 `ctor.rs` 两个 else 分支开头加了 3 行 + 一个常量 + 测试模块，冲突概率低）。

## 问题理解

`mat2x2()`（任何 `matCxR()` 无模板参数、无实参）在 WGSL 中是非法的：WGSL 只有带模板的零值构造 `mat2x2<f32>()`，因为无法从零个实参推断分量类型。wesl-rs 在两处处理这种调用：
- 类型检查 `type_ctor` → `mat_ctor_ty(c, r, &[])`
- 求值 `call_builtin_fn` → `ctor::mat(c, r, &[])`

两处都直接 `convert_all_ty(&[])`，空列表返回 `None`，于是报 "matrix components are incompatible"，误导用户（根本没有分量）。带模板的版本 `mat_ctor_ty_t` 已有 "matrix constructor expects arguments" 的空参检查，无模板版本漏了。

## 合理性判断

Issue 由活跃贡献者 BenjaminBrienen 提出，标签 Bug + good first issue，范围小且明确；未修复（base `38b8f0c38b29bc84be7438e6dc086e1e217d0c0e` 上 `wesl eval 'mat2x2()'` 仍报 "matrix components are incompatible"）。合理。

## 改动

`crates/wgsl-types/src/builtin/ctor.rs`：
- 新增常量 ``ERR_MAT_ZERO_VALUE = E::Builtin("the zero-value matrix constructor requires a template argument (e.g. `mat2x2<f32>()`)")``（`E::Builtin` 只接受 `&'static str`，所以示例固定写 `mat2x2<f32>()`）。
- `mat()`（求值）和 `mat_ctor_ty()`（类型检查）在非转换分支开头：`args.is_empty()` 时返回该错误。
- 新增 `#[cfg(test)] mod tests`（wgsl-types 之前没有单元测试）：覆盖 mat2x2/mat3x4/mat4x2 的 `type_ctor` 与 `mat` 两条路径，并确认带模板的 `mat2x2<f32>()` 仍然返回 `mat2x2<f32>`。

范围说明：`array()`（无模板无实参）也会报 "array elements are incompatible"，同类问题但不在 issue 范围内，PR 中作为可选后续提及。`vecN()` 无参是合法的（AbstractInt 零向量），代码已正确处理。

## 验证（Rust 1.98.1，`CARGO_TARGET_DIR` 在工作目录）

| 步骤 | 命令 | 结果 |
|---|---|---|
| Red（只加测试） | `cargo test -p wgsl-types --lib` | ❌ 1 failed: `left: "matrix components are incompatible"` vs 期望消息 |
| Green | `cargo test -p wgsl-types --lib` | ✅ 2 passed |
| CI 同款全量测试（含子模块 wesl-testsuite） | `RUSTFLAGS="-C debuginfo=0 -D warnings" CARGO_INCREMENTAL=0 cargo test --workspace --lib --bins --tests --benches` | ✅ rc=0；testsuite 582 passed / 7 ignored，其余全部 ok |
| 格式 | `cargo fmt --all -- --check` | ✅ |
| Clippy | `cargo clippy --workspace --all-targets -- -Dwarnings` 与 `--all-features` | ✅ 均无警告 |
| 端到端 base | `cargo run -p wesl-cli -- eval 'mat2x2()'` | `error: matrix components are incompatible` |
| 端到端 patched | 同上 / `mat3x4()` / `mat2x2<f32>()` / `mat2x2(1,2,3,4)` | 新错误消息 / 新错误消息 / `mat2x2(vec2(0f, 0f), vec2(0f, 0f))` / `mat2x2(vec2(1.0, 2.0), vec2(3.0, 4.0))` |

未运行：CI 的 grammar/wasm/miri 等其它 job（与本改动无关；miri 在 CI 中本身已禁用）。

## 如何提交

```bash
git clone https://github.com/<you>/wesl-rs && cd wesl-rs   # fork of webgpu-tools/wesl-rs
git checkout -b fix-mat-zero-value-error origin/main        # base: 38b8f0c38b29bc84be7438e6dc086e1e217d0c0e
git am /path/to/0001-fix-error-message-for-zero-value-matrix-constructor-.patch
git push -u origin fix-mat-zero-value-error
```

---

## PR title

`fix error message for zero-value matrix constructor without template`

## PR body

~~~markdown
## Description

`mat2x2()` (or any `matCxR()`) with neither a template argument nor constructor arguments is not valid WGSL: the only zero-value matrix constructor is the templated one, e.g. `mat2x2<f32>()`, since the component type can't be inferred from zero arguments. wesl-rs did reject it, but with a misleading message:

```
$ wesl eval 'mat2x2()'
error: matrix components are incompatible
```

Root cause: both `mat_ctor_ty` (type checking) and `ctor::mat` (evaluation) call `convert_all_ty` on the argument list, which returns `None` for an empty list. The templated variant `mat_ctor_ty_t` already has an explicit empty-args check; the untemplated ones did not.

This PR adds an `args.is_empty()` check to both functions, returning:

```
error: the zero-value matrix constructor requires a template argument (e.g. `mat2x2<f32>()`)
```

(`Error::Builtin` takes a `&'static str`, so the example is always `mat2x2<f32>()`; happy to switch to a different wording or error variant if you prefer.)

I also added a small unit-test module in `wgsl-types/src/builtin/ctor.rs` covering both code paths for a few matrix shapes, plus a check that `mat2x2<f32>()` still type-checks. The same kind of message also happens for `array()` ("array elements are incompatible"); I left that alone to keep this focused on the issue, but can fold it in if wanted.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #256

## Checklist

- [x] Tests pass locally (`cargo test --workspace --lib --bins --tests --benches` with `RUSTFLAGS="-C debuginfo=0 -D warnings"`: all green, incl. testsuite 582 passed / 7 ignored; new test fails before the fix and passes after; `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets [--all-features] -- -Dwarnings` clean)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, error message only
~~~
