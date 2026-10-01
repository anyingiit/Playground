## 📌 What Does This PR Do?

Fixes `align-parameters` inserting the alignment padding between the variadic operator (`...`) / by-reference sigil (`&`) and the parameter variable.

## 🔍 Context & Motivation

With `align-parameters = true`, this:

```php
public function __construct(
    public readonly int $priority = 0,
    string ...$renders,
) {}
```

was formatted as `string ...          $renders`, which violates PSR-12 ("There MUST NOT be a space between the variadic three dot operator and the argument name"). The same happened for `&$param`.

Root cause: in the `FunctionLikeParameter` formatter, the `IfBreak` padding was pushed *after* `&`/`...` and right before the variable. The prefix width already accounts for `&`/`...`, so moving the padding in front of them keeps the variable names (`$`) aligned while the sigils stay attached:

```php
public function __construct(
    public readonly int $priority = 0,
    string           ...$renders,
) {}
```

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## 🛠️ Summary of Changes

- **Bug Fix:** `align-parameters` no longer separates `...` / `&` from the parameter variable.
- **Tests:** new formatter case `align_parameters_variadic_and_by_reference` (variadic, by-reference, by-reference variadic, untyped variadic). It fails without the fix and passes with it.

## 📂 Affected Areas

- [ ] Linter
- [x] Formatter
- [ ] Analyzer
- [ ] CLI
- [ ] Dependencies
- [ ] Documentation
- [ ] Other (please specify):

## 🔗 Related Issues or PRs

Closes #2182 (originally reported in discussion #2153)

## 📝 Notes for Reviewers

An alternative would be to align `...$renders` so that it *starts* at the variable column (excluding the sigils from the prefix width). I went with keeping the `$` column aligned because the option is documented as "align by the variable"; happy to switch if you prefer the other style.

Checklist:

- [x] Tests pass locally: `cargo test -p mago-formatter --locked` (469 + 53 passed); new case red without the fix, green with it
- [x] `cargo fmt --all -- --check` and `cargo clippy -p mago-formatter --all-targets --all-features -- -D warnings` clean
- [ ] `CHANGELOG.md` — n/a (repo has no changelog file)
- [ ] Documentation — n/a (behaviour fix only)
