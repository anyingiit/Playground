# Malicious-code audit — MudBlazor/MudBlazor @ 47584cb (dev, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/mudblazor31` → no auto-exec hooks, no npm lifecycle hooks, no committed binaries, no pattern findings (tool scans only 81 script/text files, so .NET build surface was reviewed manually below).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `src/Directory.Build.props` / `.targets` | Only compiler settings, Roslyn version, Bun wrapper command strings, CompilerVisibleProperty items | benign |
| `src/MudBlazor/MudBlazor.csproj` `<Exec>` targets (`dotnet tool restore`, `bun install --frozen-lockfile`, `bun run build.mts`) | Frontend asset build (SCSS/TS bundling). Conditioned on `SkipBunCompile != true`; we build with `/p:SkipBunCompile=true` so none of these run | benign, not executed |
| `.config/dotnet-tools.json` | single local tool `bundotnet.cli` 1.3.0 (Bun downloader wrapper) — only used by the skipped targets above | benign, not executed |
| `src/package.json` | deps eslint/sass/typescript/happy-dom, `trustedDependencies: [sass]`; no scripts; not installed (Bun skipped) | benign, not executed |
| `src/MudBlazor.Docs*.csproj`, `MudBlazor.UnitTests.Docs.csproj` `<Exec dotnet run ...>` | Docs compiler / docs-test generator; not part of the unit-test project graph we build | benign, not executed |
| `src/MudBlazor.UnitTests/*.csproj`, `UnitTests.Shared`, `UnitTests.Viewer` | NuGet refs only (bunit, nunit, Moq, AwesomeAssertions, coverlet.MTP, FluentValidation, ASP.NET WASM); no custom targets, no SetUpFixture/ModuleInitializer, no Process.Start; one `new HttpClient()` DI registration in test context (no network calls) | benign |
| `tools/*.ps1` | Icon/CSS generator + package check scripts; never invoked by build/test | benign, not executed |
| NuGet config | no `nuget.config` in repo → default nuget.org feed | benign |

Verdict: **no malicious code found**; safe to build/test the `MudBlazor.UnitTests` graph with `/p:SkipBunCompile=true`.
