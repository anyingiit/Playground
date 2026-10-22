# git-ai-project/git-ai#1036 — Update TOML config files without losing comments

| 项 | 值 |
|---|---|
| Issue | https://github.com/git-ai-project/git-ai/issues/1036 |
| Labels | enhancement, good first issue |
| Status | ✅ ready — patch + PR text 已完成 |
| Base branch | `main`（基于 8a6184a） |
| 重复 PR 检查 | 2026-10-22：issue open、无 assignee；评论仅 dlight 建议 toml_edit + 维护者 svarlamov “欢迎基于 toml_edit 的 PR”，无人认领；`gh pr list --search 1036` / "toml comments" / "toml_edit" 无相关 PR（#2342 为 toml-node CVE 升级，无关） |
| AI 政策 | 仓库有 AGENTS.md/CLAUDE.md 专门指导 AI agent（TDD、复用代码、task lint/fmt），无禁止 AI 贡献条款 |
| DCO / CLA / changeset | 均不需要（无 DCO 检查、无 CLA bot；CHANGELOG 由 workflow 自动生成） |

## 问题理解
仓库中唯一写 TOML 的地方是 `src/mdm/agents/codex.rs`（Codex 的 `~/.codex/config.toml`，安装/卸载 hooks 时写入）。原实现用 `toml::to_string_pretty` 整体重新序列化，导致用户注释全部丢失、key 被按字母重排。issue 要求像 jsonc 一样保留注释，维护者明确欢迎基于 `toml_edit` 的实现。

## 改动
- `Cargo.toml`：新增直接依赖 `toml_edit = "0.23"`（lockfile 里已有 0.23.7 作为 proc-macro-crate 的传递依赖，只多启用了 `toml_writer`，无新下载 crate）。
- `src/mdm/utils.rs`：新增 `update_toml_preserving_format(original, desired)`——把用 `toml::Value` 算出的目标配置“同步”到由原文本解析出的 `toml_edit::DocumentMut` 上：相同值不动（保留注释/空白/顺序），变化的标量就地替换并保留 decor，删除多余 key，新 key/表追加；array-of-tables 按下标同步；仅含子表的新表设为 implicit 以避免多余 `[hooks]` 头。
- `src/mdm/agents/codex.rs`：3 处 `toml::to_string_pretty(&merged_config)` 改为 `update_toml_preserving_format(&existing_config_content, &merged_config)`；现有语义逻辑完全不变（复用已有代码，diff 小）。
- 测试：codex 2 个回归测试（安装后原文件内容逐字保留在开头、卸载后完全恢复原文件；被修改的 `[features]` 表内注释保留），utils 3 个 helper 单测。

## 验证（macOS，cargo 1.94.1，CARGO_TARGET_DIR 在工作目录）
- Red（未改实现，仅加 2 个 codex 测试）：`cargo test --lib mdm::agents::codex::tests::test_install_hooks_` → 14 passed, **2 failed**（输出中注释消失、key 重排）
- Green：同命令 + helper 测试 → 46 passed
- `cargo test --lib` → 2547 passed, 0 failed, 1 ignored
- `cargo test --test integration codex` → 64 passed
- `cargo fmt -- --check` ✓；`cargo clippy --all-targets -- -D warnings` ✓（= `task lint`）；`cargo doc --no-deps` ✓
- 未运行：完整 `task test`（全部集成测试，耗时很长）；本机无 `task`，按 Taskfile 直接用等价 cargo 命令

## 需要提交者注意
- 仓库 Conventional Commits 风格（`fix(scope): ...`），已遵循；无 AI trailer 要求。
- AGENTS.md 要求开 PR 后关注 Ubuntu CI 并回应 Devin 自动 review 的意见。
- AGENTS.md 提到“STRICT TDD with TestRepo-based tests”——本改动是 mdm 安装器的纯文件改写逻辑，沿用该模块现有的单元测试风格（`with_temp_home` + `#[serial]`），没有 git 仓库交互，未写 TestRepo 测试；若维护者要求可补。
- 行为说明：toml 0.9 的 `Map` 是有序 BTreeMap，所以新增的 key 按字母序追加在末尾；已有 key 保持原顺序。

## 如何提交
```
git clone https://github.com/git-ai-project/git-ai && cd git-ai
git checkout -b fix/codex-toml-preserve-comments
git am /path/to/204-git-ai-project-git-ai-1036/0001-*.patch
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 独立复核（2026-10-22）

PASS。新克隆 main@8a6184a 上 `git am` 干净；红：还原 3 处写入后 2 个回归测试失败；绿：`cargo test --lib -- mdm::agents::codex mdm::utils` 84 通过，`cargo test --test integration codex` 64 通过，fmt/clippy 干净。另跑 7 个临时边界用例（点号键、删除整张表、内联表、类型变化等）结果均与期望值一致。已知外观小问题：表数组按位置匹配，删除前一块时后一块会继承其注释；值始终正确。
