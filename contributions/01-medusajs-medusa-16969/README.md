# medusajs/medusa#16969 — applyTranslations collects IDs from alias services

| | |
|---|---|
| Issue | https://github.com/medusajs/medusa/issues/16969 |
| Tier | 高活跃 + 高 Star（Medusa，~36k★） |
| Labels | `good first issue`, `type: bug` |
| Status | ✅ 实现 + 测试通过 · ⚠️ **已有同类 PR [medusajs/medusa#16970](https://github.com/medusajs/medusa/pull/16970)**（同样的 string 过滤，但没有测试，被 bot 标记 `requires-more`，仅因 changeset 格式） |
| 建议动作 | 不要开重复 PR。可在 #16970 下留言提供我们的回归测试（见下方评论草稿）；若 #16970 被关闭/停滞，再用本补丁开 PR |

## 问题理解
开启 locale 时，`applyTranslations`（`packages/core/utils/src/translations/apply-translations.ts`）
递归收集**所有**嵌套对象的 `id`，包括通过 Remote Query alias 暴露的外部服务（如自建 CMS，数字 id）。
结果查询变成 `reference_id IN (770, 'prod_…')`，而 `translation.reference_id` 是 text 列，
Postgres 报 `operator does not exist: text = integer`。

## 合理性判断
- 维护者打了 `type: bug` + `good first issue`；medusa 官方 bot 在 #16970 中确认“fix itself is correct and well-targeted”。
- 所有可翻译的 Medusa 实体 id 都是字符串（`prod_…` 等），`reference_id` 为 text，数字 id 不可能有翻译，过滤是安全的。
- 字符串 id 的 alias 服务仍会被查询，但只是查不到翻译，不会报错（行为与现在一致）。

## 改动
- `gatherIds` 只收集 `isString(id)` 的 id（复用仓库已有 `common/is-string`）。
- 新单测：`should only gather string ids and ignore numeric ids from aliased services`。
- changeset：`"@medusajs/utils": patch` — `fix(utils): …`（符合 bot 要求的 `fix(package): ` 格式）。

## 验证（在真实 monorepo 环境：`yarn install` + 构建 `@medusajs/deps`/`@medusajs/types`）
- `packages/core/utils`: `yarn build` ✅；`yarn test` → **107 suites / 584 passed, 1 skipped** ✅
- 新测试在未修复代码上失败 ✅（证明测试有效）
- Prettier 2.8.8（仓库配置）检查：改动部分无问题（该 spec 文件第 86 行有一处**既存**格式问题，未触碰）

## 如何提交
```bash
git clone https://github.com/<you>/medusa && cd medusa
git checkout -b fix/translations-ignore-non-string-ids origin/develop
git am /path/to/0001-fix-utils-ignore-non-string-ids-when-gathering-trans.patch
git push -u origin HEAD   # base: develop
```

### 给 #16970 的评论草稿（推荐）
```
Hi! I independently hit the same fix for #16969 and wrote a regression test for it — feel free to
pull it into this PR if useful (it fails on `develop` and passes with the string-id check):

<paste the `it("should only gather string ids and ignore numeric ids from aliased services", ...)` block>

Context: I'm using some spare AI-assistant (Claude Code) quota to try to help out on good-first-issues;
if it's not useful, just ignore this — no worries at all 🙂
```

### PR（仅当 #16970 关闭后）— chefs-pick-oss-starter 格式
**Title:** `fix(utils): ignore non-string ids when gathering translation reference ids`

```markdown
## Description

`applyTranslations` walked every nested object and collected any truthy `id`, including numeric ids of
entities returned by aliased Remote Query services (e.g. a custom CMS exposed as `cms`). Mixed into the
text `reference_id IN (...)` filter they made Postgres fail with `operator does not exist: text = integer`.

`gatherIds` now only collects string ids. Translations are keyed by a text `reference_id` and every
translatable Medusa entity uses a string id, so a non-string id can never have a translation.
A string id from an alias service is still looked up and simply finds nothing, as today.

Added a changeset (`@medusajs/utils`: patch).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #16969

## Checklist

- [x] Tests pass locally (`packages/core/utils`: `yarn build`, `yarn test` → 107 suites / 584 tests passed;
      new test fails on `develop` without the fix)
- [x] `CHANGELOG.md` is updated (if applicable) — via changeset `.changeset/translations-ignore-non-string-ids.md`
- [ ] Documentation is updated (if applicable) — n/a, internal bug fix
```
