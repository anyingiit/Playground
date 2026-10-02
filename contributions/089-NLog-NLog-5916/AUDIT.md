# Audit — NLog/NLog @ 91217eff (dev, shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/NLog` + manual review of MSBuild targets/props, build scripts and process/network use in `src/NLog` and `tests/NLog.UnitTests`.

| Hit | Reviewed | Verdict |
|---|---|---|
| build.ps1:23 `Invoke-WebRequest` nuget.exe from dist.nuget.org | Official NuGet CLI download for the Windows packaging script; build.ps1 is not run here | benign / not run |
| NLog.Targets.GZipFile / NLog.WindowsEventLog csproj `DownloadFile https://nlog-project.org/N.png` | Fetches the package icon before `GenerateNuspec` (pack only); not triggered by build/test | benign |
| src/NLog.proj `Exec` SandCastle docs | Windows-only documentation target, not used by `dotnet build/test` | benign / not run |
| src/NuGet/NLog.Schema/NLog.Schema.targets | Copies NLog.xsd into consuming projects; no exec/network | benign |
| `Process.Start` in src/NLog (ProcessInfoProperty, csproj ref) / `HttpClient`-like refs | Normal library features (process info layout renderer); nothing runs at build time | benign |
| No committed binaries, no npm hooks, no Directory.Build.props/targets | — | — |

Verdict: nothing malicious; safe to run `dotnet build` / `dotnet test` on src/NLog and tests/NLog.UnitTests.
