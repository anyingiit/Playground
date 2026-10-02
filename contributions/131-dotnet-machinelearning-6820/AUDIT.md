# Malicious-code audit — dotnet/machinelearning @ 681cfb6

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/machinelearning` (full checkout, 4498 tracked files; 303 text files scanned by the script) plus manual review of MSBuild files on the build/test path.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (npm lifecycle, setup.py, etc.) | none found | n/a |
| Committed binaries | none flagged | n/a |
| `eng/common/darc-init.ps1:24`, `internal-feed-operations.ps1:29`, `tools.ps1:289/520`, `post-build/nuget-verification.ps1:68` (`Invoke-WebRequest`) | Arcade SDK shared scripts (dotnet/arcade) downloading darc / credential provider / dotnet-install / vswhere / nuget.exe from Microsoft endpoints; Windows PowerShell only, not used here (we invoke `dotnet build`/`dotnet test` directly) | benign |
| `<Exec>` in `build/Codecoverage.proj`, `eng/helix.proj`, `src/Native/*.proj`, `ModelRedist.csproj` | coverage report / helix / native build; not imported by `Microsoft.Data.Analysis(.Tests).csproj` or their references | benign, not executed |
| `Directory.Build.props/targets`, `test/Directory.Build.props/targets` | standard Arcade imports, TFM selection, analyzer settings; no Exec/download | benign |
| `NuGet.config` | only Microsoft `pkgs.dev.azure.com/dnceng` public feeds | benign |
| `test/Microsoft.Data.Analysis.Tests` + `Microsoft.ML.TestFrameworkCommon` | xUnit tests, no process spawning on load; `TestDownloadUtils.cs` downloads test datasets only when specific ML tests ask (not used by DataFrame tests) | benign |

Verdict: **no malicious code found**; upstream is the official dotnet org repository. OK to build/test the DataFrame projects.
