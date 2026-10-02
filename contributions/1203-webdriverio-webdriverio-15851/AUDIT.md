# AUDIT — webdriverio/webdriverio

审计对象：`v10` @ 7423b42 (2026-10-01，最终提交基于此)。另外最初审计了 `main` @ dbf0f49。两次都在任何 install/build/test 之前运行：
`python3 /home/user/Playground/tools/audit_repo.py /home/user/work/webdriverio-15851`（main：扫描了 1667 个文本文件；v10 的结果分类相同）。

| 命中 | 复核 | 结论 |
|---|---|---|
| `package.json` postinstall = `run-s postinstall:*` → 只有 `postinstall:husky` = `husky` | 读了 package.json 的 scripts | 无害：只安装 git hooks。安装时还用了 `--ignore-scripts` |
| `.husky/pre-commit`（main 上对暂存文件跑 eslint，v10 上跑 oxlint）、`.husky/pre-push`（`test:eslint` / `test:oxlint`） | 两个文件都读过 | 无害：只做 lint。提交时用了 `core.hooksPath=/dev/null` |
| `vitest.config.ts` 的 setupFiles：`__mocks__/fetch.ts`、`tests/setup/strictSelectors.ts`（v10） | 读过 | 无害：单元测试用的 fetch mock；另一个文件只把 `WDIO_DEFAULTS.strictSelectors.default` 设为 false |
| `e2e/vitest.config.ts` | 没有用到（没有跑 e2e） | — |
| `pnpm-workspace.yaml` 的 `allowBuilds`（v10：只有 sharp 为 true） | 读过 | 无害；并且装的时候用了 `--ignore-scripts` |
| v10 的 `AGENTS.md`、`CLAUDE.md`、`.agents/{setup,resume,skills}`、`.claude/launch.json` | 读了 AGENTS.md、CLAUDE.md、launch.json（只是 docusaurus dev server 的配置）以及 verify skill | 无害：是写给 agent 的文档。`.agents/setup` 没有执行。clone 里的 `.claude/` 不会被本会话加载 |
| powershell-download ×25：都在 `packages/webdriverio` 里 `downloadFile` 命令的实现和测试中 | 读了匹配处 | 无害：这是有文档的 WebdriverIO 浏览器命令（Selenium Grid 文件下载），不是安装时运行的代码 |
| raw-ip-url：`website/recipes/selenium-grid/selenium-grid.js` 里的 `http://172.168.0.2` | 读过 | 无害：文档示例里的 Grid 地址 |
| secret-paths：`packages/wdio-types/src/Capabilities.ts`（"Local State file"） | 读过 | 无害：关于 Chrome prefs 的文档注释 |
| 提交进仓库的二进制文件 | 无 | — |

结论：**没有发现恶意代码。**
