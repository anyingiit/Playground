# dotnet/machinelearning#6820 — DataFrame ElementwiseEquals/NotEquals ignore nulls

| 项 | 值 |
|---|---|
| Issue | https://github.com/dotnet/machinelearning/issues/6820 |
| Tier | 高星 |
| Labels | area-DataFrame, bug, help wanted（"[up-for-grabs] Good issue for external contributors"）, yellow（"maintenance only"） |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Base | `main` @ 681cfb6bed71678bdf248220db3e92ee5eba56f3 (2026-09-30) |
| Duplicate-PR check | 2026-10-01：issue open、0 评论、无 assignee、Development 无关联 PR；`pulls?q=6820` 无相关 PR；关键词 `ElementwiseEquals` → #6869（性能优化，已合并）、#6834（类型转换，已合并）、#6831（DateTime，已关闭），`Elementwise null` → #6723（按 null 过滤，已合并）——均未修复本问题；当前 main 代码仍有该 bug（红测试证实） |

## 问题理解

`PrimitiveDataFrameColumn<T>` 的 null 用 validity bitmap 表示，数值缓冲区里存 `default(T)`。比较运算（`PrimitiveColumnContainer<T>.HandleOperation(ComparisonOperation, ...)`）只比较原始缓冲区值、完全忽略 bitmap，因此 `0 == null` 得到 `true`、`0 != null` 得到 `false`（issue 自带的失败单测）。列-列、列-标量、不同类型（经 Clone 转换）的所有重载最终都汇聚到这两个 container 方法。

## 合理性判断

- 维护方标了 `bug` + `help wanted`（"Good issue for external contributors"），issue 自带失败测试，语义明确。
- 选择的语义与库内既有约定一致：`ElementwiseEquals(null)` 已等价于 `ElementwiseIsNull()`；`StringDataFrameColumn` 中 null == null 为 true。故：null==null → true，null==值 → false，NotEquals 取反。
- `>`/`<` 等排序比较遇到 null 应返回什么属于设计问题（issue 正文只举 Equals/NotEquals），本补丁不改，在 PR 中说明并请维护者指示。
- AI 政策：仓库有 `.github/copilot-instructions.md`、`.github/agents/*`、`.github/skills/*`，积极使用 AI agent；CONTRIBUTING / 标签说明里没有 AI 禁令。PR 需关联 issue、包含测试（根目录 `PULL_REQUEST_TEMPLATE.md`，pr_body 的 Checklist 已按其 4 项填写），首次贡献需签 CLA（机器人提示）。

## 改动

- `src/Microsoft.Data.Analysis/PrimitiveColumnContainer.BinaryOperations.cs`：两个 `HandleOperation(ComparisonOperation, ...)` 在矢量化比较后调用新的私有方法 `ApplyNullEqualitySemantics`。仅对 Equals/NotEquals 生效；两侧都无 null 时直接返回（无性能损失）；否则逐 buffer 读 validity，对任一侧为 null 的行按有效性写结果。标量重载传 `right = null`（标量本身非 null；`ElementwiseEquals(null)` 走既有的 `ElementwiseIsNull` 路径）。
- `test/Microsoft.Data.Analysis.Tests/PrimitiveDataFrameColumnTests.cs`：新增 3 个测试：`TestElementwiseEqualsWithNulls`（issue 场景 + null/null + NotEquals + 结果 NullCount==0）、`TestElementwiseEqualsWithNullsAndDifferentColumnTypes`（int vs double）、`TestElementwiseEqualsScalarWithNulls`（列 vs 标量 0 / 0.0）。

## 验证

环境：.NET SDK `11.0.100-rc.1.26420.103`（global.json 指定）+ .NET 8.0.16 runtime（Linux 上测试只跑 net8.0），装在 `/home/user/work/.tools/dotnet`；只构建 DataFrame 及其测试项目。

| 命令 | 结果 |
|---|---|
| `dotnet build test/Microsoft.Data.Analysis.Tests/Microsoft.Data.Analysis.Tests.csproj -m:2` | Build succeeded, 0 warnings, 0 errors |
| 回退 `src/`（`git stash push src/`）后 `dotnet test test/Microsoft.Data.Analysis.Tests/... --filter "FullyQualifiedName~ElementwiseEquals"` | **Failed: 3**, Passed: 22 → red（3 个新测试全部失败） |
| 打补丁后同一命令 | Passed: 25, Failed: 0 → green |
| 打补丁后全量 `dotnet test test/Microsoft.Data.Analysis.Tests/Microsoft.Data.Analysis.Tests.csproj -m:2` | Passed: 491, Failed: 0, Skipped: 0 (net8.0) |
| `dotnet format <test csproj> --no-restore --verify-no-changes --include <两个改动文件>`；`dotnet format src/Microsoft.Data.Analysis/... --verify-no-changes --include <src 文件>` | exit 0（无需格式化） |
| `git diff --check` | 无空白问题 |

独立复核（2026-10-01 20:35 UTC）：重新执行上表红→绿（回退 src 后 3 failed / 22 passed；恢复后 25 passed）、全量 491 passed、dotnet format exit 0，结果一致；upstream main 已前进到 5a44dfd，但 DataFrame 目录无改动，补丁可无冲突应用；issue 仍 open、无关联 PR。

未运行：Windows 上的 net48/net9.0 目标、整仓 `./build.sh`（含 native/其他 ML 项目，与本改动无关且很重）。

## 如何提交

```bash
git clone https://github.com/dotnet/machinelearning && cd machinelearning
git checkout -b fix-dataframe-elementwise-equals-nulls origin/main
git am /path/to/0001-Respect-null-values-in-DataFrame-ElementwiseEquals-E.patch
git push <your-fork> fix-dataframe-elementwise-equals-nulls   # PR 目标分支: main
# PR 标题见 pr_title.txt，正文见 pr_body.md
```

## 需要提交者注意

- 首次向 dotnet 组织提交需按 dotnet-policy-service 机器人提示签 CLA；无 DCO、无 changelog 要求。合并时会 squash。
- 提交信息为普通英文句子（仓库无 Conventional Commits），结尾 `Fixes #6820`（仓库 PR 模板推荐 `Fixes #nnnn`，故 pr_body 也用 Fixes 而非 Closes，效果相同）。
- PR 正文里提出了 `>`/`<` 对 null 的语义问题，维护者若希望一并处理可追加提交。
- 标签 `yellow` = "maintenance only"（该区域处于维护模式），bug 修复属于范围内，但审阅可能较慢。
