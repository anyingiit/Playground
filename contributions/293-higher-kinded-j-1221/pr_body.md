## Description

The Path Types table in the cheat sheet named an extract method that two types don't have:

- `LazyPath<A>`: `.run()` → `A` is now `.get()` → `A`. `LazyPath` has `get()` (and `force()`, which lets checked exceptions through), but no `run()`.
- `GenericPath<F, A>`: `.run()` → `Kind<F, A>` is now `.runKind()` → `Kind<F, A>`.
- `WithStatePath<S, A>`: `.run(initial)` → `(S, A)` is now `.run(initial)` → `StateTuple<S, A>`, the type `run(S)` returns. This is the optional third row from the issue.

I also added a line under Documentation in `release-history/unreleased.md`, in the same form as the Prism glossary entry (#1155).

Fixes #1221

## Type of change

- [x] Documentation update

## How Has This Been Tested?

Each method name and return type is checked against `LazyPath.java` (`get()`, `force()`), `GenericPath.java` (`runKind()`) and `WithStatePath.java` (`run(S initialState)` returns `StateTuple<S, A>`).

## Book changes

- [ ] `./gradlew :hkj-examples:test :hkj-examples:bookVerify` and `hkj-book/check.sh` pass. `hkj-book/check.sh` passes: heading and anchor checks (including the new `../cheatsheet.md#path-types` link), mermaid, chapter footers, readability (`--strict`, every page matches its baseline) and British spelling. I didn't run `./gradlew :hkj-examples:test :hkj-examples:bookVerify`, since the change touches no Java snippet, only table cells and a release note.
- [x] The prose follows the Style Guide.
- [x] No new rule or refusal, and no generated page is edited.
- [x] Readability counts are unchanged.

## Checklist:

- [x] I have performed a self-review of my own code
- [x] I have added an entry to `hkj-book/src/release-history/unreleased.md` for a change a user can see

## Additional Comments (Optional)

I prepared this with help from an AI coding assistant (Claude Code), and checked each method against the source myself.
