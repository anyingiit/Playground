# repowise-dev/repowise #2796 — A generic constructor call (`x := New[T](...)`) leaves its local untyped in Go

| 项 | 值 |
|---|---|
| Issue | https://github.com/repowise-dev/repowise/issues/2796 |
| Tier | 新锐 |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=2796` 0 结果；open PR 中无 Go 泛型/`_GO_CALL_DECL` 相关；issue 无 assignee、无评论、无 linked PR。复审时（同日）再次确认：仍为 0 结果、无评论。 |
| Base | `main` @ 14ff7670（2026-10-01）；复审时 upstream main 已到 57aaafe，patch 仍可 `git am`，相关测试 259 passed |

## 问题理解
`receiver_types.py` 的 `_GO_CALL_DECL` 要求 target 名后紧跟 `\s*\(`。泛型调用 `New[T](...)` 中间多了 `[...]` 类型实参，所以局部变量拿不到类型，后面的 `x.Scan()` 也就没有边。issue 的建议是沿用 `_GO_FIELD_END` 的两层嵌套有界方括号组。

## 合理性判断
- issue 带 bug + good first issue 标签，issue 里给出了根因、修法和验收标准。验收标准写明“泛型局部变量上的方法调用能正确解析”。
- **只改正则不够**（实测后发现）：tree-sitter-go 无法区分 `New[T](x)` 和泛型类型转换，把它解析成 `type_conversion_expression → generic_type`；`New[T]()` 则被解析成通过 `index_expression` 的调用。这两种形状原先都不产生 `CallSite`，而 resolver 要靠这个 CallSite 找到 `New` 的返回类型（`call_receiver_typing.py` 按 `(line, receiver, target)` 匹配 CallSite）。所以只改正则时，issue 里的复现（`detect.New[int](cfg)`）仍然是 `[]`。因此在 `queries/go.scm` 里补了 4 个 pattern。多参数的 `New[K, V](a, b)` 本来就是 `call_expression`，原先已经能捕获。
- 副作用评估：真正的泛型类型转换 `List[int](x)` 会作为一次对类型 `List` 的调用进入 resolver，这和现有的 `T(x)` 处理方式一致（`call_receiver_typing.py::_returned_type_id` 中 `symbol.kind in _TYPE_KINDS` 分支注释为 “a conversion”）。`handlers[k]()`、`fns[i](x)` 这类以标识符为下标、通过索引调用函数值的写法，在语法上和 `New[T]()` / `New[T](x)` 完全无法区分，会产生 target 为 `handlers`/`fns` 的 CallSite。复审实测：若被导入的包里恰好有同名函数（哪怕未导出），resolver 会经 `import_merged` 连出一条错误的边。因此复审把 index 形状收窄为下标只能是类型实参可能的形状（`identifier`、`selector_expression`、`*T`），`fns[0]()`、`handlers["a"](req)`、`fns[i+1]()` 不再产生 CallSite（新增测试守护）。剩余风险只在下标是单个标识符时存在，属于语法本身的歧义，PR 里已说明。

## 改动
- `packages/core/src/repowise/core/ingestion/languages/receiver_types.py`：`_GO_CALL_DECL` 在 target 与 `\s*\(` 之间加入可选的 `(?:\[(?:[^\[\]\n]|\[[^\[\]\n]*\])*\])?`，与 `_GO_FIELD_END` 相同。`match.end()` 仍然落在 `(` 之后，所以 `scan_call_assignments` 的 `_call_end` 和“整个右侧就是这个调用”的检查不受影响（有测试覆盖 `New[T]().Child()` 和 `Count[T](xs) + 1` 仍被拒绝）。另外加了注释。
- `packages/core/src/repowise/core/ingestion/queries/go.scm`：新增 4 个 call pattern：`type_conversion_expression`/`generic_type`（裸名，以及 `qualified_type` 带 `@call.receiver` 的形式），以及 `call_expression` + `index_expression`（裸名和 `pkg.` 两种；`index` 限定为 `identifier` / `selector_expression` / `*T` 形式的 `unary_expression`）。
- 测试：
  - `tests/unit/ingestion/test_receiver_types.py::TestGoCallAssignments` 新增 5 个用例：`x := New[T](cfg)`；`c, err := cache.New[K, V](size)`；嵌套 `New[map[string]int](` 跨行参数；`New[T]().Child()` / `Count[T](xs) + 1` 仍被拒绝；`xs[i]` / `m[k].f` 不算调用（非泛型行为不变）。
  - `tests/unit/ingestion/test_call_resolver_strategies.py::TestGoCallTypedLocal::test_a_generic_constructor_result_types_its_receiver`，参数化 0/1/2 个实参三种情况，端到端验证 `d := detect.NewOf[...](...); d.Scan()` → `Detector::Scan`。夹具 `_GO_DETECT` 加了 `func NewOf[T any](v ...T) *Detector`。
  - `tests/unit/ingestion/test_go_extractors.py::TestGoGenericCall`：`test_generic_call_site_is_captured` 9 个参数化用例（含复审补充的 `New[*T]()`、`pkg.New[pkg.T]()`），检查每种语法形状都只产生一个 `New` CallSite，并且 receiver 正确；`test_a_call_through_a_value_index_names_no_function` 3 个用例（`fns[0]()`、`handlers["a"](req)`、`fns[i+1]()`）确认按值下标调用不产生 CallSite。

## 验证
环境：`uv sync --all-packages`（Python 3.11.15），工作目录 `/home/user/work/repowise`，分支 `fix/go-generic-call-decl`。
- **Red**：`git stash push -- packages` 只还原实现，保留测试后运行
  `uv run pytest -q tests/unit/ingestion/test_go_extractors.py tests/unit/ingestion/test_receiver_types.py tests/unit/ingestion/test_call_resolver_strategies.py`
  → 复审后为 `12 failed, 247 passed`（初版为 11 failed）。失败的是 6 个 `TestGoGenericCall` 捕获用例（多参数 `New[K, V]` 两种和 `pkg.New[pkg.T]()` 在 base 上本来就过）、3 个 `TestGoCallAssignments` 和 3 个端到端用例。按值下标的 3 个守护用例在 base 上通过；用初版未收窄的 go.scm 跑则 3 个全红，收窄后转绿。
- 中间验证：只改正则、不改 go.scm 时，端到端用例仍然失败（`[] == ['detect/detect.go::Detector::Scan']`）。这证明 go.scm 的改动是必要的。
- **Green**：同一命令 `259 passed`。复审又跑了整个 `tests/unit/ingestion`：`4092 passed, 2 failed`（两个都是 `test_git_commit_rows_integration`，下面说明的环境问题）。`tests/unit/ingestion/test_go_range_receivers.py` 也通过。
- `uv run ruff check .` → All checks passed!（按仓库要求**没有**运行 `ruff format .`）
- 完整套件 `uv run pytest -q tests/providers/ tests/unit/`（25401 个用例）：`7 failed, 25371 passed, 19 skipped, 4 xfailed`（耗时 53 分钟）。7 个失败都与本改动无关：
  - 6 个是 git 相关测试（`test_change_risk::test_author_experience_accrues`、`test_security_gate::test_a_submodule_in_the_change_is_skipped_not_fatal`、`test_update_git_tier::test_essential_tier_update_never_blames`、`test_git_commit_rows_integration` 的 2 个）和 `test_repo_config_errors::test_unreadable_env_raises_typed_error`。在 `main` 上单独运行同样失败。原因是本环境：全局 git 配置了 `commit.gpgsign`、user，并且以 root 运行，所以“不可读”的文件仍然可读。
  - `test_procutils::test_process_name_of_child_is_python` 只在完整套件中失败（进程名是 `pytest`）。在本分支上单独运行 `tests/unit/test_procutils.py` 时 10 个全部通过，在 base 上单独运行也通过，与改动无关。
- 没有运行：`npm run build`（不涉及前端）。

## 复审记录（独立复审，2026-10-01）
- 复核 red→green：只还原 `packages/` 后 12 failed，恢复后 259 passed；`ruff check .` 通过；新增代码行 `ruff format --diff` 无输出（仓库现有文件本身就不是 ruff format 格式，未格式化整文件）。
- 发现并修复：初版 go.scm 的 `index_expression` pattern 对任意下标都生效，`fns[0]()` / `handlers["a"]()` 会产生以 slice/map 变量名为 target 的 CallSite；探针实测在被导入包中有同名函数时出现错误边（`import_merged`）。已收窄下标形状并加测试，commit 已 amend 并重新导出 patch。
- 作者/提交者均为 anyingiit，patch 中无 AI 模型名；`git apply --check` 在 14ff767 和最新 upstream main 57aaafe 上均通过。
- 完整套件（25371 passed）是初版跑的；复审只改了 go.scm 的两个 pattern 和测试，复跑了整个 `tests/unit/ingestion`。

## 需要提交者注意
- CONTRIBUTING 要求**先在 issue 下评论认领**（评论即锁定），提交 PR 前请先评论 "I'd like to take this"，并确认此前没有其他人认领。
- 没有 AI 政策限制；PR 模板包括 Summary / Related Issues / Test Plan / Checklist，pr_body.md 已按模板填写，并加了 disclosure 段落。
- 不要运行 `ruff format .`（仓库没有用 formatter 统一格式）。
- 改动超出 issue 原本只改正则的范围，额外改了 `go.scm`，原因见上。PR 正文已说明。维护者如果只想改正则，可以拆开，但那样 issue 的验收标准（方法调用能解析）无法达成。
- docs/CHANGELOG.md 由 git-cliff 根据 conventional commits 生成，不需要手动修改。

## 如何提交
```bash
# 先在 https://github.com/repowise-dev/repowise/issues/2796 评论认领
git clone https://github.com/<you>/repowise && cd repowise   # 你的 fork
git remote add upstream https://github.com/repowise-dev/repowise && git fetch upstream
git checkout -b fix/go-generic-call-decl upstream/main
git am /home/user/Playground/contributions/106-repowise-dev-repowise-2796/0001-fix-go-type-a-local-assigned-from-a-generic-construc.patch
uv sync --all-packages && uv run pytest tests/unit/ingestion -q && uv run ruff check .
git push -u origin fix/go-generic-call-decl
gh pr create --repo repowise-dev/repowise --head <you>:fix/go-generic-call-decl --title "$(cat /home/user/Playground/contributions/106-repowise-dev-repowise-2796/pr_title.txt)" --body-file /home/user/Playground/contributions/106-repowise-dev-repowise-2796/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
