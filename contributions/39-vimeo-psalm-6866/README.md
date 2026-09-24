# vimeo/psalm #6866 — `implode(<non-empty-string>, non-empty-list<string>)` wrongly inferred as `non-empty-string`

| 项 | 值 |
|---|---|
| Issue | https://github.com/vimeo/psalm/issues/6866 |
| Tier | 自由 |
| Labels | Help wanted, bug, easy problems, good first issue, internal stubs/callmap |
| Status | ✅ ready — patch + PR text done (2026-09-24) |
| Duplicate-PR check | `is:pr 6866` → 0; `is:pr is:open implode` → 0; issue open, unassigned, no linked PR/branch (re-checked right before finishing). Old related PRs #7967 / #8595 (2022) are closed and dealt with other implode cases. |
| Base | `master` @ 79465b8 (2026-09-23) |
| Patch | `0001-Don-t-infer-non-empty-string-for-implode-of-possibly.patch` |

## 问题理解
`implode('asdf', [''])` 的结果是 `''`，但 Psalm 推断为 `non-empty-string`（literal 情况下为 `non-empty-literal-string`）。
原因在 `stubs/CoreGenericFunctions.phpstub` 的 `implode`（及别名 `join`）条件返回类型：只要 separator 是 non-empty-string 且数组 non-empty，就认为结果非空。
但数组只有一个元素时结果就是该元素本身，元素可能为 `''`、`null`、`false` 或 `__toString()` 返回 `''` 的对象。
维护者 orklah 在 issue 下建议“在 stub 里加一层嵌套条件”；报告者 2022 年再次遇到。master 上 stub 仍未变化，问题依旧。

## 合理性判断
- 这是类型推断的 soundness bug（会导致误报 RedundantCondition / DocblockTypeContradiction），维护者已标 bug + good first issue + easy problems，并给出了修法方向。
- 仓库非常活跃（danog 维护，2026-09 仍在合并外部贡献者 PR：yuriy-sorokin、janedbal、Portll、Eljees 等）。
- AI 政策：CONTRIBUTING.md、docs/contributing/*、.github/ 下均无 AI/LLM 相关规定。

## 改动
- `stubs/CoreGenericFunctions.phpstub`（`implode` 和 `join` 两处相同改动）：separator 非空且数组非空时，
  - 仅当元素类型为 `non-empty-string|int|float`（int/float 转字符串必非空）才推断 `non-empty-string` / `non-empty-literal-string`（literal 分支改为 `array<non-empty-literal-string|literal-int>`）；
  - 否则回落为 `literal-string`（元素与 separator 都是 literal 时，保留 literal 性）或 `string`。
  - separator 为空串的分支原本就正确，未改。
- `tests/ArrayFunctionCallTest.php`：新增 `implodeNonEmptySeparatorAndPossiblyEmptyElements`（`[""]`、`["a", ""]`、`non-empty-list<string>`、非 literal separator、`non-empty-list<non-empty-string>`、`non-empty-list<int>`、`non-empty-list<?string>`、`join()`）。

## 验证
环境：PHP 8.4.19，`composer install`（CI 用同样命令）。机器被多个 agent 共享（load avg 10–17），全量 205 个测试文件串行跑需要数小时，因此跑的是相关子集 + 自分析。
- Red（未修复，stub 还原）：`php vendor/bin/phpunit tests/ArrayFunctionCallTest.php --filter implode` → 6 tests, **1 failure**（$a/$b = non-empty-literal-string，$c/$d/$g/$h = non-empty-string）
- Green（修复后）：同命令 → OK (6 tests, 7 assertions)
- 所有使用 `implode(`/`join(` 的测试文件（14 个，按 CI 的方式每个文件单独 `php -d zend.assertions=1 -d assert.exception=1 vendor/phpunit/phpunit/phpunit <file>`）全部通过：
  ArrayFunctionCallTest 261 tests OK (2 skipped) · AttributeTest 57 OK · Config/ConfigTest 48 OK · ConstantTest 138 OK · DocumentationTest 351 OK · ImmutableAnnotationTest 36 OK · ReturnTypeProvider/{Basename,Dirname,Sprintf}Test 4/6/52 OK · StubTest 35 OK · TaintTest 200 OK · ToStringTest 39 OK · UnusedVariableTest 293 OK (6 skipped) · HackConformanceTest 7 skipped（需要 docker，CI 中是单独 job）
- Psalm 自分析（CI 的 `composer psalm` 步骤）：`php ./psalm --threads=2 --no-cache` → **No errors found!**（验证 stub 改动不会在 Psalm 自身代码中引入新错误）
- `vendor/bin/phpcs -ps tests/ArrayFunctionCallTest.php` → 无问题；`parallel-lint` → No syntax error
- 未运行：其余 ~190 个测试文件（与 implode stub 无关；CI 会跑）。注：`composer phpunit` 脚本本身在 master 上已坏（paratest 报 “functional option is not supported in WrapperRunner”），与本改动无关，CI 用的是 `bin/ci/tests-github-actions.sh`。

## 如何提交
```bash
git clone https://github.com/vimeo/psalm.git && cd psalm
git checkout -b fix/6866-implode-possibly-empty-elements origin/master
git am /path/to/0001-Don-t-infer-non-empty-string-for-implode-of-possibly.patch
git push <your-fork> fix/6866-implode-possibly-empty-elements
# open PR against vimeo/psalm master
```

## 需要提交者注意
- 仓库无 PR 模板、无 CHANGELOG 文件（release notes 由标签生成），无 DCO 要求；也没有 AI 政策。
- 这是一个“精度 vs 正确性”取舍：`implode(',', $list_of_plain_strings)` 现在推断为 `string` 而不是 `non-empty-string`。这正是 issue 要求的 soundness 修复，但维护者可能希望针对 6.x 分支或讨论。若维护者要求，可改成 base `6.x`（stub 在 6.x 上应可直接 cherry-pick，未验证）。

---

## PR title
```
Don't infer non-empty-string for implode() of possibly-empty elements
```

## PR body
```markdown
## Description

`implode()` / `join()` with a non-empty separator and a non-empty array was always inferred as `non-empty-string` (or `non-empty-literal-string`), but a single element that stringifies to `''` makes the result empty: `implode(':', [''])`, `implode(':', [null])`, or a `Stringable` returning `''`. The stub's conditional return type only looked at the separator and at the array being non-empty.

Following orklah's suggestion in the issue, this adds a nested conditional to the stub: with a non-empty separator and a non-empty array, the result is `non-empty-string` only when every element is guaranteed to stringify to a non-empty value (`non-empty-string`, `int` or `float`); literal inputs keep `non-empty-literal-string`. Otherwise it falls back to `literal-string` (literal separator + literal elements) or `string`. The empty-separator branch was already correct and is unchanged.

Trade-off worth mentioning: `implode(',', $nonEmptyListOfString)` is now `string` rather than `non-empty-string`, which is the sound answer since the list may be `['']`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #6866

## Checklist

- [x] Tests pass locally
  - New `ArrayFunctionCallTest` case `implodeNonEmptySeparatorAndPossiblyEmptyElements` fails on master (inferred `non-empty-(literal-)string`) and passes with the fix
  - Every test file that uses `implode(`/`join(` (14 files incl. ArrayFunctionCallTest, TaintTest, DocumentationTest, UnusedVariableTest, ToStringTest, StubTest, ConfigTest) passes with `vendor/phpunit/phpunit/phpunit <file>`
  - `./psalm --no-cache` self-analysis: No errors found
  - `phpcs` / `parallel-lint` clean on the changed test file
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes are generated)
- [ ] Documentation is updated (if applicable) — n/a (documented `implode` literal-string examples still hold)
```
