# pmd/pmd#7100 — [groovy] CPD fails on GStrings that end in an interpolated variable

| Item | Value |
|---|---|
| Issue | https://github.com/pmd/pmd/issues/7100 |
| Repo | pmd/pmd (~5k★, Java, daily commits, maintainers adangel/oowekyala merge outside PRs) |
| Tier | 高活跃高Star |
| Labels | a:bug |
| Status | ✅ ready |
| Duplicate-PR check | 2026-09-24 (start + re-check before finishing): no comments, no assignee, no linked PR; `is:pr 7100` → 0 results; `is:pr groovy` → only dependabot bumps; open PR list has nothing for Groovy/CPD |
| Base | `main` @ 251ef73 |
| Patch | `0001-groovy-Fix-7100-CPD-fails-on-GStrings-ending-in-an-i.patch` |

## 问题理解
`GroovyCpdLexer` 直接使用 `org.apache.groovy.parser.antlr4.GroovyLexer`。Groovy 编译器实际用的是其子类 `GroovyLangLexer`，
它覆盖了 `rollbackOneChar()`；基类在 GString 的 `$name` 路径结束后需要回退一个字符，没有子类时这个字符被吞掉：
- `"$i"` / `"x-$i"`：结束引号被吞 → `LexException: token recognition error`，或抛出 `GroovySyntaxError`（`AssertionError` 子类，绕过 `--no-fail-on-error`）。
- `"x $i y"`：不报错，但后续片段丢了前导空格（现有 `sample.txt`/`cpdoff.txt` 期望文件里 `[is already in the tree"]` 起始列 45 而不是 44，说明这个 bug 早已被“固化”进测试数据）。

Issue 同时询问 CPD 是否应该捕获 `GroovySyntaxError`。

## 合理性判断
明确的 bug（有效 Groovy 代码无法被 CPD 处理），报告人给了根因和建议修法；无 PR、无认领。PMD 的 CONTRIBUTING / `.github` / devdocs 中没有任何 AI 相关政策（grep LLM/AI/Copilot/ChatGPT/generative 无结果）。无 DCO、无 CLA 要求。

## 改动
1. `GroovyCpdLexer`：`new GroovyLexer(...)` → `new GroovyLangLexer(...)`。
2. `GroovyTokenManager`：`lexer.nextToken()` 抛出的 `GroovySyntaxError`（行/列来自异常）转换成 `LexException`，使其和其他词法错误一样被处理（例如 `def a = \`x\`` 或未闭合字符串）。验证过：这两种非法输入在 base 上同样抛 `GroovySyntaxError`，因此是既有问题，不是换 lexer 引入的回归。
3. 测试：新增 `gstrings.groovy/.txt`（issue 里的两例 + `"x $i y"`、`"${i}"`、`"$i.name"`、`"""multi $i"""`）；新增 `testLexerSyntaxErrorIsReportedAsLexException`；更新 `sample.txt`、`cpdoff.txt` 中各 2 行（GString 片段现在正确包含前导空格，列 44）。

## 验证
环境：JDK 21.0.10、Maven 3.9（系统 mvn），`-Dmaven.repo.local=/home/user/work/m2`。
```
mvn -pl pmd-groovy -am install -DskipTests ...            # 构建 pmd-core/pmd-test/pmd-lang-test
# RED：只回退 src/main（保留新测试）
mvn -o -pl pmd-groovy test ...  → Tests run: 4, Failures: 3, Errors: 1
   testGStringsEndingWithInterpolatedVariable: LexException line 2, column 12 token recognition error
   testLexerSyntaxErrorIsReportedAsLexException: GroovySyntaxError Unexpected character: '`'
   testSample / testCpdOffAndOn: 期望文件中的列号（旧行为吞字符）不一致
# GREEN（含仓库 CI 的 checkstyle、PMD、CPD 检查）
mvn -pl pmd-groovy verify -Dmaven.javadoc.skip  → Tests run: 4, Failures: 0, Errors: 0; 0 Checkstyle violations; pmd:check / cpd-check 通过; BUILD SUCCESS
```
未运行：完整 `./mvnw clean verify`（全部 50+ 模块，本机资源不够）。其他模块不依赖 `pmd-groovy` 的代码（仅 `pmd-languages-deps`/根 pom 引用），因此只影响此模块。

## 需要提交者注意
- PR 标题需以 `[groovy]` 前缀（PR 模板要求）。
- `docs/pages/release_notes.md` 未修改：维护者合并时自己维护 “Fixed Issues”（且 adangel 的 #7106 正在改该文件，避免冲突）。如被要求，可在 `* groovy` 下加一行 `* [#7100](https://github.com/pmd/pmd/issues/7100): \[groovy] CPD fails on GStrings that end in an interpolated variable`。
- 无 AI 政策、无 DCO；按惯例保留披露段落即可。

## 如何提交
```bash
git clone https://github.com/<you>/pmd.git && cd pmd
git checkout -b issue-7100-groovy-gstring-lexer origin/main
git am /path/to/0001-groovy-Fix-7100-CPD-fails-on-GStrings-ending-in-an-i.patch
git push -u origin issue-7100-groovy-gstring-lexer   # PR 目标分支：main
```

---

## PR title
`[groovy] Fix #7100: CPD fails on GStrings ending in an interpolated variable`

## PR body
```markdown
## Describe the PR

`GroovyCpdLexer` instantiated `org.apache.groovy.parser.antlr4.GroovyLexer` directly. The Groovy compiler uses its subclass `GroovyLangLexer`, which implements `rollbackOneChar()`; the base lexer needs that after a GString path like `$i`. Without it the character right after the variable is swallowed:

- `"$i"` / `f("x-$i", "y")`: the closing quote is eaten, so lexing fails with a `LexException` or with a `GroovySyntaxError`
- `"x $i y"`: no error, but the next GString part loses its leading space. You can see this in the existing `sample.txt` / `cpdoff.txt` expected files (`is already in the tree"` started at column 45 instead of 44). Those 4 lines are updated here.

Changes:
- `GroovyCpdLexer` now uses `GroovyLangLexer`, as suggested in the issue.
- `GroovyTokenManager` turns a `GroovySyntaxError` thrown by the lexer into a `LexException` with the same line/column. `GroovySyntaxError` extends `AssertionError`, so before this change it wasn't handled like other lexical errors (the issue mentions it bypassing `--no-fail-on-error`). This happens on `main` too for invalid input such as ``def a = `x` `` or an unterminated string.
- New CPD test data `gstrings.groovy` covering the examples from the issue plus `"${i}"`, `"$i.name"` and a triple-quoted GString, and a test for the `LexException` conversion.

I didn't touch `docs/pages/release_notes.md` because I wasn't sure whether you'd prefer to update it yourselves. Happy to add the entry if you want.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issues

- Fix #7100

## Ready?

- [x] Added unit tests for fixed bug/feature (`GroovyCpdLexerTest`: new tests fail on `main`, 4/4 pass with the fix)
- [x] Passing all unit tests (`./mvnw -pl pmd-groovy verify`: tests, checkstyle, PMD and CPD checks pass. The full multi-module build was not run locally)
- [ ] Complete build `./mvnw clean verify` passes (checked automatically by github actions)
- [x] Added (in-code) documentation (if needed): comments at the lexer and at the error conversion
```
