# NLog/NLog #5916 — Enable Dotnet Code Analysis by default

| 项 | 值 |
|---|---|
| Issue | https://github.com/NLog/NLog/issues/5916 |
| Tier | 高星 |
| Labels | refactoring, up-for-grabs |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=5916` 0 结果；关键词 "analyzers" 搜索无相关 PR；issue 无 assignee、无评论；dev 上 `.editorconfig`/csproj 均未启用 EnableNETAnalyzers |
| Base | `dev` @ 91217eff（2026-09-27，NLog 默认分支是 dev） |

## 问题理解
维护者 snakefoot 提议在 NLog 启用 .NET 内置代码分析（`EnableNETAnalyzers` + `AnalysisLevel=latest` + `AnalysisMode=recommended`），并在 `.editorconfig` 里调整部分规则的严重级别（issue 给了 CA1001/CA1848/CA1707/IDE0130 四个例子）。

## 合理性判断
- issue 由维护者本人开出，标签 up-for-grabs，明确欢迎外部贡献。
- src 下 6 个项目都开了 `TreatWarningsAsErrors`，直接开启分析器会让构建失败（src/NLog 464 个 error），所以必须同时调整 severity，这正是 issue 要求的内容。
- 仓库没有 AI 政策（CONTRIBUTING.md、.github、labels 都查过），不需要 DCO，也没有 PR 模板。

## 改动
- 6 个 `src/*/*.csproj`：在 `TreatWarningsAsErrors` 后加 `EnableNETAnalyzers`/`AnalysisLevel latest`/`AnalysisMode Recommended`（沿用逐项目配置的风格，仓库没有 Directory.Build.props）。
- `.editorconfig` 的 `[*.{cs,vb}]` 段：
  - issue 中的 4 条；
  - 公共 API 命名/设计规则（改了就是破坏性变更）：CA1000/CA1069/CA1710/CA1711/CA1716 设为 none，CA1067/CA1068/CA1725 设为 suggestion；
  - 建议使用的 API 在 net35/netstandard2.0 上不存在：CA1840/CA1858/CA1865/CA2249/CA2263 设为 suggestion；
  - 其他代码质量规则先设为 suggestion，以后可以逐条修复：CA1305/CA1309/CA1806/CA1822/CA1830/CA1838/CA1859/CA1861/CA2101/CA2208。
- 没有改任何 .cs 源码。测试项目没有加（没开 TreatWarningsAsErrors，开启后会多出约 1000 条 warning），PR 里写明可以后续再加。

## 验证（.NET SDK 10.0.401，通过 dotnet-install.sh 安装到 /home/user/work/dotnet）
- Base：`dotnet build src/NLog/NLog.csproj -c Release` → 0 error，2 个 NETSDK1210 warning（SDK 自带的提示，base 上就有）。
- Red（只改 csproj、不改 .editorconfig）：`dotnet build src/{NLog,NLog.RegEx,NLog.Targets.AtomicFile}/... -c Release --no-incremental` → Build FAILED，464 Error(s)。
- Green：6 个 src 项目都执行 `dotnet build src/<p>/<p>.csproj -c Release -m:2 --no-incremental` → exit 0，0 error，只剩 NETSDK1210。src/NLog 用 build.ps1 的 TFM 组合 `-p:TargetFrameworks="net46;net45;net35;netstandard2.0;netstandard2.1"` 构建也是 0 error。
- `dotnet test tests/NLog.UnitTests/ --framework net10.0 --configuration release`（即 run-tests.ps1 的 Linux 路径）→ Passed 2970 / Skipped 8 / Failed 0。
- 独立复核（reviewer，全新 clone + git am，同一 SDK）：patch 干净应用；red 464 error（GZipFile 362、WindowsEventLog 252，均因先构建 NLog 失败）；green 6 个项目 0 error；去掉 CA2101/CA2263 后 AtomicFile/RegEx 会报错，证明这两条是必需的；单元测试 2970/8/0 一致。
- 没有运行：Windows 专用的 CheckSourceCode、net462/net35/net45 测试、build.ps1 打包（本环境是 Linux）。

## 需要提交者注意
- 无 AI 政策、无 DCO、无 PR 模板；CHANGELOG 和 PackageReleaseNotes 由维护者在发版时更新，PR 里不用改。
- 这个 PR 主要是在调规则的严重级别。维护者可能更希望修掉一部分规则，而不是降为 suggestion（src/NLog 各 TFM 累计：CA1305 56 条、CA2249 28 条、CA1859 37 条）。如果 review 里这样要求，可以按规则拆成后续 PR。
- AppVeyor 的 Windows 镜像是 VS 2026，`AnalysisLevel=latest` 会跟随该 SDK。如果它的 SDK 比 10.0.401 新，可能会多出新规则，请留意 CI 结果。
- `.editorconfig` 原文件末尾没有换行，补丁补上了换行（diff 中显示 1 行删除）；行尾沿用原来的 LF。

## 如何提交
```bash
git clone https://github.com/NLog/NLog && cd NLog
git checkout -b build/enable-net-analyzers origin/dev
git am /home/user/Playground/contributions/701-NLog-NLog-5916/0001-Enable-.NET-code-analysis-with-AnalysisMode-Recommen.patch
dotnet build src/NLog/NLog.csproj -c Release && dotnet test tests/NLog.UnitTests/ -f net10.0 -c release
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/701-NLog-NLog-5916 NLog/NLog dev build/enable-net-analyzers contributions/701-NLog-NLog-5916/pr_title.txt contributions/701-NLog-NLog-5916/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
