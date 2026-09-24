# pyrite-wiki/pyrite #363 — KB_NOT_FOUND for KBs added with `pyrite kb add`

| 项 | 值 |
|---|---|
| Issue | https://github.com/pyrite-wiki/pyrite/issues/363 |
| Tier | 自由 |
| Labels | bug, cli, good first issue |
| Status | ✅ ready — patch + PR text done (full suite not completed, 60-file related subset green) |
| 重复 PR 检查 | 2026-09-24: issue 无评论、无 assignee、无 linked PR；open PRs 只有 #371/#367/#362（均无关） |
| Base branch | `dev` @ 547a8eb |

## 需要提交者注意
- **AI 政策**：CONTRIBUTING 明确 "AI-assisted contributions are welcome"，并**要求**在 commit 上加 `Co-authored-by:` trailer 声明 AI 参与。所以 patch 里的 commit 带了 `Co-authored-by: Claude <noreply@anthropic.com>`（只有工具名，没有模型名）。请保留它。
- **认领**：CONTRIBUTING 说花超过一小时之前先在 issue 下认领（good first issue 一句话就够），或者把 PR 本身当作 claim（PR 模板里有 "Plan / claim" 一节，已经填好）。两个人做同一个 issue 是允许的。
- PR 发到 **`dev`**，不要发到 `main`。分支名按惯例用 `fix/...`。
- 首次贡献者的 CI 要维护者批准后才会跑。
- 没有 DCO / Signed-off-by 要求。

## 问题理解
`pyrite kb add` 只把 KB 注册到 index 数据库（`kb` 表，source='user'），不写 config.yaml。`get`、`index sync`、`link`、`task` 这些命令通过 `pyrite/cli/context.py` 的 `_init_base()` / `get_config_and_db()` 调用 `db.merge_registered_kbs(config)`，所以能看到这个 KB。但 `search`、`kb validate`、`kb schema show|add-type|remove-type|set`、`schema validate` 直接用 `load_config()`，只认 config.yaml，于是报 `KB_NOT_FOUND`。我按 issue 里的步骤在本地复现了：4 个命令全部 KB_NOT_FOUND，`get` 正常。

## 合理性判断
这是一个真实的 bug。维护者（markramm，项目 BDFL）自己提的 issue，写了验收标准。#245 之前修过同类问题（task 命令，见 `tests/test_task_commands_registered_kbs.py`），`PyriteConfig.all_kbs()` 的 docstring 也明确说要操作所有 KB 的地方就应该包括 DB 注册的 KB。项目经常合并外部 PR（git log 里有 fatihcvs、Shivansh Shukla、Harsh Raj Singhania 等人的提交）。

## 改动
- `pyrite/cli/context.py`：新增共享 helper `with_registered_kbs(config)`。它打开 index DB，执行 `merge_registered_kbs`，关闭 DB，然后返回 config。config.yaml 的优先级不变，因为 `register_db_kbs` 本来就会跳过同名的 KB。它接收一个已经加载好的 config，不自己去 load，这样现有测试里 patch 各模块 `load_config` 的写法都不受影响。
- `search_commands.py`：`search` 改用 `with_registered_kbs(load_config())`。`search --files` 不带 `-k` 时改为遍历 `config.all_kbs()`。
- `kb_commands.py`：`kb validate` 和 `kb schema show/add-type/remove-type/set` 改用这个 helper。`kb validate` 不带名字时改为遍历 `config.all_kbs()`。
- `schema_commands.py`：`schema validate` 改用这个 helper。
- 新增测试 `tests/test_config_only_commands_see_registered_kbs.py`，共 11 个。
- 新增 changelog 片段 `changelog.d/kb-add-config-only-commands.fixed.md`（项目规定不要直接改 CHANGELOG.md）。

## 验证
环境：`uv venv .venv -p 3.12 && uv pip install -e ".[server,cli,dev]"`，加上 `extensions/*` 的 editable 安装。没装 `ai` 和 `semantic` extras（它们会拉 torch）。所有命令都在 `HOME=<tmp>`、`PYRITE_AUTO_EMBED=0`、`HF_HUB_OFFLINE=1` 下跑。

- **red → green**：`pytest tests/test_config_only_commands_see_registered_kbs.py`
  - 修复前（`git stash` 掉 `pyrite/`）：**9 failed, 2 passed**。通过的 2 个是故意写的守护测试：config.yaml 同名 KB 优先、未知 KB 仍然报 KB_NOT_FOUND。
  - 修复后：**11 passed**。
- **按 issue 步骤用真实 CLI 复现**：修复后 `search hello -k notes`、`kb validate notes`、`kb schema show notes`、`schema validate -k notes` 都返回 exit 0；`search hello -k nope` 仍然报 KB_NOT_FOUND（exit 1），而且提示里现在会列出 `notes`。
- `ruff check pyrite/ tests/ extensions/` → All checks passed。`ruff format --check` → 557 files already formatted。
- `scripts/check_import_cycles.py` → No import cycles。`scripts/check_fix_commit_has_tests.py --range origin/dev HEAD` → OK。
- 全量 `pytest tests/ extensions/ -n 4` 在这台共享机器上太慢（约 10 分钟才跑到 3%），我中途停掉了。改跑最大的相关子集：所有 `test_cli*`、`test_search*`、`test_kb*`、`test_schema*`，加上所有引用 `merge_registered_kbs` / `all_kbs` / `with_registered_kbs` / 被 patch 的 `load_config` 名字的测试文件，共 60 个文件 → **1264 passed, 72 skipped, 0 failed**（4 分 25 秒）。skipped 主要是缺 postgres、semantic、ai 这些可选依赖。其余测试文件没有跑。
- 项目自带的 `scripts/verify_red_ci.py --base origin/dev`：9 个 "red without the fix"。2 个 "passes without the fix"，就是上面说的两个守护测试，PR 里已经说明。

## 如何提交
```bash
git clone https://github.com/<you>/pyrite && cd pyrite
git checkout -b fix/kb-add-config-only-commands origin/dev
git am /path/to/0001-fix-config-only-CLI-commands-see-KBs-added-with-pyri.patch
git push -u origin fix/kb-add-config-only-commands
# PR base: pyrite-wiki/pyrite:dev
```

## PR title
fix: config-only CLI commands see KBs added with `pyrite kb add` (#363)

## PR body
```markdown
## Summary
`search -k`, `kb validate`, `kb schema show|add-type|remove-type|set` and `schema validate -k` built their config with a bare `load_config()`, which only knows the KBs in `config.yaml`. That made a KB added with `pyrite kb add` come back as `KB_NOT_FOUND`, even though `get`, `index sync` and `link` accept it, because those merge the DB registry through `pyrite/cli/context.py`.

This PR adds one shared helper, `with_registered_kbs(config)`, to `pyrite/cli/context.py`. It opens the index, runs `db.merge_registered_kbs(config)`, closes the index again, and returns the config. The affected commands now use `config = with_registered_kbs(load_config())`. `config.yaml` KBs still win on a name clash, since `register_db_kbs` already skips names that are in `config.yaml`. The helper takes an already-loaded config instead of loading one itself, so the existing tests that patch each module's `load_config` keep working unchanged.

Two related spots in the same commands now enumerate `config.all_kbs()` instead of `config.knowledge_bases`:
- `kb validate` without a KB name
- `search --files` without `-k`

Otherwise those two would still silently skip `kb add` KBs, which is the case the `all_kbs()` docstring warns about.

Fixes #363

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below; as CONTRIBUTING asks, the commit carries a `Co-authored-by: Claude` trailer. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Plan / claim
This PR is the claim. The plan is one shared helper in `cli/context.py`, used by the seven `load_config()` call sites the issue lists, plus one CLI test per affected command.

## Testing
- [x] New `tests/test_config_only_commands_see_registered_kbs.py` (11 tests). Each test registers a KB only in the database, which is the state `kb add` leaves behind, and runs the real Typer command. Without the fix: 9 failed, 2 passed. With the fix: 11 passed. `python scripts/verify_red_ci.py --base origin/dev` reports the same 9 as "red without the fix".
  - The 2 tests that pass without the fix are deliberate guards: a `config.yaml` KB beats a DB-registered KB of the same name, and an unknown KB still reports `KB_NOT_FOUND`.
- [x] I reproduced the issue's steps with the real CLI (`kb add` + `index sync`). All four commands now return exit 0. `search -k nope` still returns `KB_NOT_FOUND`, and its hint now lists the registered KB.
- [x] `ruff check pyrite/ tests/ extensions/ && ruff format --check pyrite/ tests/ extensions/`: clean.
- [x] `scripts/check_import_cycles.py` and `scripts/check_fix_commit_has_tests.py --range origin/dev HEAD`: OK.
- [ ] `pytest tests/ extensions/ -n auto` (full suite): **not run to completion**. It was too slow on my shared machine. I ran the 60 test files that touch the changed modules or patch these `load_config` names (all `test_cli*`, `test_search*`, `test_kb*`, `test_schema*`, plus every file that references `merge_registered_kbs` / `all_kbs` / the patched names): **1264 passed, 72 skipped, 0 failed**. The run was on Python 3.12 with `.[server,cli,dev]` and all `extensions/*`, without the `ai`/`semantic` extras.
- [x] A `fix:` change includes a test that fails without the fix.
- [ ] Frontend change: n/a

Changelog: `changelog.d/kb-add-config-only-commands.fixed.md`

## Notes for the reviewer
- `kb schema add-type`/`remove-type`/`set` were not in the issue's command list, but they were among the listed line numbers and had the same bug, so this PR fixes them too.
- `kb discover` still uses a bare `load_config()`. It reports `kb.yaml` files found on disk rather than resolving a KB by name, so I left it alone.
```
