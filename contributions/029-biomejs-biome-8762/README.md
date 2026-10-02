# biomejs/biome #8762 — noUnusedImports ignores JSDoc links placed before imports / at EOF / before plain statements

| 项 | 值 |
|---|---|
| Issue | https://github.com/biomejs/biome/issues/8762 |
| Tier | 高活跃高Star |
| Labels | A-Analyzer, L-JavaScript, S-Feature, S-Help-wanted |
| Status | ✅ ready — red→green, full `biome_js_analyze` suite + clippy + fmt pass; PR prose must be written by the submitter (see below) |
| Duplicate-PR check | No open PR (re-checked 2026-09-24 before finishing: issue open, 0 comments, unassigned, no linked PR; open-PR search for "jsdoc" shows nothing related). One earlier PR **#9666** (same idea, "collect JSDoc references from every token") was **closed unmerged** on 2026-03-29 by ematipico after Conaclos labelled it `M-Likely Agent` ("automated PR without a human in the loop"); no technical objection was posted. |
| Base | `main` @ 8d0b990 (2026-09-24) |

Earlier candidate #8185 (noUnusedPrivateClassMembers) was dropped: it no longer reproduces on `main` (a test with the
issue's exact code passes in both `.ts` and `.js`), so there was nothing to fix. Could be worth a comment on the issue.

## 需要提交者注意 (AI policy — read before submitting)

- `CONTRIBUTING.md` → "AI assistance notice": AI use is **allowed but must be disclosed, with its extent** (e.g. "This PR was written primarily by Claude Code").
- `CONTRIBUTING.md` + `AGENTS.md`: the **PR description and all comments must be written by the human contributor, not by AI**. Short and to the point. Maintainers close PRs they believe have AI-written communication. So treat the PR text below only as notes and **write the PR body yourself, in your own words**, and keep it short.
- `AGENTS.md`: automated contributions may add `🤖🤖🤖` at the end of the PR title to opt into the "streamlined merge process". Since the previous attempt (#9666) was closed as a "likely agent" PR, being upfront (disclosure, and optionally the marker) is the safest route. Be ready to answer review questions yourself.
- Use the repo PR template (`.github/PULL_REQUEST_TEMPLATE.md`); do not replace it.
- No DCO / sign-off required. Commit title is Conventional Commits (squash-merged with the PR title).
- Target branch `main` (behaviour fix, patch changeset included). If maintainers treat it as a feature (issue is labelled `S-Feature`), they may ask for `next` + a `minor` changeset.

## 问题理解

`noUnusedImports` treats an import as used when a JSDoc comment references its name (`{@link X}`, `{@linkcode X}`,
`@param {X}`, `@type {X}` …). The collector (`JsDocTypeCollectorVisitor` in
`crates/biome_js_analyze/src/lint/correctness/no_unused_imports.rs`) only looked at the leading trivia of the **first
token of certain node kinds** (declarations, class/object/TS-type members, enum members, exports, static member
assignments). A JSDoc comment attached anywhere else was ignored, e.g.

```ts
/** @packageDocumentation  … {@link Foo} */   // attached to the `import` token
import type { Foo } from "mod";               // reported as unused
run(); /** {@link Bar} */                      // trailing trivia
/** {@link Baz} */                             // attached to EOF
```

TSDoc requires `@packageDocumentation` to be the first comment in the file, i.e. before the imports, so the false
positive hits exactly that documented pattern.

## 合理性判断

Maintainers labelled it `S-Help-wanted`; the rule already intends to honour JSDoc references (issues #4677, #7876 were
fixed the same way), and the issue even proposes the approach. The fix is small and local to one rule.

## 改动

- `no_unused_imports.rs`: the visitor now reacts only to the root node and scans the leading **and trailing** trivia of
  every token of the file for JSDoc comments (`JsdocComment::text_is_jsdoc_comment`), feeding the same regex-based
  extractor as before. This is a superset of the old node-based collection (every comment is trivia of some token), so
  all previous cases keep working. The now-unused `AnyJsWithTypeReferencingJsDoc` union and imports were removed.
- Tests: `tests/specs/correctness/noUnusedImports/valid_issue_8762.ts` (JSDoc before an import, before an expression
  statement, trailing on the same line, `@type` before an assignment, at EOF) and
  `valid_issue_8762_package_documentation.ts` (`@packageDocumentation` header before the only import), with snapshots.
- `.changeset/jsdoc-links-anywhere-no-unused-imports.md` (patch).

## 验证

Build dirs: `CARGO_TARGET_DIR=/home/user/work/biome-cache/target`, toolchain 1.98.1 (from `rust-toolchain.toml`).

Red (fix stashed, new tests present):
`cargo test -p biome_js_analyze --test spec_tests -- no_unused_imports::valid_issue_8762`
→ `test result: FAILED. 0 passed; 2 failed` — every referenced import reported ("This import is unused."):
`valid_issue_8762.ts` lines 4,5,6,8 and `valid_issue_8762_package_documentation.ts` line 8.

Green (with fix):
`cargo test -p biome_js_analyze --test spec_tests -- no_unused_imports` → `test result: ok. 48 passed; 0 failed`
(all existing noUnusedImports specs incl. the JSDoc/TSDoc ones from #4677/#7876, Svelte/Vue embeds, unchanged snapshots).

`cargo fmt --all -- --check` → clean.

Full crate suite: `cargo test -p biome_js_analyze` → all pass
(spec_tests `3159 passed; 0 failed`, lib unit tests `313 passed; 1 ignored`, other test binaries 4/1/2/1/10 passed).

`cargo clippy -p biome_js_analyze -- --deny warnings` → clean.
`--all-targets` could not be used: it fails **before reaching this crate** on a pre-existing
`unused import: Resource` warning in `crates/biome_service/src/diagnostics.rs:11` (a dev-dependency; file not touched by
this patch, so the same happens on the unpatched base). Upstream CI runs `just l` on its own toolchain; nothing to do here.

Not run: `just l` / whole-workspace clippy and the website doc checks (disk budget; the rule docs were not changed).
Build cache (`biome-cache`, ~12 GB at the end incl. clippy) was deleted after verification.

Note: running the spec tests locally rewrites three Svelte `.snap` files only to drop an `assertion_line: 149` metadata
line (insta version noise, unrelated) — those were reverted and are not in the patch.

## 如何提交

```bash
git clone https://github.com/biomejs/biome && cd biome
git checkout -b fix/no-unused-imports-jsdoc-anywhere origin/main
git am /path/to/0001-fix-noUnusedImports-count-JSDoc-references-anywhere-.patch
git push <your-fork> fix/no-unused-imports-jsdoc-anywhere   # open PR against main
```

## PR title

```
fix(noUnusedImports): count JSDoc references anywhere in the file
```
(Optionally append ` 🤖🤖🤖` per biome's AGENTS.md if you want the agent-contribution track.)

## PR body (DRAFT NOTES — biome requires the PR text to be written by you; rewrite in your own words and keep it short)

Uses biome's template (`## Summary` / `## Test Plan` / `## Docs`); the checklist items from our format are folded in.

```markdown
## Summary

Closes #8762.

`noUnusedImports` only looked for JSDoc references in comments attached to declarations, members and exports.
A `{@link Foo}` in a `@packageDocumentation` comment above the imports, in a comment before a plain statement,
or at the end of the file was ignored, so the import was reported as unused. The collector now scans the
comments of every token in the file (the old cases are a subset of this). Changeset included (patch).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

(An earlier attempt, #9666, took the same approach and was closed as a likely unattended agent PR — this one
has a human reviewing and answering.)

## Test Plan

- New specs `valid_issue_8762.ts` and `valid_issue_8762_package_documentation.ts` fail without the change
  (every referenced import is reported) and pass with it.
- `cargo test -p biome_js_analyze` passes; `cargo clippy -p biome_js_analyze -- -D warnings` and `cargo fmt --check` are clean.
- CHANGELOG: changeset `.changeset/jsdoc-links-anywhere-no-unused-imports.md`.

## Docs

N/A (behaviour fix, rule docs unchanged).
```
