# wasmCloud/wasmCloud#5607 — `wash oci` ignores `SSL_CERT_FILE` and the OS trust store

| | |
|---|---|
| Issue | https://github.com/wasmCloud/wasmCloud/issues/5607 |
| Tier | 高活跃 + 高 Star（CNCF 项目，~2.4k★，双周发版） |
| Labels | `enhancement`, `good first issue` |
| Status | ✅ 实现 + 单测 + clippy + nightly fmt 通过 |
| 重复 PR 检查 | 无引用 #5607 的 PR（2026-09-24 检查） |

## 问题理解
`wash oci push/pull`（以及同样走 `RegistryArgs` 的 `wash inspect`）只信任编译进来的 webpki 根证书 +
`--ca-path`/`WASH_OCI_CA_PATHS`。私有 CA（如 kind 集群里的 Harbor）即使已经在系统信任库或
`SSL_CERT_FILE` 里，也会失败于 `invalid peer certificate: UnknownIssuer`，且报错不提示 `--ca-path`。
issue 提议：OCI 命令默认信任 “webpki + native roots”，并对证书错误给出提示。

## 合理性判断
- 维护方打了 `good first issue`，并给出了具体实现方向（`rustls_native_certs::load_native_certs()` → DER → `extra_root_certificates`）。
- 仓库在 `host/http_client.rs` 里已有 `TrustRoots::WebpkiAndNative`，并明确写了：**对 host 的出站流量，信任系统库是显式 opt-in**（扩大信任边界）。
  因此本实现把 native roots 做成 wash-runtime 的**进程级 opt-in**（默认关闭，host 行为不变），只由交互式 CLI（`wash oci`、`wash inspect`）打开 —— 与 issue（“OCI commands”）和既有安全立场一致。
- `rustls-native-certs` 已是 wash-runtime 依赖，无新增依赖（`cargo machete` 不受影响）。

## 改动
- `crates/wash-runtime/src/oci.rs`
  - 新增 `pub fn set_trust_native_roots(bool)`（`AtomicBool`，默认 false）。
  - native roots 通过 `OnceLock` 只加载一次；加载错误 `warn!` 并跳过。
  - `usable_trust_roots()` 只保留 webpki 能接受的证书并转为 DER —— 关键：代码注释已说明 `oci-client` 遇到一张解析失败的证书会**整体回退到默认配置**，而系统库里常有个别 webpki 拒绝的条目。
  - `extra_ca_certificates()` 在开启时追加 native roots。
  - 新单测 `only_usable_native_roots_are_trusted`（不触碰全局状态，避免与现有 `no_ca_paths_leaves_the_trust_store_unclaimed` 互相干扰）。
- `crates/wash/src/cli/oci.rs`：`RegistryArgs::oci_config` 打开 native roots；新增 `with_ca_hint()`，错误链含 `UnknownIssuer` 时在顶层加上 `--ca-path` / `WASH_OCI_CA_PATHS` / 系统信任库提示（保留原始错误链）；更新 `--ca-path` 帮助文本；2 个新单测。
- `crates/wash/src/cli/inspect.rs`：同样应用提示。

## 验证
| 命令 | 结果 |
|---|---|
| `cargo test -p wash-runtime --no-default-features --features oci --lib oci::` | 19 passed, 1 ignored ✅ |
| `cargo test -p wash --lib cli::oci` | 2 passed ✅（`unknown_issuer_errors_point_at_ca_path`、`other_errors_are_left_alone`） |
| `cargo clippy -p wash-runtime -p wash --features "wash-runtime/wasi-tls,wash/host-component-plugins"`（CI 的 `OPTIONAL_FEATURES`） | 0 warnings ✅ |
| `cargo +nightly fmt -- --check`（CI 的 Format 步骤） | ✅ |
| CI 的 “anyhow context 小写” grep 检查 | ✅ 无命中 |

说明：单测运行后只改动了 `--ca-path` 的 doc comment 与 `debug!` 宏的换行（fmt），随后 clippy 已完整编译通过。
`--all-targets` 的 clippy 需要 `cargo xtask build-fixtures` 预先生成 wasm fixtures，且会命中 `sockets/tcp.rs` 里一个与本改动无关的既有 test-only lint，CI 也不跑 `--all-targets`。
未做真实私有 CA registry 的端到端测试（需要 kind + Harbor）。

## 需要提交者注意
- 仓库最近的提交带 `Signed-off-by`（CNCF 项目常见 DCO）。补丁里**没有**替你签署；应用后请执行 `git commit --amend -s` 自行签署。
- 提交类型：`feat(wash):`（CONTRIBUTING 要求 `<type>: <description>`）。

## 如何提交
```bash
git clone https://github.com/<you>/wasmCloud && cd wasmCloud
git checkout -b wash-oci-native-roots origin/main
git am /path/to/0001-feat-wash-trust-the-system-certificate-store-for-OCI.patch
git commit --amend -s --no-edit      # DCO sign-off
cargo test -p wash --lib cli::oci && cargo +nightly fmt -- --check
git push -u origin HEAD              # base: main
```

### PR — chefs-pick-oss-starter 格式
**Title:** `feat(wash): trust the system certificate store for OCI commands`

```markdown
## Description

`wash oci push`/`pull` (and `wash inspect`, which shares `RegistryArgs`) only trusted the compiled-in webpki
roots plus `--ca-path` bundles. A registry behind a private CA therefore failed with `UnknownIssuer` even
when that CA was already in the OS trust store or in `SSL_CERT_FILE`/`SSL_CERT_DIR`, and the error said
nothing about `--ca-path`.

- `wash-runtime` gains `oci::set_trust_native_roots(bool)`. When on, every OCI client also trusts the
  platform's native roots (`rustls_native_certs`, which honours `SSL_CERT_FILE`/`SSL_CERT_DIR`). They are
  loaded once, and filtered to certificates webpki accepts before being handed to `oci-client` as DER —
  one unparsable OS-store entry would otherwise make `oci-client` fall back to a wholly default config.
- It is **off by default**, so a host keeps the reproducible compiled-in roots, matching the explicit
  opt-in `TrustRoots::WebpkiAndNative` already takes for outbound HTTP. The CLI (`wash oci`, `wash inspect`)
  turns it on. `--ca-path` / `WASH_OCI_CA_PATHS` are unchanged for scoping trust explicitly.
- When a push/pull/inspect fails with `UnknownIssuer`, the error now leads with a hint to pass the CA via
  `--ca-path` (or `WASH_OCI_CA_PATHS`) or add it to the system trust store; the original cause chain is kept.
- `--ca-path` help text updated accordingly.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #5607

## Checklist

- [x] Tests pass locally
  - `cargo test -p wash-runtime --no-default-features --features oci --lib oci::` → 19 passed (new: `only_usable_native_roots_are_trusted`)
  - `cargo test -p wash --lib cli::oci` → 2 new tests pass
  - `cargo clippy -p wash-runtime -p wash --features "wash-runtime/wasi-tls,wash/host-component-plugins"` → clean
  - `cargo +nightly fmt -- --check` → clean
  - Not tested end-to-end against a private-CA registry (no kind/Harbor available here)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, release notes are generated by the release train
- [x] Documentation is updated (if applicable) — `--ca-path` help text
```
