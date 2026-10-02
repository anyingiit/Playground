# maciejhirsz/logos#562 — The handbook docs should be moved into the rustdoc

| 项 | 值 |
|---|---|
| Issue | https://github.com/maciejhirsz/logos/issues/562 |
| Tier | 自由 |
| Labels | book, documentation, good first issue |
| Status | ✅ ready — patch + PR text done (not submitted, independently reviewed 2026-10-01)；⚠️ 提交前请先人工阅读 issue 的 3 条评论（见“需要提交者注意”） |
| Base | `master` @ fba6c4d (2026-09-11, "Merge pull request #579") |
| Duplicate-PR check | 2026-10-01：`pulls?q=562` 只命中无关的 #382；关键词 `handbook OR rustdoc OR book` 的 41 个 PR 中没有针对 #562 的（#563 是 #554 的 partial input 文档；#578 是 workspace 重构，open，可能与本补丁冲突）。Issue 无 assignee、无关联 PR/分支 |

## 问题理解

Issue（Lokathor，2026-05-22）：`Logos` derive 宏的 rustdoc 页面“basically nothing there”（只列出 helper 属性名），所有用法说明都在外部 handbook 网站上，`cargo doc --offline` 看不到。希望把 handbook 的解释放进 crate 的 rustdoc，使文档集中在一处。

## 合理性判断

- 维护者已打 `documentation` + `book` + `good first issue` 标签，说明接受此方向。
- 仓库没有 CONTRIBUTING 文件 / AGENTS.md / CLAUDE.md / PR 模板；book 的 Contributing 章节（`book/src/contributing*.md`）鼓励“improving the documentation (either in the crate or in the book)”，要求跑 `cargo fmt`、`cargo clippy`、`cargo test --workspace`，无 AI 相关规定（`grep -ril -e LLM -e AI-generated -e "AI contribution" -e Copilot -e ChatGPT` 只命中 logos.png / example.json 的二进制/数据噪声）。
- 外部贡献者的文档 PR 常被合并（#582、#576、#550、#545、#525 等）。
- 范围选择（需要维护者可调整）：不是把整本 book 原样复制，而是在 derive 宏上写一份紧凑的“属性参考”，涵盖 handbook 中解释属性/宏行为的章节（Getting started、Attributes、`#[logos]`、`#[token]/#[regex]`、Token disambiguation、Callbacks、Extras、Subpatterns、Custom error、Source lifetime、utf8）。教程类章节（context-dependent lexing、examples、debugging、unicode、contributing）仍留在 book，book 不改动。

## 改动

仅 `src/lib.rs`（+377/-1）：
- 在 `#[cfg(feature = "export_derive")] pub use logos_derive::Logos;` 上加文档注释。rustdoc 会把 re-export 上的文档并入 derive 宏页面，且示例作为 `logos` crate 的 doctest 运行（放在 proc-macro crate `logos-derive` 里则无法依赖 `logos` 跑 doctest）。
- 内容：示例 / `#[token]`、`#[regex]` 语法（含 `ignore(case)`）/ 优先级计算与冲突处理 / 回调及返回类型表 / 全部 `#[logos(...)]` 选项（skip、extras、error 两种形式、utf8、lifetime、subpattern、type、crate、export_dir，选项列表根据 `logos-codegen/src/parser/mod.rs` 核对）。9 个新 doctest。
- crate 级文档的 handbook 链接改为同时指向 derive 宏文档。

## 验证

环境：stable rustc/cargo 1.97.0，`CARGO_TARGET_DIR=/home/user/work/logos/target CARGO_BUILD_JOBS=2`。

| 命令 | 基线 (fba6c4d) | 打补丁后 |
|---|---|---|
| `cargo doc -p logos --no-deps` 后查看 `target/doc/logos/derive.Logos.html` | 只有属性名列表，无任何说明（red） | 完整说明（约 12k 字符正文），所有锚点/intra-doc 链接解析正常（green） |
| `cargo test --doc -p logos` | 9 passed | 18 passed（9 个新 doctest） |
| 把冲突示例中的 `priority = 3` 去掉再跑 doctest | — | 按预期编译失败（“all at the priority 2”），证明文档中关于优先级的说明与实际一致；已恢复 |
| `cargo test --doc -p logos --features state_machine_codegen` / `--features forbid_unsafe` | — | 18 passed / 17 passed |
| `cargo test --workspace`（CI 的 `cargo test --verbose` 子集更大） | — | 全部 ok，0 failed |
| `cargo fmt --check` | — | OK |
| `cargo clippy --features debug -- -D warnings` | — | OK |
| `RUSTDOCFLAGS="-D warnings" cargo doc -p logos --no-deps --features debug`；以及 `--no-default-features` | — | 无 warning |

未运行：CI 的 nightly `RUSTDOCFLAGS='--cfg docsrs' cargo +nightly doc -Zrustdoc-scrape-examples`（本机无 nightly）、`cargo hack` feature powerset、tarpaulin、msrv（1.80）检查、mdbook（book 未改）。本补丁只改文档注释，不影响编译代码。

### 独立复核（2026-10-01）

- 重新确认无重复 PR（`pulls?q=is:pr 562` 只有无关的 #382；`rustdoc` 只命中 #578/#546/#413，均非本 issue）。Issue 评论仍无法读取（WebFetch 不渲染评论，`gh api`/api.github.com 被代理 403）。
- 内容核对：`#[logos(...)]` 选项与 `logos-codegen/src/parser/mod.rs` 一致（`source` 已弃用，未列出，正确）；`export_dir` 的 `.dot`/`.mmd` 行为与 `logos-codegen/src/lib.rs` `generate_graphs` 一致；优先级说明与 book `token-disambiguation.md` 一致（book 原文“range/class 加 1”与 `[a-zA-Z]+` 为 2 的说法本身略含糊，补丁照搬 book 的表述）。
- 复跑：基线 fba6c4d `cargo test --doc -p logos` 9 passed，`derive.Logos.html` 正文约 686 字符、无 “Token disambiguation”（red）；补丁后 18 passed，正文约 11.9k 字符（green）；去掉 `priority = 3` 后 1 个 doctest 失败并报 “all at the priority 2”（17 passed/1 failed），已恢复；`cargo fmt --check` OK；`cargo clippy --features debug -- -D warnings` OK；`RUSTDOCFLAGS="-D warnings" cargo doc -p logos --no-deps` 无 warning。
- 复核改动：在 `use core::fmt::Debug;` 与新文档注释之间加一个空行（纯格式），amend 后重新导出补丁，`git am` 到 fba6c4d 验证通过。

## 如何提交

```bash
git clone https://github.com/maciejhirsz/logos && cd logos
git checkout -b docs-derive-reference origin/master
git am /path/to/0001-docs-lib-document-the-Logos-derive-macro-in-rustdoc.patch
cargo test --doc -p logos
git push <your-fork> docs-derive-reference   # PR 目标分支: master
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 需要提交者注意

- ⚠️ **Issue 显示有 3 条评论，但本环境无法读取**（WebFetch 渲染的页面不含评论；GitHub API/`gh api` 对该仓库被代理 403）。提交前请务必在浏览器中阅读这 3 条评论：确认没有人认领、维护者没有给出不同的范围要求（例如要求用 `include_str!` 复用 book 文件、或认为不应重复 book 内容）。如有冲突请调整或放弃。
- 范围是“紧凑参考 + doctest”，不是整本 book 搬迁；PR 描述中已说明并请维护者决定是否需要扩展。内容与 book 有一定重复，后续 book 修改时需同步——维护者可能对此有意见。
- 提交信息采用仓库 PR 中常见的 Conventional Commits 风格（`docs(lib): ...`）。无 DCO、无 changelog、无 PR 模板、无 AI 政策；PR 正文含 Claude Code 披露段落。
- 开放中的 #578（workspace 布局重构）若先合并，`src/lib.rs` 可能被移动，需要 rebase。
