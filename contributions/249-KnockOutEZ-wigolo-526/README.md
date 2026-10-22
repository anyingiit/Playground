# KnockOutEZ/wigolo#526: authStatePath (WIGOLO_AUTH_STATE_PATH) is never applied to the browser context

| 项 | 值 |
|---|---|
| Issue | https://github.com/KnockOutEZ/wigolo/issues/526 |
| Tier | 自由（单人维护、活跃，TS） |
| Labels | area:fetch, bug, good first issue, help wanted |
| Status | ✅ ready，独立复核 PASS（未提交） |
| 重复 PR 检查 | 2026-10-22 20:10 UTC：`repo:KnockOutEZ/wigolo storageState` → 只有 #527（原报告者 9 月开的，9-25 **自己关闭**、无理由、维护者未评审）；8 个 open PR 无相关 |
| 维护者态度 | 2026-10-21 维护者（自己也用 Claude）确认 bug、标"up for grabs"，给了修法建议并要单测、最好加集成测试 |
| AI 政策 | 无限制；维护者本人用 Claude Code |
| Base | `main` @ 3507bb8 |
| DCO / CLA | 无 DCO。**CLA 是"提交即同意"**（CONTRIBUTING），无需签名/个人信息；但条款含**授予维护者再许可（可转商业许可）的权利**——符合"GitHub 登录即可"规则，仅提醒 owner 知悉 |
| 需先认领 | 否（维护者已标 up for grabs） |

## 问题理解
`getAuthOptions()` → router → `fetchWithBrowser` 一路传了 `storageStatePath`，但 `browser-pool.ts` 里三个建 context 的地方都没用它，`use_auth` 的抓取实际是未登录状态。

## 关键设计点
维护者建议在三处 `newContext` 都加 `storageState`。但 L429 是**池化 context**（会被后续抓取复用）——直接加会把登录态泄漏给之后的匿名抓取（#527 + CodeRabbit 也指出过）。所以：
- 池化路径：带 storage state 的抓取在**共享 browser 上新建专属 context**（`storageState` + `acceptDownloads`），在 finally 里关闭（复用现有 `dedicated` 清理逻辑，不关共享 browser、不占 stealth 名额）。比 #527 的"每次起一个 throwaway browser"更省。
- stealth 路径：专属 context 的选项里加 `storageState`。
- CDP / hosted scraping browser：新建 context 时带上；已有 context（远端浏览器自己的）无法事后注入，照旧使用并 `log.warn`。
- 文档 `docs/configuration.md` 补一句。（CHANGELOG 按复核意见已去掉：外部 PR 均不改它，维护者发版时自己写。）
- userDataDir（#161）未处理，PR 里说明。

## 验证
- 单测 `tests/unit/fetch/browser-pool.storage-state.test.ts` 6 个：红（只回退 src）→ 4 失败 2 通过（2 个是"行为不变"守卫）；绿 → 6 通过
- 集成测试（真 headless Chromium + 本地 server 回显 Cookie 头）：红 → 失败（cookie 没发）；绿 → 通过，且随后的匿名抓取 cookie 为空。整个 `tests/integration/fetch/browser-pool.test.ts` 20/20
- `npm run lint`（tsc）通过
- 全量 `vitest run tests/unit`：7926 通过、3 失败；3 个都是 `config-writer-json` 的 PERMISSION_DENIED 用例，在未改动的 main 上同样失败（沙箱以 root 运行，忽略文件权限），与补丁无关
- 本地环境注记：沙箱里 Playwright 1.60 需要 chromium 1223，只有 1194，做了本地别名才跑起集成测试（不影响补丁）

## 如何提交
```
tools/submit_pr.sh contributions/249-KnockOutEZ-wigolo-526 KnockOutEZ/wigolo main fix/apply-auth-storage-state contributions/249-KnockOutEZ-wigolo-526/pr_title.txt contributions/249-KnockOutEZ-wigolo-526/pr_body.md
```
（不加 `--signoff`。）

## 独立复核（2026-10-22 20:19 UTC）

结论 PASS。复核者从 3507bb8 重新克隆并 `git am`：单测 6 个，回退修复后 4 红 2 绿（2 个是行为不变的守卫）；集成测试回退后红，修复后全文件 20/20；lint 通过；`tests/unit/fetch` 899/899。代码逻辑（dedicated 清理、stealth 信号量、abort、shutdown）均无问题。已采纳：
- 去掉 CHANGELOG 改动（仓库惯例）；
- `npm test` 勾选改为未勾，并如实写明跑了哪些；
- 对 #527 的致谢写准确：单测文件布局参照了 #527（AGPL，可复用；也满足 CLA 第 3 条"原创或有权提交"）；
- CDP 段补一句：托管 scraping browser 无 context 时会把会话载入远端浏览器。
