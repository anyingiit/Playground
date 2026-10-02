## Description

Enables the built-in .NET code analyzers for the projects in `src/`, as proposed in the issue:

```xml
<EnableNETAnalyzers>true</EnableNETAnalyzers>
<AnalysisLevel>latest</AnalysisLevel>
<AnalysisMode>Recommended</AnalysisMode>
```

The properties are added next to `TreatWarningsAsErrors` in all six `src` projects (NLog, NLog.OutputDebugString, NLog.RegEx, NLog.Targets.AtomicFile, NLog.Targets.GZipFile, NLog.WindowsEventLog). Since these projects build with `TreatWarningsAsErrors`, turning the analyzers on without tuning breaks the build (464 errors for `src/NLog` across its target frameworks). `.editorconfig` therefore gets:

- The four entries from the issue (CA1001, CA1848 → suggestion; CA1707, IDE0130 → none).
- **Public API rules → none / suggestion**: CA1000, CA1069, CA1710, CA1711, CA1716 (`none`, e.g. 46 hits for identifiers like `Error`/`Event`/`Default`) and CA1067, CA1068, CA1725 (`suggestion`). Fixing them would mean breaking or behavior-relevant API changes.
- **Suggested API not available on all targets (net35 / netstandard2.0)** → suggestion: CA1840, CA1858, CA1865, CA2249, CA2263.
- **Remaining code quality rules** → suggestion for now, so they still show in the IDE and can be cleaned up in separate, focused PRs: CA1305, CA1309, CA1806, CA1822, CA1830, CA1838, CA1859, CA1861, CA2101, CA2208.

No source code is changed, so the PR only affects build diagnostics. Each `.editorconfig` line carries the rule title as a comment, so it's easy to raise individual rules back to `warning` once they are fixed. The test projects are not included because they don't build with `TreatWarningsAsErrors`, and the Recommended mode reports roughly 1000 extra warnings there (mostly CA1707, CA1305, CA2201). I'm happy to add them in a follow-up if you want.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #5916

## Checklist

- [x] Tests pass locally (.NET SDK 10.0.401, Linux)
  - Analyzers on without the `.editorconfig` tuning: `dotnet build src/NLog/NLog.csproj -c Release` fails with 464 errors; the other five `src` projects fail as well (they build NLog first, and NLog.RegEx / NLog.Targets.AtomicFile additionally hit CA2263 / CA2101).
  - With this PR: `dotnet build src/<project>/<project>.csproj -c Release --no-incremental` succeeds for all six `src` projects with 0 errors and no CA/IDE warnings. The only warning left is NETSDK1210, which also appears on `dev`. The same holds for `src/NLog` with `/p:targetFrameworks="net46;net45;net35;netstandard2.0;netstandard2.1"` as in `build.ps1`.
  - `dotnet test ./tests/NLog.UnitTests/ --framework net10.0 --configuration release`: Passed 2970, Skipped 8, Failed 0
  - Not run: the Windows-only steps (`CheckSourceCode`, net462/net35 test runs, `build.ps1` pack).
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes are maintained by the maintainers)
- [ ] Documentation is updated (if applicable) — n/a (build configuration only)
