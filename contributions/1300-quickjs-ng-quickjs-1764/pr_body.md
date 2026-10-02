## Description

`Function.prototype.apply`, `Reflect.apply` and `Reflect.construct` build their argument list in
`build_arg_list()`, which read the array-like's `length` with `js_get_length32()` (ToUint32). A negative
length such as `-1` therefore wrapped around to `2^32 - 1` and threw
`RangeError: too many arguments in function call (only 65535 allowed)`:

```js
(function () { return arguments.length; }).apply(null, { length: -1 }); // RangeError, expected 0
```

The spec's CreateListFromArrayLike uses LengthOfArrayLike, i.e. ToLength, which clamps negative values
to `+0`. This change switches `build_arg_list()` to `js_get_length64()` (ToLength) and does the
`JS_MAX_LOCAL_VARS` check on the 64-bit value before narrowing. As a side effect, lengths `>= 2^32` are no
longer truncated modulo 2^32 (e.g. `{ length: 2 ** 32 + 1 }` used to produce a single argument; it now
throws the existing "too many arguments" RangeError, like other engines throw for an oversized list).

Regression tests are added to `test_function()` in `tests/test_builtin.js` (negative / `-Infinity` /
`-4294967295` lengths via `apply`, `Reflect.apply` and `Reflect.construct`, plus the `2 ** 32 + 1` case).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1764

## Checklist

- [x] Tests pass locally — cmake Release build of `qjs_exe` + `run-test262`; `run-test262 -c tests.conf` (what `make test` runs): exit 0, 0/118 errors. Without the `quickjs.c` change the new test fails with `tests/test_builtin.js:150: RangeError: too many arguments in function call`. test262 subsets at the pinned submodule commit (`run-test262 -c test262.conf -a -d ...`): `built-ins/Function/prototype/apply` 0/88, `built-ins/Reflect` 0/306, `language/expressions/call` 0/165 errors.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [ ] Documentation is updated (if applicable) — n/a, spec-conformance bug fix
