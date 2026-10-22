# vyncint/termlens#586: to_svg drops underlined blank fields and writes characters XML forbids

| 项 | 值 |
|---|---|
| Issue | https://github.com/vyncint/termlens/issues/586 |
| Tier | 自由 |
| Labels | bug, good first issue |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 19:52 UTC：`repo:vyncint/termlens 586` → 0；仓库无 open PR；issue 无评论、无 assignee、Development 为空 |
| AI 政策 | 同 245：CONTRIBUTING §6 欢迎 AI 协助但**禁止 AI 署名**（commit 和 PR 正文都不要 Generated 脚注 / 🤖 / emoji），CI 强制 |
| Base | `main` @ 06cd15d |
| DCO / CLA | **需要 DCO（CI 强制）**：commit 已签；无 CLA |
| 需先认领 | 否 |
| 与 245 的关系 | 同仓库、互不依赖；两者都改 CHANGELOG `[Unreleased] → Fixed`（245 插在开头，247 追加在末尾），`git am --3way` 可叠加。先合哪个都行 |

## 问题理解
1. SVG 渲染把每个 run 的尾随空白 trim 掉，全空白的 run 直接跳过，连带下划线/删除线一起丢了——空的带下划线表单字段在 SVG 里消失（HTML 正常）。
2. `escape_xml` 只转义 `& < > "`，C0 控制符（如 OSC 0 标题里的 `\x01`）和 U+FFFF 原样写入，SVG 不合法，解析器打不开。

## 改动
- `crates/termlens/src/screen/render.rs`：有 underline/strikethrough 的 run 不 trim；`escape_xml` 把 XML 1.0 `Char` 之外的字符（除 tab/LF/CR 外的 C0、U+FFFE、U+FFFF）替换成 U+FFFD（一换一，保持列宽）。`escape_xml` 由 to_svg 和 to_html 共用，HTML 同样受益。
- `crates/termlens/tests/export.rs`：`assert_well_formed_xml`（无新依赖：检查每个字符都是 XML Char，且标签正确嵌套）+ 3 个测试：装饰空白 run、cell 中 U+FFFF、标题中 `\x01`（后者走 emit fixture，Windows 上按仓库惯例 ignore #149）。
- `CHANGELOG.md`：`[Unreleased] → Fixed`。

## 验证
- 红：只回退 render.rs → 3 个新测试失败
- 绿：恢复后 export 15 passed
- `cargo test --workspace --all-features` 全过（49 个 test result 全 ok）；clippy `-D warnings` 干净；`cargo fmt --all --check` 干净
- `check-dco.sh` / `check-no-ai-attribution.sh main..HEAD` OK
- 未做：没有引入真正的 XML 解析器（issue 说"类似 #376 那样的解析检查"；为避免新增 dev-dependency 用了轻量检查，PR 正文写明，维护者若要 roxmltree/quick-xml 可再加）

## 如何提交
```
tools/submit_pr.sh contributions/247-vyncint-termlens-586 vyncint/termlens main fix-svg-blank-runs-xml-chars contributions/247-vyncint-termlens-586/pr_title.txt contributions/247-vyncint-termlens-586/pr_body.md
```
（不要加 `--trailer`。手动：fork → `git checkout -b fix-svg-blank-runs-xml-chars origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 20:00 UTC）
- 新克隆 main@06cd15d，`git am` 干净；红（从 origin/main 回退 render.rs → 恰好 3 个新测试失败）→ 绿（export 15/15）。
- fmt / clippy（含 --no-default-features）/ `cargo test --workspace --all-features`（49 个 test binary 全 ok）/ check-dco / check-no-ai-attribution / check-readme-links 全过。
- 用 xmllint 和 expat 解析测试生成的 SVG：全部 well-formed。XML Char 集合正确（DEL/C1 合法，保留正确）。
- 竞争 PR：无（唯一 open PR #604 无关）。
- 建议并已采纳：PR 正文与 CHANGELOG 写明副作用（有文字的装饰 run 尾随空白现在也画线，与 to_html 一致）；helper 文档改为如实说明"不是完整解析"。
- 结论：PASS。
