# csaf-rs/csaf #736: Align get_ssvc_v2 with the typed accessors' Option<Result<..>> signature

| Item | Value |
|---|---|
| Issue | https://github.com/csaf-rs/csaf/issues/736 |
| Tier | 自由 |
| Labels | CSAF 2.0, CSAF 2.1, enhancement, good first issue (Type: Task, milestone: Library) |
| Status | ✅ done: patch + PR text ready (base `main` @ `cd5bb07f1d8f`, 2026-09-24) |
| Duplicate-PR check | Checked 2026-09-24, before starting and again at the end: issue has no assignee, no linked PR/branch and no comments; PR searches for `736`, `ssvc` (open) and `get_ssvc_v2` return nothing related. The only related PRs are the merged #715 and #747 (this issue is a follow-up to #715) |
| AI policy | No AGENTS.md/CLAUDE.md/CONTRIBUTING; grep for LLM/AI-generated/Copilot/ChatGPT/Claude finds nothing, so there is no restriction. Disclosure paragraph is in the PR body anyway |

## 问题理解

`ContentTrait` 的 CVSS typed accessor（#715 引入）用 `Option<Result<T, serde_json::Error>>` 区分「metric 不存在」（`None`）和「存在但无法反序列化」（`Some(Err)`）。`get_ssvc_v2` 比这更早，返回 `Result<SelectionList, _>`，把两种情况都折叠成 `Err`，所以 CSAF 2.0 的实现（2.0 没有 SSVC）只能伪造一个 `"SSVC metrics are not implemented in CSAF 2.0"` 错误。Issue（由 maintainer 在 #715 review 讨论后提出）给出的方案：

- `get_ssvc_v2` 改为返回 `Option<Result<SelectionList, serde_json::Error>>`
- 2.0 实现返回 `None`；2.1 实现在 `ssvc_v2` map 为空时返回 `None`，否则返回 `Some(反序列化结果)`
- `has_ssvc_v2` 改成 trait 默认方法 `self.get_ssvc_v2_raw().is_some()`，和 `has_cvss_v*` 保持一致
- 调整 crate 内的调用方

## 合理性判断

- Issue 由核心团队在 #715 的 review 讨论后提出，方案写得很具体，并标了 `good first issue` 和 milestone "Library"。
- 这是 public trait 的 breaking change。Issue 里说它适合"跟下一个 breaking release 一起发"。所以 commit 用了 `refactor!:` 加 `BREAKING CHANGE:` footer（仓库用 Conventional Commits，并由 commitlint 检查）。
- 仓库会合并外部贡献（例如 gronke 的 #715 和 #747 就是这个 issue 的来源）。README 里要求 Conventional Commits。没有 PR template，也没有 changelog 文件（发布说明由 release 流程生成），所以不需要 changelog 条目。

## 改动（6 files, +71 / −31，全部在 `csaf-rs/src`）

- `csaf/traits/vulnerabilities/content_trait.rs`
  - `has_ssvc_v2` 现在是默认方法：`self.get_ssvc_v2_raw().is_some()`
  - `get_ssvc_v2` 的签名改为 `Option<Result<SelectionList, serde_json::Error>>`，并补了 doc 注释
  - `Score`（CSAF 2.0）：`get_ssvc_v2` 返回 `None`，删除 `has_ssvc_v2` override 和不再使用的 `serde::de::Error` import
  - `Content`（CSAF 2.1）：空 map 返回 `None`，否则返回 `Some(SelectionList::deserialize(&self.ssvc_v2))`（沿用原来的借用反序列化，不 clone），删除 `has_ssvc_v2` override
  - 新增 3 个单元测试：present→`Some(Ok)`；nonconforming→`Some(Err)`；absent→`None`（2.1 `Content` 和 2.0 `Score` 都测）
- `validations/test_6_1_47.rs`、`test_6_1_48.rs`、`test_6_1_49.rs`：`if has_ssvc_v2() { match get_ssvc_v2() {..} }` 改为 `if let Some(ssvc_result) = get_ssvc_v2() { match ssvc_result {..} }`（缩进不变，diff 很小）
- `validations/test_6_2_37.rs` 和 `validations/utils/ssvc.rs`：issue 没有列出这两个调用方，但签名改了它们就编译不过。前者改为 `let Some(Ok(selection_list)) = ... else { continue }`（去掉多余的 `has_ssvc_v2` 判断，保留"解析失败由 6.1.46 报告"的注释）；后者去掉 `.filter(has_ssvc_v2)`，改为 `.get_ssvc_v2().and_then(Result::ok)`，行为不变（跳过不存在或解析失败的 metric）

## 验证

环境：rustc/cargo 1.98.1，`CARGO_TARGET_DIR=/home/user/work/csaf-target`，已初始化 `csaf` submodule（OASIS 测试数据）。

| Step | Command | Result |
|---|---|---|
| Baseline (unpatched main) | `cargo test -p csaf-rs --locked` | lib: **517 passed**, 0 failed; other targets 1 passed, 1 passed / 11 ignored |
| Red: base + only the new tests | `cargo test -p csaf-rs --lib --locked ssvc_accessor` | **does not compile**: 4× E0599 (`is_none` not found on `Result`; `expect`/`is_err` not found on `SelectionList`). On the old API an absent SSVC metric was `Err(..)`, not `None` |
| Green (patched) | `cargo test -p csaf-rs --locked` | lib: **520 passed** (517 + 3 new `ssvc_accessor_*`), 0 failed; other targets unchanged |
| Format | `cargo fmt --all -- --check` | clean |
| Lint | `cargo clippy --workspace --exclude csaf-service --all-targets --all-features --locked -- -D warnings` | clean |
| Docs | `RUSTDOCFLAGS="-D warnings" cargo doc -p csaf-rs --no-deps --locked` | clean |

Not run:
- `csaf-service`: its dependency `utoipa-swagger-ui` has a build script that downloads Swagger UI from GitHub, and that is blocked in this sandbox. `csaf-service` never references SSVC (grep), so the change cannot affect it.
- `--release` / cross-target CI matrix, Go/WASM binding tests, type-generator drift check: no generated files were touched.

## 如何提交

```bash
git clone https://github.com/csaf-rs/csaf && cd csaf
git checkout -b refactor/ssvc-v2-option-result origin/main
git am /path/to/0001-refactor-return-Option-Result-.-from-ContentTrait-ge.patch
git push <your-fork> refactor/ssvc-v2-option-result
# open PR against csaf-rs/csaf:main
```

### 需要提交者注意
- PR title must follow Conventional Commits; pre-checks CI lints it. Use the title below.
- It is a breaking API change, as the issue says. Maintainers may want to hold it for the next breaking release.
- No DCO/sign-off requirement found. No AI policy found.

## PR title

```
refactor!: return Option<Result<..>> from ContentTrait::get_ssvc_v2
```

## PR body

```markdown
## Description

Implements the proposal from #736 (follow-up to the review discussion in #715): `ContentTrait::get_ssvc_v2` now has the same shape as the typed CVSS accessors, so an absent SSVC metric is no longer reported as an error.

- `get_ssvc_v2` returns `Option<Result<SelectionList, serde_json::Error>>`: `None` when the metric is absent, `Some(Err(_))` when it is present but does not deserialize.
- CSAF 2.0 (`Score`) returns `None` instead of fabricating `"SSVC metrics are not implemented in CSAF 2.0"`. The now-unused `serde::de::Error` import is removed.
- CSAF 2.1 (`Content`) returns `None` for an empty `ssvc_v2` map and `Some(SelectionList::deserialize(&self.ssvc_v2))` otherwise. It keeps the existing borrowed deserialization, so nothing is cloned.
- `has_ssvc_v2` is now a default trait method (`self.get_ssvc_v2_raw().is_some()`), mirroring `has_cvss_v2`/`has_cvss_v3`/`has_cvss_v4`. Both overrides are removed.
- Call sites: `test_6_1_47.rs`, `test_6_1_48.rs` and `test_6_1_49.rs` now use `if let Some(ssvc_result) = content.get_ssvc_v2() { match ssvc_result { .. } }`. Two call sites that the issue did not list also needed updating, and their behavior is unchanged:
  - `test_6_2_37.rs` uses `let Some(Ok(selection_list)) = .. else { continue }`. Parse failures are still left to 6.1.46.
  - `validations/utils/ssvc.rs` uses `.get_ssvc_v2().and_then(Result::ok)` in place of the separate `has_ssvc_v2` filter.
- Added unit tests next to the existing typed-CVSS accessor tests in `content_trait.rs`. They cover a present metric (`Some(Ok)`), a non-conforming map (`Some(Err)`), and an absent metric (`None`, for both CSAF 2.1 `Content` and CSAF 2.0 `Score`).

This changes the public signature of `ContentTrait`, so the commit is marked `refactor!` with a `BREAKING CHANGE:` footer. As the issue suggests, it may be best to merge it with the next breaking release.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #736

## Checklist

- [x] Tests pass locally: `cargo test -p csaf-rs --locked` gives 520 passed, 0 failed (517 on `main` plus the 3 new `ssvc_accessor_*` tests). The new tests do not compile against the old signature. `cargo fmt --all -- --check`, `cargo clippy --workspace --exclude csaf-service --all-targets --all-features --locked -- -D warnings` and `RUSTDOCFLAGS="-D warnings" cargo doc -p csaf-rs --no-deps` are all clean. I could not build `csaf-service` locally because its `utoipa-swagger-ui` build script needs network access; it does not reference SSVC.
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the repo has no changelog file. The breaking change is recorded in the commit's `BREAKING CHANGE:` footer.
- [ ] Documentation is updated (if applicable): the rustdoc of `get_ssvc_v2` is updated. No other docs reference this method.
```
