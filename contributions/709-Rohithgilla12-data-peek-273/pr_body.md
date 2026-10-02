## Description

Adds Markdown as an export format, so result sets can be pasted straight into PR descriptions, issues and docs.

**Summary of changes**

- `lib/export.ts`
  - `ExportFormat` now includes `'markdown'`.
  - New `escapeMarkdownCell(value)`: `null`/`undefined` → empty cell, objects → JSON (same as CSV), `|` → `\|`, and `\r\n` / `\r` / `\n` → a space so each row stays on one line.
  - New `exportToMarkdown(data)`: emits a GitHub-flavored table (`| a | b |`, then `| --- | --- |`, then one line per row). With no rows it emits only the header and separator.
  - `serializeExport` handles `'markdown'`, so **Download file** and **Copy to clipboard** both work through the existing paths. Downloads get the `.md` extension and the `text/markdown` MIME type.
- `components/export-menu-items.tsx`: adds a **Markdown** entry (`FileText` icon). This shared menu is used by both the results toolbar and the schema explorer's table menu.
- `apps/docs/content/docs/features/export.mdx`: documents the new format, its file name and its escaping rules.

I followed the existing `exportToCSV(data)` / `exportToJSON(data)` signature (`ExportData` in, string out) rather than the `(rows, columns, options)` shape sketched in the issue, so it slots into `serializeExport` like the other formats.

**Type of change:** New feature

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #273

## Checklist

- [x] Tests pass locally
  - New tests in `src/renderer/src/lib/__tests__/export.test.ts` cover `escapeMarkdownCell` (null/undefined, pipes, newlines, objects, primitives), `exportToMarkdown` (header + separator, null cells, escaping in headers and values, no rows) and `serializeExport(data, 'markdown')`. Without the change 10 of them fail; with it the file passes 88/88.
  - `pnpm --filter @data-peek/desktop exec vitest run`: 1398 passed, 56 skipped. The only failing file, `src/main/__tests__/mcp-handlers.test.ts`, fails to load the same way on `main` in my environment because I installed without the Electron binary ("Electron failed to install correctly").
  - `pnpm typecheck` (in `apps/desktop`, node + web): passes
  - `eslint` and `prettier --check` on the changed files: clean
- [x] My code follows the project's style guidelines (Prettier: single quotes, no semicolons)
- [x] I have performed a self-review
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (no changelog file in the repo)
- [x] Documentation is updated (if applicable) — `apps/docs/content/docs/features/export.mdx`

## Screenshots

Not included. The UI change is one more row in the existing export submenu, alongside CSV / JSON / SQL.
