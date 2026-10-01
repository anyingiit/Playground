## Description

Slack-created sessions always ran on OpenCode: the Slack bot never sent `harness` to `POST /sessions`, and the Slack integration settings had no harness field. This adds a workspace-level **Agent harness** setting for Slack, built on the shared helpers in `packages/shared/src/harnesses.ts` (`harnessIdSchema`, `checkHarnessCompatibility`, `getHarnessLabel`). Nothing is reimplemented.

**What changes**

- **shared**: `slackGlobalSettingsSchema` gets an optional `harness`. When it is unset, the built-in harness (OpenCode) is used.
- **control-plane** (`IntegrationSettingsStore.validateSlackSettings`): `harness` is accepted at the global level only. Unknown ids are rejected, and so is a Slack default model the harness cannot run, with the shared message (`Model "openai/gpt-5.4" cannot run on the Claude Agent harness.`).
- **slack-bot**
  - `getSlackSettings` reads the harness. An unknown value falls back to the default and does not drop the rest of the settings.
  - `startSessionAndSendPrompt` picks the harness in this order: the launch plan (stale-thread recovery), then the Slack setting, then `DEFAULT_HARNESS`. Before anything is created, it checks both the session-default model and the first-prompt model against that harness. Those models can come from env `DEFAULT_MODEL`, the Slack default model, App Home or `!model` flags. On a mismatch it replies in the thread with the reason and a hint, and no session is created. It sends `harness` only when it is not the default, so OpenCode requests stay byte-for-byte the same. It also stores the harness on the thread mapping.
  - Stale-thread recovery reuses the thread's harness. Mappings written before this change have no harness and recover on OpenCode, so a later change to the workspace setting never switches an existing thread.
  - A follow-up `!model` that the thread's harness cannot run gets the same clear reply. It is not sent, so it can no longer surface as a generic failure or a stale-session recovery.
- **web** (Settings › Integrations › Slack): adds an "Agent harness" picker. The default-model list is filtered with the existing `filterModelOptionsForHarness`, and an incompatible stored pair shows the error and disables Save. Reset returns to OpenCode.
- **docs**: `docs/CLAUDE_AGENT.md` gets a new "Slack" subsection covering model sources, auth and the image requirement. The public Slack and agent-harness pages and `CHANGELOG.md` (Unreleased › Added) are updated too.

Provider auth needs no Slack-specific code. Slack sends no explicit account selection, so the control plane's existing resolver applies: an installation-default Claude account on Claude Agent, otherwise the API key. The minimum image generation for the Claude harness is also enforced by the existing launch/image-selection path. Out of scope, as the issue says: Slack-triggered automations, and changing a running session's harness.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #2044

## Checklist

- [x] Tests pass locally:
  - `npm run build -w @open-inspect/shared`
  - `npx vitest run` in `packages/slack-bot`: 523 passed. In `packages/shared`: 1082 passed. In `packages/web`: 2676 passed. In `packages/docs`: 44 passed.
  - `npx vitest run` in `packages/control-plane`: 6114 passed, 2 failed. Both failures are in `src/routes/environments-catalog.test.ts` ("conceals and audits nonmember or missing team …"), and they fail the same way on `main` without this change.
  - New tests fail without the fix (red → green): control-plane 2, slack-bot 13 (5 new launcher, 2 index/thread-flow, client, store, settings, plus updated expectations), web 3.
  - `npm run typecheck -w` for shared, control-plane, slack-bot and web: clean. `npx eslint .`: clean. `npx prettier --check` on changed files: clean.
- [x] `CHANGELOG.md` is updated (if applicable): an "Unreleased › Added" entry.
- [x] Documentation is updated (if applicable): `docs/CLAUDE_AGENT.md`, `packages/docs/content/docs/integrations/slack.mdx` and `packages/docs/content/docs/models/agent-harnesses.mdx`.
