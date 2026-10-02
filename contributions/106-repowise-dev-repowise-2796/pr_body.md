## Summary

- `_GO_CALL_DECL` now skips an optional type-argument list between the target and its `(`. It uses the same two-level bounded bracket group as `_GO_FIELD_END`, so `x := New[T](cfg)`, `x, err := pkg.New[K, V](a, b)` and `x := New[map[string]int](cfg)` now produce a `CallAssignment`, the same as `x := New(cfg)`. The whole-right-hand-side check in `scan_call_assignments` is unchanged: `New[T]().Child()` and `Count[T](xs) + 1` are still refused.
- `queries/go.scm`: the regex alone was not enough for the reproduction in the issue. tree-sitter-go cannot tell `New[T](x)` from a conversion to a generic type (it parses it as `type_conversion_expression` → `generic_type`), and it parses `New[T]()` as a call through an `index_expression`. Neither shape produced a `CallSite`, so the resolver had no call to read `New`'s return type from, and `x.Scan()` still got no edge. Four patterns now capture those shapes, bare and `pkg.`-qualified. For the index shape only an index that can be a type argument (`T`, `pkg.T`, `*T`) counts, so `fns[0]()` or `handlers["a"](req)` still produce no call site. `handlers[k]()` with an identifier index is indistinguishable from `New[T]()` in the grammar and is captured as a call to `handlers`; that can only add an edge if a function with that name is in scope. The multi-argument shape `New[K, V](a, b)` is already a `call_expression` and was already captured. A real conversion `List[int](x)` reaches the resolver as a call to the type, just like `T(x)` does today.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related Issues

Fixes #2796

## Test Plan

- [x] Tests pass (`pytest`)
  - New: `TestGoCallAssignments` (generic, qualified with two type arguments, nested `map[string]int` across lines, still refused inside an expression, an index expression is not a call), `TestGoCallTypedLocal::test_a_generic_constructor_result_types_its_receiver` (zero, one and two arguments, end to end: `d := detect.NewOf[int](1); d.Scan()` resolves to `Detector::Scan`), and `TestGoGenericCall` in `test_go_extractors.py` (each grammar shape, including `New[*T]()` and `pkg.New[pkg.T]()`, yields one `New` call site with the right receiver; a call through a literal or computed index such as `fns[0]()` yields none).
  - 12 of the new cases fail on `main` and pass with this change. The other cases pass on both and guard existing behavior. I also checked that the regex change alone still leaves the end-to-end test red, which is why `go.scm` is part of this PR.
  - `pytest tests/unit/ingestion`: 4092 passed, 2 failed (the two `test_git_commit_rows_integration` failures described below).
  - `pytest tests/providers/ tests/unit/` (run before the index-shape narrowing above, which only touches `go.scm`): 25371 passed. 7 failures are unrelated to this change. Six of them (git-history and file-permission tests in `test_change_risk`, `test_security_gate`, `test_update_git_tier`, `test_git_commit_rows_integration` and `test_repo_config_errors`) fail the same way on `main` in my environment, which runs as root with commit signing enabled in the global git config. `test_procutils::test_process_name_of_child_is_python` fails only in the full run, because the process is named `pytest`, and passes when run on its own.
- [x] Lint passes (`ruff check .`)
- [ ] Web build passes (`npm run build`) *(if frontend changes)*: n/a, no frontend changes

## Checklist

- [x] My code follows the project's code style
- [x] I have added tests for new functionality
- [x] All existing tests still pass
- [x] I have updated documentation if needed (n/a; the code comments on `_GO_CALL_DECL` and in `go.scm` describe the new shapes)
