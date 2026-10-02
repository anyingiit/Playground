# quickjs-ng/quickjs#1764 — Function.prototype.apply throws RangeError for a negative length

| 项 | 值 |
|---|---|
| Issue | https://github.com/quickjs-ng/quickjs/issues/1764 |
| Tier | 自由 |
| Labels | 无（issue 未打标签） |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Base | `master` @ 6a9b531（2026-10-01 浅克隆） |
| Duplicate-PR check | 2026-10-01 ~22:55 UTC：`pulls?q=1764` 只命中无关的 #1551（arena allocator）；`pulls?q=is:pr apply`、`pulls?q=is:pr length` 均无相关 PR；issue 0 评论、未分配、无关联 PR |

## 问题理解

`build_arg_list()`（`Function.prototype.apply` / `Reflect.apply` / `Reflect.construct` 以及 `OP_apply_eval` 共用）用 `js_get_length32()`（ToUint32）读取类数组的 `length`。`{length:-1}` 被转成 `2^32-1`，超过 `JS_MAX_LOCAL_VARS`（65535）后抛 `RangeError: too many arguments ...`。规范中 CreateListFromArrayLike 使用 LengthOfArrayLike → ToLength，负数应变为 0，所以应返回 0。V8/JSC/SpiderMonkey 等都返回 0。

## 合理性判断

- 明确的规范一致性 bug，issue 中给了规范引用和其他引擎行为；项目以 test262 conformance 为目标，近期有大量类似 conformance 修复被合并（如 #1706 Iterator.from、#1741 String.prototype.repeat）。
- AI 政策：仓库无 CONTRIBUTING/AGENTS.md/CLAUDE.md；`.github/` 仅 workflows 和 dependabot；labels 页无 AI 相关描述；grep LLM/Copilot/AI-generated 只在 docs/projects.md 的第三方项目介绍中出现。无 AI 禁令。

## 改动

- `quickjs.c` `build_arg_list()`：改用 `js_get_length64()`（ToLength），在 int64 上比较 `JS_MAX_LOCAL_VARS` 后再收窄为 `uint32_t`。副作用（也是规范正确行为）：`length >= 2^32` 不再按 2^32 取模截断，而是抛同一个 "too many arguments" RangeError。
- `tests/test_builtin.js` `test_function()`：新增负长度（-1、-Infinity、-4294967295）经 `apply` / `Reflect.apply` / `Reflect.construct` 返回 0 的断言，以及 `2**32+1` 抛 RangeError 的断言。
- 仓库无 CHANGELOG；无 PR 模板；CI 中无 clang-format/lint 步骤。

## 验证

构建：`cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j3 --target qjs_exe run-test262`

| 命令 | 结果 |
|---|---|
| 未修复（仅加测试）`build/run-test262 -c tests.conf -f tests/test_builtin.js` | **exit 1**：`tests/test_builtin.js:150: RangeError: too many arguments in function call (only 65535 allowed)` → red |
| 未修复 `build/run-test262 -c tests.conf`（= `make test`） | exit 1（同上错误） |
| 修复后 `build/run-test262 -c tests.conf -f tests/test_builtin.js` | exit 0 → green |
| 修复后 `build/run-test262 -c tests.conf` | exit 0，`Result: 0/118 errors, 9 excluded` |
| 修复后 test262（submodule 固定提交 5ef1e57，稀疏检出）`build/run-test262 -c test262.conf -a -t 2 -d test262/test/built-ins/Function/prototype/apply` | 0/88 errors |
| 同上 `-d test262/test/built-ins/Reflect` | 0/306 errors |
| 同上 `-d test262/test/language/expressions/call` | 0/165 errors, 6 skipped |
| `build/qjs -e 'print((function(){return arguments.length}).apply(null,{length:-1}))'` | `0` |

未运行：完整 test262（太重）、Windows/其他平台 CI 矩阵。

## 如何提交

```bash
git clone https://github.com/quickjs-ng/quickjs && cd quickjs
git checkout -b fix-apply-negative-length origin/master
git am /path/to/0001-Use-ToLength-in-CreateListFromArrayLike-for-apply.patch
git push <your-fork> fix-apply-negative-length   # PR 目标分支: master
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。参考克隆（含提交）：`/home/user/work/quickjs-ng-quickjs`，分支 `fix-apply-negative-length`。

### 需要提交者注意
- 仓库无 DCO、无 CHANGELOG、无 PR 模板；提交信息为普通英文句子（非 Conventional Commits）。
- 无 AI 政策限制；PR 正文已包含 Claude Code 披露段落。
- 该仓库开放 PR 多、外部修复者活跃 —— 提交前请再查一次 `https://github.com/quickjs-ng/quickjs/pulls?q=1764` 及 issue 评论，避免重复。
- 行为变化：`length >= 2^32` 的类数组以前被截断（如 `2**32+1` → 1 个参数），现在抛 RangeError；PR 描述已说明。
