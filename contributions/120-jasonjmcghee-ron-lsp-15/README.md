# jasonjmcghee/ron-lsp #15 — Workspace: RON 文件在 crate 外时无法解析类型

| 项 | 值 |
|---|---|
| Issue | https://github.com/jasonjmcghee/ron-lsp/issues/15 |
| Tier | 自由 |
| Labels | bug, good first issue, help wanted |
| Status | ✅ ready（独立复审通过，2026-10-01；patch 可在 upstream main b5e8023 上 git am） |
| 重复 PR 检查 | 2026-10-01 查看了 pulls?q=is:pr，共 14 个 PR（#1–#24），没有一个涉及 workspace、crate 路径或 #15。issue 没有评论，也没人认领。 |
| Base | `main` @ b5e8023（"Release 0.1.4"） |

## 问题理解
workspace 结构是 `crates/proj_core/src/{lib.rs,user.rs}` 加上 `assets/defs/user.ron`（不在任何 crate 里）。在 user.ron 里写 `/* @[proj_core::user::User] */` 会报 "Could not find type"，而 `@[crate::user::User]` 或 `@[User]` 可以解析。

原因在 `src/rust_analyzer.rs` 的 `file_path_to_module_path`：它把所有类型都登记成 `crate::<mods>::Type`，不知道类型属于哪个 crate。结果有两个：
- 不能用真实的 crate 路径引用类型；
- 不同 crate 里同名模块的类型在 type_cache 里互相覆盖。

## 合理性判断
- 这是 issue 里描述的真实缺陷：从 crate 外引用类型，自然的写法就是用 crate 名。
- 改动向后兼容。原来的 `crate::` key 和简单名匹配都保留；新 key 放在单独的 map 里，不影响 `get_all_types`，补全里不会出现重复。
- 仓库没有 CONTRIBUTING、AGENTS.md 或 .github，也就没有 AI 政策和 PR 模板。

## 改动（仅 src/rust_analyzer.rs）
- 新增两个字段：`crate_types: HashMap<crate 限定路径, TypeInfo>` 和 `crate_type_aliases`。
- `scan_workspace`：对每个文件，用 `find_crate_name` 找它所属的 crate。做法是向上找最近的、含 `[package] name` 的 Cargo.toml，把 `-` 换成 `_`，按目录缓存结果；只有 `[workspace]` 的 Cargo.toml 会跳过。然后把该文件的 `crate::…` 类型和别名额外登记为 `<crate>::…`。如果别名的目标写成 `crate::…`，也改写成对应的 crate 名（`type_to_string` 输出的 `a :: b` 会先规范化成 `a::b`）。
- `get_type_info`：解析别名时也查 crate 别名表；在精确匹配之前，先查 crate 限定的类型表。lazy rescan 分支也做同样处理。
- `has_custom_deserializer` 的别名解析也查 crate 别名表。
- 新增 `#[cfg(test)] mod tests`，包含 `resolves_crate_qualified_paths_in_workspace`。测试按 diagnostics.rs 的写法在 temp_dir 下建 fixture：两个成员 `proj-core` 和 `other`，都定义了 `user::User`，字段不同。断言四点：
  - `proj_core::user::User` 能解析，并且有 name 字段；
  - `other::user::User` 能解析，并且有 email 字段；
  - crate 限定的别名能解析；
  - `crate::user::User` 仍然可用。

## 验证（rustc stable，CARGO_TARGET_DIR=/home/user/work/ron-lsp/target）
- Red：把实现还原成 b5e8023，只保留测试，运行 `cargo test -j2 --bin ron-lsp resolves_crate_qualified`，结果 FAILED，panic 信息是 "proj_core::user::User should resolve"。
- Green：同一条命令，1 passed。
- `cargo test -j2`：72 passed + 1 passed（tests/format_cli.rs）。base 上是 71 + 1。
- `cargo fmt --check`：通过（已运行 cargo fmt）。
- `cargo clippy -j2`：0 warnings，base 上也是 0。
- CLI 端到端：用 `[workspace] members=["crates/*"]` 的 fixture 运行 `./target/debug/ron-lsp check assets/defs/user.ron`（注解是 `@[proj_core::user::User]`），输出 "All files valid!"。故意把字段写错时，会报 "Required fields: name"。precheck 阶段在 base 上确认过，同样的文件会报 "Could not find type"。

## 独立复审（2026-10-01）
- 在 upstream main（b5e8023，ls-remote 确认仍为 HEAD）的新 clone 上 `git am` 成功；作者为 anyingiit，patch 中无 AI 模型名。
- 只还原实现、保留测试：`cargo test -j2 --bin ron-lsp resolves_crate_qualified` FAILED（panic 于 "proj_core::user::User should resolve"）；恢复 patch 后 1 passed。
- `cargo test -j2`：72 + 1 passed；`cargo fmt --check` 通过；`cargo clippy -j2`：无新增警告。
- 检查了 `has_custom_deserializer`：`TypeInfo.name` 仍为 `crate::…`，与 custom_deserializers 集合的 key 一致，crate 限定查找不影响该判断。

## 需要提交者注意
- 仓库没有 AI 政策、PR 模板、CHANGELOG，也不需要 DCO（commit 不带 Signed-off-by）。PR 正文使用标准的 disclosure 段落。
- issue 带 `help wanted`，无人认领，无需先申请 assign；如想礼貌可先在 issue 留言说明正在提 PR。
- `cargo clippy --all-targets` 有 2 条 `len_zero` 警告，位于 src/diagnostics.rs 测试代码，base 上同样存在，与本 patch 无关。
- PR 标题沿用仓库已有风格（如 #19 "Issue 18: …"）。
- 没有改 README。PR 里建议维护者自己补充 `<crate_name>::path` 写法的文档。如果想主动补，可以在 README 的注解示例旁加一句。
- 已知限制：crate 外文件里的 `crate::…` 注解在多个 crate 有同名路径时仍有歧义，这部分没有改，PR 里已说明。
- `impl Deserialize for other_crate::T` 这种以 crate 名开头的 custom deserializer 路径没有特殊处理，这是已有行为。

## 如何提交
```bash
git clone https://github.com/jasonjmcghee/ron-lsp && cd ron-lsp
git checkout -b fix/workspace-crate-qualified-paths origin/main
git am /home/user/Playground/contributions/120-jasonjmcghee-ron-lsp-15/0001-Resolve-crate-qualified-type-paths-in-workspaces.patch
cargo fmt --check && cargo clippy && cargo test
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/120-jasonjmcghee-ron-lsp-15 jasonjmcghee/ron-lsp main fix/workspace-crate-qualified-paths contributions/120-jasonjmcghee-ron-lsp-15/pr_title.txt contributions/120-jasonjmcghee-ron-lsp-15/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
