# AUDIT — shadcn-labs/pdfcn @ 39c75c1

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pdfcn` (632 text files scanned)

| 项 | 结果 |
|---|---|
| Auto-executing surface | none |
| npm lifecycle hooks | root `prepare = lefthook install`; `apps/web` `postinstall = fumadocs-mdx` |
| Committed binaries | none |
| Pattern findings | none |

## 人工复核

- `prepare: lefthook install` — 仅在本地 `.git/hooks` 安装 lefthook 钩子；`lefthook.yml` 的 pre-commit 只运行 `pnpm fix {staged_files}`（ultracite 格式化）。无网络/外传行为。安装时设置 `LEFTHOOK=0` 跳过。
- `apps/web postinstall: fumadocs-mdx` — fumadocs 官方 CLI，读取 `source.config.ts` 生成 `.source/` 类型/索引文件；`source.config.ts` 只配置 rehype-pretty-code 和 docs 目录。安全。
- `pnpm-workspace.yaml` 的 `onlyBuiltDependencies` 只允许 `lefthook` 运行依赖构建脚本，其余三方包的 install 脚本不会执行。
- `.cursor/hooks.json` — 仅 Cursor 编辑器在文件编辑后运行 `pnpm fix`，本环境不触发。
- `apps/web/scripts/build-registry.mts`（`pnpm registry:build`）— 调用 `shadcn build` 后读写 `registry.json` / `public/r/*.json`，重写 import 路径并校验依赖闭包；无网络、无 shell 拼接。

结论：**未发现恶意代码**，可以安装与构建（`LEFTHOOK=0`，store 放在 clone 内）。
