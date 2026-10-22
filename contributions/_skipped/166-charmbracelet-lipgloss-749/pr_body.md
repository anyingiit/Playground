## Description

Importing `charm.land/lipgloss/v2` currently builds the default `Writer` at package init via
`colorprofile.NewWriter(os.Stdout, os.Environ())`. When running inside tmux, `colorprofile.Detect`
spawns `tmux info` (with `context.Background()`, i.e. no timeout), so every program that imports
lipgloss pays for a subprocess before `main()` — even if it only uses `Style.Render` and never touches
`Writer` or the `Print*`/`Sprint*` helpers (#749).

This PR makes the detection lazy:

- `Writer` now starts as `&colorprofile.Writer{Forward: os.Stdout}`, i.e. with
  `colorprofile.Unknown` as its profile ("absence of a profile"; `Detect` never returns it).
- A small internal `defaultWriter()` helper (guarded by a mutex) detects the profile against
  `Writer.Forward` the first time `Print`, `Println`, `Printf`, `Sprint`, `Sprintln` or `Sprintf` needs it,
  and stores it in `Writer.Profile`, so detection runs at most once.
- The documented v2 patterns keep working: replacing `lipgloss.Writer` (e.g. with
  `colorprofile.NewWriter(os.Stderr, os.Environ())`) or setting `lipgloss.Writer.Profile` — and setting the
  profile explicitly now also skips detection entirely.
- The `Fprint*` functions are unchanged (they already detect per call on the given writer).

**Trade-off for reviewers:** code that reads `lipgloss.Writer.Profile`, or writes to `lipgloss.Writer`
directly (e.g. `fmt.Fprint(lipgloss.Writer, s)`), *before* any of the package-level print functions has
been called will now see `colorprofile.Unknown` (which `colorprofile.Writer` treats like `NoTTY`, i.e. it
strips ANSI) instead of the detected profile. I couldn't find a way to keep that exact behaviour with an
exported `*colorprofile.Writer` variable while avoiding init-time detection. If you'd prefer a different
shape (e.g. an exported accessor, or addressing the subprocess cost in `colorprofile` instead), I'm happy
to adjust — or feel free to take this in another direction. The opt-in `compat` package still detects at
init; I left it alone since it's a separate import.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #749

## Checklist

- [x] Tests pass locally
  - New `TestWriterDetectsProfileLazily` re-runs the test binary in a subprocess with `TMUX`/`TTY_FORCE=1`
    set and a fake `tmux` on `PATH` that records whether it was called. It checks that (a) merely importing
    lipgloss does not run `tmux info`, (b) `Print` and `Sprint` still trigger detection, and (c) presetting
    `Writer.Profile` skips detection. Without the fix the `import` and `preset profile` cases fail; with it
    all pass. (Skipped on Windows since the fake binary is a shell script.)
  - `go test ./...` — all packages pass
  - `go vet .` — clean; `golangci-lint run .` (v2.5.0) reports nothing for the changed files (only 3
    pre-existing `gofumpt` findings in untouched `color.go`, `get.go`, `terminal.go`)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file (release notes are generated)
- [x] Documentation is updated (if applicable) — `Writer`'s doc comment explains the lazy detection
