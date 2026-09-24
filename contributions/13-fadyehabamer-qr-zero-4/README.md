# fadyehabamer/qr-zero #4 — CLI: add --dark, --light and --module-size for SVG output

| 项 | 值 |
|---|---|
| Issue | https://github.com/fadyehabamer/qr-zero/issues/4 |
| Tier | 自由 |
| Labels | enhancement, good first issue, help wanted |
| Status | ✅ ready — patch + PR text done, all CI steps green |
| Duplicate-PR check | 开始时 & 结束前（2026-09-24）各查一次：仓库只有 owner 的 #1(已合并发布)/#2/#3(杂务)，无相关 PR；issue 无 assignee、无评论 |
| Base branch | `main` @ `0779ccc` |

## 候选评估
- otp-input-kit#5：同作者的 UMD 全局名/README 不一致，可行但价值较低（且验收要求重建 dist）。
- codazo-obsidian#7：只改一行注释，价值最低。
- **qr-zero#4（选中）**：真正的功能缺口 —— `toSvg()` 已支持 `dark`/`light`/`moduleSize`，CLI 未暴露。

## 问题理解
CLI 的 `--svg` 输出只能用默认黑/白和 4px/module。issue 要求加 `--dark <color>`、`--light <color>`（`none`/`transparent` = 无背景）、`--module-size <n>`（正整数），必须配合 `--svg`（`<file>` 或 `-`），否则 exit 2；非法值与 `--margin` 一样报 usage 错误（exit 2）；更新 USAGE、README 表格、CHANGELOG，并在 `test/cli.test.ts` 加测试。

## 合理性判断
由 owner 本人提出并标 good first issue/help wanted；CONTRIBUTING（在 `chore/community-files` 分支 / PR #3）明确欢迎此类改动，要求 Conventional Commits（无 scope）、README 同步、CHANGELOG `## [Unreleased]` 条目、不提交 dist、不改版本号。改动不影响核心 bundle（仅 CLI），符合 “零依赖 / bundle size” 原则。
注意：CONTRIBUTING 写了 “Leave a comment before you pick one up” —— 提交前建议 owner 先在 issue 下留言认领。

## 改动
- `src/cli.ts`：新增 `--dark`、`--light`、`--module-size` 选项并传给 `toSvg()`；无 `--svg` 时报错（exit 2）；空颜色报错；`--light none|transparent`（大小写不敏感）映射为 `light: null`；`--module-size` 必须为正整数（与 `--margin` 同样的正则校验风格）。USAGE 文本更新。颜色值由 `toSvg()` 内部 `escapeXml` 转义，无注入问题。
- `test/cli.test.ts`：3 个新测试（stdout、`none/transparent/NONE`、文件输出）+ 9 个 usage-error 用例。
- `README.md`：CLI 示例 + 选项表 3 行 + 说明需 `--svg`；测试计数 103 → 106。
- `CHANGELOG.md`：新增 `## [Unreleased]` / Added 条目及 compare 链接。
- `src/svg.ts` 未改（issue 列出了它，但 CLI 侧把 `none` 映射成 `null` 已足够，无需改公共 API）。

## 验证
环境：Node（本机），`npm ci` 后：
- 基线（未改）：`npm test` → 103/103 pass。
- Red：新测试 + 旧 `src/cli.ts`（0779ccc）→ `node --import tsx --test test/cli.test.ts` → 9 pass / **3 fail**（新增的 3 个）。usage-error 测试在旧代码上也通过，因为 parseArgs strict 模式本来就拒绝未知选项（exit 2）—— 但这些用例保证新选项的校验。
- Green：`node --import tsx --test test/cli.test.ts` → 12/12 pass。
- 全量 CI 步骤：`npm run typecheck` ✅；`npm test` → **106/106 pass**；`npm run build` ✅；`bash scripts/check-pack.sh` ✅（ESM/CJS/React/types/CLI bin）；`node scripts/size.mjs` → full API gzip 4.84 kB（核心 bundle 未改动，仅 CLI）。
- 手动：`npx tsx src/cli.ts "hello" --svg - --dark "#1d4ed8" --light none --module-size 8` → `width="232"`、无 `<rect>`、`fill="#1d4ed8"`；`qr-zero x --dark red` → exit 2 + 提示需 `--svg`。

## 如何提交
```sh
gh repo fork fadyehabamer/qr-zero --clone && cd qr-zero
git checkout -b feat/cli-svg-colors origin/main
git am /path/to/0001-feat-dark-light-and-module-size-CLI-options-for-SVG-.patch
git push -u origin feat/cli-svg-colors
gh pr create --base main --title "feat: --dark, --light and --module-size CLI options for SVG output" --body-file <PR body below>
```
（仓库不要求 DCO。建议先在 issue 留言认领。）

## PR title
`feat: --dark, --light and --module-size CLI options for SVG output`

## PR body
```markdown
## What does this PR do?

`toSvg()` already accepts `dark`, `light` and `moduleSize`, but the `qr-zero` CLI had no way to set them, so getting brand colours, a transparent background or a specific pixel size meant editing the SVG afterwards. This adds three options for SVG output:

| Option | Maps to | Notes |
| --- | --- | --- |
| `--dark <color>` | `dark` | any CSS colour, e.g. `#1d4ed8` or `currentColor` |
| `--light <color>` | `light` | `none` or `transparent` (case-insensitive) → `light: null`, no background `<rect>` |
| `--module-size <n>` | `moduleSize` | positive integer, validated like `--margin` |

- They work with both `--svg <file>` and `--svg -`.
- Using any of them without `--svg` is a usage error (exit 2) with a hint to add `--svg`, as are an empty colour and a `--module-size` that isn't a positive integer (`0`, `2.5`, `big`, …).
- Colour values still go through `toSvg()`'s XML escaping, so nothing new reaches the markup unescaped.
- `src/svg.ts` is unchanged: mapping `none` to `null` in the CLI was enough, so the library API stays as it is.

Docs: `--help` text, the README CLI example and options table (plus the test count, 103 → 106), and an `## [Unreleased]` CHANGELOG entry.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

Closes #4

## Checklist

- [x] `npm run typecheck` and `npm test` pass (106/106; the 3 new CLI tests fail on `main` and pass with this change)
- [x] `npm run build` passes (and `bash scripts/check-pack.sh` passes too)
- [x] New behaviour has tests (`test/cli.test.ts`: stdout, `--light none/transparent`, file output, and 9 new usage-error cases)
- [x] README updated for API, CLI or limit changes
- [x] `CHANGELOG.md` has an entry under `## [Unreleased]`
- [x] Bundle size change noted below (`npm run size` before / after), if any

## Bundle size

No change: only `src/cli.ts` changed, and the library bundles don't include it (`full API` is still 4.84 kB gzip, `encode + toSvg` 4.22 kB).
```
