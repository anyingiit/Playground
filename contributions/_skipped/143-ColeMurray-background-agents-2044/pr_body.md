## Description

Slack sessions were always created on OpenCode: `createSession()` never sent a `harness`, so the control plane applied its default. This adds an **Agent harness** setting to the Slack integration so operators can choose Claude Agent. Unconfigured workspaces behave exactly as before.

**Settings (shared + control plane + web)**
- `slackGlobalSettingsSchema` gains an optional, global-only `harness` (`harnessIdSchema` from `packages/shared/src/harnesses.ts`).
- `validateSlackSettings` accepts `harness` at the global level only, rejects unknown ids, and applies `checkHarnessCompatibility` when a default model is also set, like the automation save path (e.g. `claude` + `openai/gpt-5.4` → `Model "openai/gpt-5.4" cannot run on the Claude Agent harness.`).
- Settings → Integrations → Slack → Defaults gets an **Agent harness** select. The default-model list is filtered to models the harness can run. Switching to Claude Agent clears an incompatible default model. Choosing OpenCode leaves the key out, so the stored blob does not change for workspaces that never pick a harness. Reset also returns it to OpenCode.

**Slack bot**
- `getSlackSettings` reads `harness`. An unknown value falls back to the default (`.catch(undefined)`) instead of discarding the rest of the settings.
- `startSessionAndSendPrompt` sends `harness` to `POST /sessions` only when one is configured. Every new-session path (mentions, DMs, target picker, stale-thread recovery) goes through this function. It checks the session model and the first-prompt model against the shared rule after all model sources have resolved: `DEFAULT_MODEL`, the workspace default, App Home, `!model`. If the harness can't run the model, it replies in the thread with the reason and creates no session, instead of only showing "couldn't create a session" after the control plane returns a 400.
- The thread mapping stores the harness (only when set), so a follow-up `!model` override that the thread's harness cannot run gets the same reply before any prompt is sent. Mappings written before this change have no harness and resolve to OpenCode, which runs every model, so their behaviour does not change.
- Provider auth is unchanged on the bot side. The control plane already resolves provider auth against the session's harness (`resolveSessionProviderAuth({ harness })`), so a Claude Agent Slack session can use a connected Claude account, and OpenCode keeps using the API key.

**Docs:** `docs/integrations/SLACK.md`, `docs/CLAUDE_AGENT.md`, `packages/docs/.../integrations/slack.mdx` (new "Agent harness" section) and `models/agent-harnesses.mdx`. Also adds an `### Added` entry under Unreleased in `CHANGELOG.md`.

Design choice for reviewers: when the harness can't run the resolved model, the bot rejects the request with an explicit error. It does not silently fall back to another model or to OpenCode. This matches the composer rule in `docs/CLAUDE_AGENT.md` ("rejected with an error rather than silently replaced"). If you would rather fall back (e.g. filter App Home models by harness), that is a small change in `session-launcher.ts`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #2044

## Checklist

- [x] Tests pass locally
  - `npm test -w @open-inspect/slack-bot`: 38 files / 520 tests passed
  - `npm test -w @open-inspect/web`: 263 files / 2676 passed
  - `npm test -w @open-inspect/shared`: 1082 passed. `npm test -w @open-inspect/linear-bot`: 267 passed. `npm test -w @open-inspect/docs`: 44 passed
  - `npm test -w @open-inspect/control-plane`: 6114 passed. 2 failed, in `src/routes/environments-catalog.test.ts` ("conceals and audits nonmember or missing team …"); they fail the same way on unmodified `main` (b98a378) and are unrelated to this change
  - 11 new tests fail without the change and pass with it (slack-bot 6, control-plane 2, web 3)
  - `npm run typecheck` equivalent (`tsc --noEmit` in shared, control-plane, slack-bot, web, linear-bot, github-bot, docs), `npm run lint`, and `npm run format:check` are clean
  - Not run locally: `test:integration` (workerd) and the Next.js builds
- [x] `CHANGELOG.md` is updated: `### Added` entry under Unreleased
- [x] Documentation is updated: Slack integration docs (both copies), the Claude Agent guide and the agent-harnesses page
