# prefix-dev/pixi#7105 — environments 增加可选 `description` 字段并在 `pixi info` 中显示

| 项 | 值 |
|---|---|
| Issue | https://github.com/prefix-dev/pixi/issues/7105 |
| Tier | 高星 |
| Labels | approved（“maintainers welcome contributions”）, enhancement, help wanted |
| Status | ✅ ready — patch + PR text done (not submitted); independent review passed 2026-10-01 |
| Base | `main` @ 6f71156de33ac6420522a77f21437ff0a331cb09 (2026-10-01) |
| Duplicate-PR check | 2026-10-01 开始时与结束前各查一次：`pulls?q=7105` 无结果；关键词 `description environments` 的 PR 列表中无相关 PR；issue 无评论、无 assignee、Development 区无关联分支/PR |

## 问题理解

Issue 提议：`[environments]` 里每个环境可以像 task 一样写一个 `description`，例如
`test-integration = { features = ["test", "dev-server"], description = "..." }`，替代目前用注释说明环境用途的做法，并让工具（例如 `pixi info`）能显示它。Issue 没有评论，标签 `approved` 表示维护者已认可该需求，设计很直接（字段名、形态都在 issue 中给出）。

## 合理性判断

- 维护者已打 `approved` + `help wanted`；task 已有同名 `description` 字段，属于自然对称扩展，不需要额外设计讨论。
- AI 政策：仓库无 AGENTS.md/CLAUDE.md；`.github/pull_request_template.md` 有 **AI Disclosure** 段（勾选“包含 AI 生成内容 / 已测试 / 承担责任”并写 Tools）→ 允许 AI 贡献，需披露。CONTRIBUTING 要求 conventional commits、`pixi run lint`、Rust docstring、改文档、JSON schema 改动需在 `schema/model.py`。
- 不需要 DCO；CHANGELOG 由 git-cliff 根据 commit 生成，不手改。

## 改动

- `crates/pixi_manifest/src/toml/environment.rs`：`TomlEnvironment` 新增 `description: Option<String>`，解析 `description` 键；仅写 `description` 也算有效环境（与只写 `solve-group` 一致，结果为只含 default feature 的环境）。新增 2 个解析单测。
- `crates/pixi_manifest/src/environment.rs`：`Environment` 新增 `pub description: Option<String>`。
- `crates/pixi_manifest/src/toml/manifest.rs`：把 description 传进 `Environment`（rustfmt 因元组变长重新缩进了 match，`git show -w` 实际只 +16/-7）。更新 2 个列出“允许的键”的 inline snapshot。
- `crates/pixi_manifest/src/manifests/workspace.rs`：`add_environment`（新环境）description=None；`update_environment_features` 与 `remove_feature` 重建内存中 `Environment` 时**保留** description（否则 `pixi add -e` / `pixi workspace feature remove` 之后内存态会丢失描述）；新增 2 个单测。
- 2 个 `.snap` 文件（允许键列表多了 `'description'`）。
- `crates/pixi_core/src/workspace/environment.rs`：新增 `Environment::description()`。
- `crates/pixi_cli/src/info.rs`：`EnvironmentInfo` 新增 `description`，文本输出在 `Environment:` 行下加 `Description:` 行（仅在设置时）；`--json` 中每个环境多 `"description"`（未设置为 `null`）。
- `schema/model.py` 增加字段；`schema/schema.json`、`schema/pyproject/schema.json`、`schema/pyproject/partial-pixi.json` 由 `python model.py` 重新生成（先验证过 base 上生成结果与仓库完全一致）；`schema/examples/valid/full.toml` 加了一个 description 示例。
- `docs/reference/pixi_manifest.md`：环境表字段说明与示例。
- `tests/integration_python/test_main_cli.py`：新增 `test_pixi_info_environment_description`（文本 + JSON），并在 `test_info_output_extended` 的 inline snapshot 中加 `"description": None`。
- 未做：`pixi workspace environment add --description` CLI 选项、其他命令显示描述（PR 中说明可后续添加）。

## 验证

环境：rustup 1.95.0（按 `rust-toolchain`）；`CARGO_TARGET_DIR/CARGO_HOME` 放在 `/home/user/work`，`CARGO_BUILD_JOBS=2`，`CARGO_PROFILE_DEV_DEBUG=0`（省磁盘）。Python：uv venv（py3.13）+ pixi.toml 中锁定的 pydantic 2.13.5 / jsonschema-rs 0.56.0 / pytest 9.1.1 / inline-snapshot 0.35 / dirty-equals 0.11 / py-rattler 0.25 等。本机无 `pixi`，所以没用 `pixi run ...`，而是直接运行这些 task 背后的命令。

| 命令 | 结果 |
|---|---|
| base：`cargo test -p pixi_manifest` | 665 passed, **1 failed**（`task::jinja_rendering_tests::tojson_stays_json`，单独测该 crate 时 base 上就失败，与本改动无关） |
| red：保留新测试、把 `th.optional("description")` 换成 `None`，`cargo test -p pixi_manifest description` | 4 个新测试 **FAILED**（`'description' was not expected here`） |
| red：仅把 `remove_feature` 里的 `description: env.description.clone()` 改为 `None`，`cargo test -p pixi_manifest keeps_description` | **FAILED**（left: None, right: Some("Development environment")） |
| green：`cargo test -p pixi_manifest` | 669 passed, 1 failed（同上 base 已有的 tojson 失败） |
| red：用 base 源码 + 新 Python 测试构建 `pixi`，`pytest --pixi-build=debug test_main_cli.py::test_pixi_info_environment_description ::test_info_output_extended` | 2 **failed** |
| green：`cargo build --bin pixi` 后 `pytest --pixi-build=debug -n 2 test_main_cli.py::{test_pixi_info_environment_description,test_info_output_extended,test_pixi_info_tasks} tests/integration_python/test_inline_environments.py` | **46 passed** |
| `cargo test -p pixi --test integration_rust -- parse_valid`（解析 schema/examples/valid 与 docs 中所有 manifest） | 4 passed |
| `cargo test -p pixi --test integration_rust -- environment feature` | 6 passed |
| schema：base 上 `python model.py` 生成结果与仓库一致；改后 `python model.py && pytest`（= `pixi run test-schema`） | 102 passed, 1 skipped；旧 schema + 新 full.toml → `test_manifest_schema_valid[full]` **FAILED**（red） |
| `cargo fmt --all -- --check` | OK |
| `cargo clippy -p pixi_manifest -p pixi_core -p pixi_cli --all-targets -- -D warnings` | OK（CI 用 `--workspace`，这里只跑了改动的 crate 及其依赖） |
| `ruff check` / `ruff format --check`（改动的 .py）、`typos`（改动文件）、`tombi format --check` / `tombi lint`（full.toml） | 全部通过 |
| 手工 `pixi info --manifest-path demo/pixi.toml` | 输出 `Description: Run the test suite` 等（PR body 中有摘录） |

未运行：完整 `pixi run test` / 全部 Python 集成测试（需要 conda-forge 大量下载与所有 build backend 二进制）、`ty check`、`cargo deny`、`actionlint`/`zizmor`/`dprint`（未改相关文件）。Python 集成测试的 autouse fixture 要求 `target/pixi/debug/` 下存在 5 个 `pixi-build-*` backend 二进制，本地用空的占位文件绕过（这些测试不使用 backend）；CI 会正常构建它们。

## 独立复核（2026-10-01）

- 复查 issue：仍 open、无评论、无 assignee、Development 无关联 PR；`pulls?q=is:pr 7105` 0 结果，无重复 PR。
- 重新从零构建并复现：`cargo test -p pixi_manifest description` → 5 passed；把 `th.optional("description")` 换成 `None` → 4 个新测试 FAILED（red）；恢复后 `cargo test -p pixi_manifest` → 669 passed, 1 failed（仅 `tojson_stays_json`，与本改动无关）；`cargo fmt --all -- --check` OK。
- 检查 `document.rs::update_environment_features`：删掉最后一个 feature 时保留 `{ description = ... }`，而该写法现在是合法环境，行为正确。
- 复核修正：pr_body 中误写的测试名改为 `test_info_output_extended`；删除了 PR 模板中不存在的 CHANGELOG 勾选项（模板要求删除不相关项）；AUDIT.md 中“未运行 Python 集成测试”的表述与实际不符，已更正。补丁本身未改动。

## 如何提交

```bash
git clone https://github.com/prefix-dev/pixi && cd pixi
git checkout -b feat/environment-description origin/main
git am /path/to/0001-feat-manifest-add-description-field-for-environments.patch
git push <your-fork> feat/environment-description   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`（已按仓库 PR 模板：Description / Fixes / How Has This Been Tested / AI Disclosure / Checklist）。

### 需要提交者注意
- PR 模板的 **AI Disclosure** 已勾选并写 `Tools: Claude Code`；模板注释还建议附上 prompt（可选），可自行决定是否补充。三个勾选项（已测试 / 承担责任）需要提交者本人确认。
- 若 base 已前进导致 `git am` 冲突：最可能冲突的是 `schema/*.json`（生成文件）与 `toml/manifest.rs`、snapshot 中的“允许键列表”。重新生成 schema：`pixi run generate-schema`；snapshot：`cargo insta review`。
- 设计取舍（可按维护者意见调整）：只写 `description` 也视为合法环境；`pixi info --json` 未设置时输出 `null`（与 `solve_group` 一致）；没有加 `pixi workspace environment add --description`。
- 无 DCO / changelog 要求；提交信息遵循 conventional commits，作者 anyingiit。
