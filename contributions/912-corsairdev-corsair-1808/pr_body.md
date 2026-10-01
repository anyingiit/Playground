## Description

`corsair ui` / `corsair studio` parsed `--port` with `Number.parseInt(options.port, 10)`, which only reads a numeric prefix:

- `--port 3000abc` was silently accepted as port `3000`;
- `--port abc` became `NaN`, which is not caught by `options.port ?? 4317` in `packages/studio/server/index.ts` and then fails inside `server.listen`.

This PR adds a small exported helper `parsePortOption()` in `packages/cli/src/commands/studio.command.ts` that applies the same rule `corsair http` already uses (the whole value must be digits, and the port must be 1–65535). `action()` now validates the port before resolving `@corsair-dev/studio`, and on a bad value prints `[#corsair]: Invalid --port "<value>". Expected an integer between 1 and 65535.` and exits with code 1. If `--port` is omitted, behaviour is unchanged: `undefined` is passed through and Studio falls back to its default port.

Tests (`packages/cli/src/commands/studio.command.test.ts`):
- `parsePortOption` accepts `1`, `3000`, `4317`, `65535` and returns `undefined` when no port is given;
- it rejects `3000abc`, `abc`, `''`, `0`, `65536`, `-1`, `30.5`, `1e3`, `' 3000'`;
- `StudioCommand.action` exits with code 1 and prints the error for `--port 3000abc` and `--port abc`. Without the fix these two action tests fail, because the bad value is never rejected.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1808

## Checklist

- [x] I have run `pnpm lint` and all checks pass (`biome check .`: 0 errors; the 7 warnings are already on `main`, in other packages)
- [x] I have run `pnpm typecheck` and there are no TypeScript errors (`tsc --noEmit` in `packages/cli`: clean)
- [x] I have run `pnpm build` and all packages build successfully (`pnpm build` in `packages/cli`: success; I did not build the whole monorepo)
- [x] I have run `pnpm test` and all tests pass (`npx jest` in `packages/cli`: 8 suites, 52 tests passed)
- [x] I have added or updated tests where applicable (new `studio.command.test.ts`, 16 tests)
- [ ] I have added or updated necessary documentation (n/a: user-visible behaviour only changes for invalid input)
- [ ] `CHANGELOG.md` is updated (n/a: the repo has no CHANGELOG)

## Additional Notes

No new dependencies and no breaking changes for valid input. `--port ''` used to fall back to the default port. It is now rejected, the same way `corsair http` handles an empty port.
