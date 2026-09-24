# MudBlazor/MudBlazor#3461 — MudDatePicker: Editable input accepts dates outside MinDate/MaxDate

| 项 | 值 |
|---|---|
| Issue | https://github.com/MudBlazor/MudBlazor/issues/3461 |
| Tier | 高活跃高Star (MudBlazor ~10k★, commits daily, maintainers merge outside PRs) |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR text done; submitter must add Before/After recording (see 需要提交者注意) |
| Duplicate-PR check | 2026-09-24: `repo:MudBlazor/MudBlazor 3461` → only #12389 (closed without merge, author deleted fork, no maintainer review). `DatePicker MinDate MaxDate` → #4088 (2022, stale, about calendar display/navigation crash, not typed input) and #13159 (v10 generic refactor, unrelated). Issue unassigned; only comments are the reporter's bump ("still exists", Aug 2025). |
| Base | `dev` @ 47584cb |

## 问题理解

`MudDatePicker` with `Editable="true"` lets the user type any date. The calendar greys out days before `MinDate` / after `MaxDate`,
and keyboard navigation clamps to them, but text typed into the input is converted and accepted even when out of range
(`Date` becomes e.g. 2024-01-09 with `MinDate = 2024-01-10`, and `DateChanged` fires). The reporter expects the same guarantee as
`MudNumericField.Min/Max`.

Root cause: `MudDatePicker.SetDateAsync` only rejects dates for which `IsDateDisabledFunc` returns true; it never looks at
`MinDate`/`MaxDate`. The base class already has `IsDayDisabled(date)` (= `< MinDate || > MaxDate || IsDateDisabledFunc`) which the
calendar uses.

## 合理性判断

- Labeled `bug` + `good first issue` by maintainers; reporter confirmed in Aug 2025 that it still reproduces; verified on current `dev` by the new failing test.
- `MinDate`/`MaxDate` XML docs say "The minimum/maximum selectable date", so accepting out-of-range typed input contradicts the documented contract.
- Previous attempt #12389 chose a different approach (add validation error, keep the value) and was abandoned without review, so there is no maintainer decision against this approach.
- Design choice (called out in the PR): typed out-of-range input is treated exactly like a typed disabled day is today (text cleared, `Date` not changed, `DateChanged` not raised). A date **bound from code** is intentionally not rejected by Min/Max (only by `IsDateDisabledFunc`, as before) to avoid a breaking change that would silently blank existing records (AGENTS.md: "Avoid breaking changes whenever possible").
- `FixYear`/`FixMonth`/`FixDay` (also mentioned in the issue) and `MudDateRangePicker` are left out of scope; mentioned as follow-up.

## AI 政策

- Repo has `AGENTS.md` ("AI Coding Agent Guide for MudBlazor") and `CLAUDE.md`-style guidance; AI-assisted PRs are explicitly expected.
- PR template: "If AI assistance was used, state how in the description. Follow all rules in AGENTS.md carefully." → disclosure paragraph included below.

## 改动

- `src/MudBlazor/Components/DatePicker/MudDatePicker.cs`: in `SetDateAsync`, user input (`suppressInteraction == false`) is checked with `IsDayDisabled` (MinDate, MaxDate, IsDateDisabledFunc); programmatic writes keep the old `IsDateDisabledFunc`-only check. 2-line comment explains why.
- `src/MudBlazor.UnitTests/Components/DatePickerTests.cs`: 3 new tests (6 cases)
  - `Editable_TypingDateOutsideMinMax_IsRejected` ("09/01/2024", "21/01/2024") — regression test for #3461
  - `Editable_TypingDateInsideMinMax_IsAccepted` (both bounds + middle)
  - `SettingDateOutsideMinMaxFromCode_KeepsTheDate` — pins the non-breaking programmatic behaviour

## 验证

Environment: .NET SDK 10.0.401 (global.json wants 10.0.400 band, rollForward latestPatch), Linux x64. Commands follow AGENTS.md.

```bash
dotnet restore src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj
dotnet build src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj --no-restore /p:SkipBunCompile=true --nologo   # Build succeeded, 0 warnings
dotnet test --project src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj --no-restore /p:SkipBunCompile=true -- \
  --filter "FullyQualifiedName~DatePickerTests.Editable_Typing|FullyQualifiedName~DatePickerTests.SettingDateOutsideMinMax" \
  --output Normal --no-ansi --hangdump --hangdump-timeout 30s
```

- RED (tests only, fix not applied): total 6, failed 2 — `Editable_TypingDateOutsideMinMax_IsRejected("09/01/2024")`/`("21/01/2024")`:
  `Did not expect comp.Instance.Date to have a value, but found <2024-01-09>.` / `<2024-01-21>`
- GREEN (with fix): total 6, failed 0, succeeded 6.
- Formatting: `cd src && dotnet format whitespace --no-restore --include MudBlazor/Components/DatePicker/MudDatePicker.cs MudBlazor.UnitTests/Components/DatePickerTests.cs --verify-no-changes` → exit 0.
- Full suite (with fix): `dotnet test --project src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj --no-restore /p:SkipBunCompile=true -- --output Normal --no-ansi --hangdump --hangdump-timeout 120s` → **Passed: total 6134, failed 0, succeeded 6132, skipped 2** (1m24s). No failures, so no base-branch comparison needed.
- Library build for all TFMs: `dotnet build src/MudBlazor/MudBlazor.csproj --no-restore /p:SkipBunCompile=true` → net8.0/net9.0/net10.0 Build succeeded, 0 warnings (TreatWarningsAsErrors on).
- Not run: Bun/TS asset build (no TS/SCSS touched), docs tests (`MudBlazor.UnitTests.Docs`, no docs/API changes), analyzer tests (untouched).
- Duplicate re-check before finishing (2026-09-24): issue still open, unassigned, no linked PR; no new open DatePicker PRs since 09-01 (only #13884, unrelated adornment tooltips).

## 如何提交

```bash
git clone https://github.com/<you>/MudBlazor && cd MudBlazor
git checkout -b fix/datepicker-editable-minmax-3461 origin/dev
git am /path/to/0001-MudDatePicker-Reject-typed-dates-outside-MinDate-Max.patch
git push -u origin fix/datepicker-editable-minmax-3461
# open PR against MudBlazor/MudBlazor:dev
```

### 需要提交者注意
- PR must target **`dev`** (not `main`).
- PR template: **Before/After screenshots from your own run are required for anything user-visible** ("even if the fix itself is pure logic"). Here the visible change is: typing an out-of-range date and leaving the field clears the input instead of keeping the date. Please record a short before/after (e.g. docs page or `src/MudBlazor.UnitTests.Viewer` with `Editable="true" MinDate=... MaxDate=...`) — this could not be produced here (no browser).
- AI use must be stated in the description (done in the disclosure paragraph). Be ready to answer review questions about the design choice (reject vs. validation error, programmatic dates kept).
- No DCO / CLA / changelog fragment required (CHANGELOG.md only points to GitHub releases).

## PR title

```
MudDatePicker: Reject typed dates outside MinDate/MaxDate (#3461)
```

## PR body

```markdown
## Description

With `Editable="true"`, `MudDatePicker` accepted any date typed into the input, even one before `MinDate` or after `MaxDate`: `Date` was set and `DateChanged` fired, although the calendar never lets the user pick such a day and the parameters are documented as the minimum/maximum *selectable* date.

`SetDateAsync` only rejected dates for which `IsDateDisabledFunc` returned true. User input (typed text, calendar picks) is now checked with the existing `IsDayDisabled`, which covers `MinDate`, `MaxDate` and `IsDateDisabledFunc`, so a typed out-of-range date is handled exactly like a typed disabled day already is: the text is cleared, `Date` is not changed and `DateChanged` is not raised.

A date bound from code (the `Date` parameter) is intentionally still only checked against `IsDateDisabledFunc`. Rejecting it by `MinDate`/`MaxDate` would silently blank existing records whose stored date is outside the range, which would be a breaking change. A test pins that behaviour.

Out of scope / possible follow-ups: `FixYear`/`FixMonth`/`FixDay` (also mentioned in the issue) and `MudDateRangePicker`. An earlier attempt (#12389) went the "keep the value, add a validation error" route and was closed without review; I went with rejection because it matches how the component already treats disabled days. Happy to switch if you prefer the validation-error behaviour.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

**Before/After:**
<!-- TODO(submitter): add before/after recording of typing an out-of-range date into an editable picker with MinDate/MaxDate -->

## Related issue

Closes #3461

## Checklist

- [x] I've read the [contribution guidelines](https://github.com/MudBlazor/MudBlazor/blob/dev/CONTRIBUTING.md)
- [x] My code follows the style of this project (`dotnet format whitespace --verify-no-changes` on the changed files: clean)
- [x] I've added or updated relevant unit tests — 3 new tests in `DatePickerTests` (6 cases); the regression test fails on `dev` and passes with the fix
- [x] Tests pass locally (`dotnet test --project src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj /p:SkipBunCompile=true`: 6134 total, 0 failed, 6132 passed, 2 skipped; `dotnet build src/MudBlazor/MudBlazor.csproj` net8/9/10: 0 warnings)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, release notes come from GitHub releases
- [ ] Documentation is updated (if applicable) — n/a, `MinDate`/`MaxDate` are already documented as the min/max *selectable* date
```
