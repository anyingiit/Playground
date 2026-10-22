# 435 — tuProlog/2p-kt#947: getArgumentAsTypeRef 回退分支检查请求的参数下标

| 项 | 内容 |
|---|---|
| Issue | https://github.com/tuProlog/2p-kt/issues/947 |
| 层级 | 自由（tuProlog） |
| Labels | bug, good first issue, module::oop-lib。维护者 gciatto 10-04 确认 master 第 124 行仍有该 bug，修法：`ensuringArgumentIsTypeRef(index)`，并为 `new_object/3` 加回归测试。 |
| Base 分支 | `master`（补丁基于 4443ffd） |
| 状态 | ✅ 可提交（复核 PASS） |
| 重复检查 | 2026-10-22：issue 无指派、无关联 PR。开着的 9 个 PR 里没有涉及 #947 或 oop-lib 的；其他 good-first-issue（936/938/939/942/944）已有别人的 PR，所以没选。 |
| AI 政策 | 无限制 |
| CLA/DCO | 无 |
| 同仓库 | 第 4 个：284（#945）、421（#1044）、433（#1005）。建议分开提交，间隔提交 |

## 改动
- `PrimitiveExtensions.kt`：`ensuringArgumentIsTypeRef(1)` 改为 `ensuringArgumentIsTypeRef(index)`。
- `TestOOPLib.kt`：新增 `typeErrorsOfNewObjectBlameTheTypeArgument`，测试 `new_object(foo(1), [], L)` 抛出 TypeError，期望类型 TYPE_REFERENCE，culprit 为 `foo(1)`。

## 验证
- 红：只回退 main 代码，`:oop-lib:jvmTest --tests '*TestOOPLib*'` 8 个测试中 1 个失败，报 `expected:<foo(1)> but was:<[]>`。
- 绿：`:oop-lib:jvmTest :oop-lib:ktlintCheck :oop-lib:detektAll --continue` BUILD SUCCESSFUL，56 个测试，6 个 skipped，0 失败。
- 补充：`new_object/3` 先执行 `ensuringArgumentIsList(1)`，所以 issue 里提到的"静默失败"在 new_object/3 中实际不会发生，PR 正文只写了报错指向错误参数这一点。
- 未跑 jsTest。

## 如何提交
```
git clone https://github.com/tuProlog/2p-kt && cd 2p-kt && git checkout -b fix-type-ref-index origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 新克隆的 origin/master 仍为 4443ffd，`git am` 能干净应用。修法与维护者确认的方案一致。
- oop-lib 里其他硬编码下标都检查过：Cast.kt 用 1、Type.kt 用 0/1，都与参数位置对应，没有同类 bug。
- 新测试同时断言 expectedType 和 culprit，确实能抓到这个 bug。
- 绿：56 个测试，6 个 skipped，0 失败；ktlint 和 detekt 通过。
- 红：TestOOPLib 8 个测试中 1 个失败，报 `expected:<foo(1)> but was:<[]>`。
- PR 正文的技术描述已全部核实；`new_object/3` 先执行 `ensuringArgumentIsList(1)` 属实。
- 无竞争 PR，无人指派。
- 复核建议把 "1st argument" 改成 "argument index 1"，已采纳。
- 结论：PASS
