# helix-editor/helix#11207 — 新增 Liquid 语言支持

| 项 | 值 |
|---|---|
| Issue | https://github.com/helix-editor/helix/issues/11207 |
| Tier | 高星（helix ~45k★） |
| Labels | A-language-support, C-enhancement |
| Status | ✅ 待提交（独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 21:40 UTC：`is:pr liquid OR stylus OR kmonad OR sfz` 只有无关的 kanata PR；issue 无 assignee、无关联 PR；唯一评论是用户分享的手动配置 |
| AI 政策 | 无，正文含披露 |
| Base | `master` @ ba40e54 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解 / 合理性
请求在 helix 内置 Shopify Liquid 支持。helix 常规接受新语言（语法 + 查询），twig/jinja/tera 等模板语言已有先例。

## 改动
- languages.toml：liquid 语言（.liquid，块注释 `{% comment %}`…，2 空格）+ grammar（hankthetank27/tree-sitter-liquid @ e45dbac，nvim-treesitter 用的同一个）。
- runtime/queries/liquid/highlights.scm：从上游查询改写为 helix scope（条件/循环/导入关键字细分、分隔符 punctuation.special、filter→function、doc 块、raw→markup.raw）。上游 raw_content 节点宽度为 0（用 py-tree-sitter 验证），所以改为捕获整个 raw_statement。
- injections.scm：照搬上游（html 合并注入、schema→json、style→css、javascript、front matter→yaml）。
- tests/query/highlights/liquid/tags.liquid：17 个断言；lang-support.md 由 docgen 生成。
- 不默认配置 LSP（需 Shopify CLI）。

## 验证
- `cargo xtask query-check liquid` ✓；`highlight-check liquid` 17/17 ✓；移走 highlights.scm 时 17/17 失败（红）。
- `--dump` 看了两份样例（见 /home/user/work/sample*.liquid）：各类标签、空白控制、doc、注入（json/css/js）都正常。已知小瑕疵：`{%` token 在语法里会带上前导换行（上游语法行为，不影响观感）；`reversed` 等 for 修饰词语法没做成关键字，显示为变量。

## 如何提交
```
D=$PWD/contributions/363-helix-editor-helix-11207
tools/submit_pr.sh $D helix-editor/helix master liquid-language $D/pr_title.txt $D/pr_body.md
```

## 独立复核
**PASS**（独立 agent，干净克隆 ba40e54）：git am 干净；query-check / highlight-check / docgen 无差异；所有 scope 均在 themes.md；无竞争 PR（搜 liquid / 11207）；语法与 nvim-treesitter 同 URL 同 rev，MIT；injections 与上游逐字节一致；自建样例（front matter、doc、schema/style/javascript、HTML 属性内等）dump 正确。
已采纳全部建议：liquid 块移到 languages.toml 末尾（近期新增语言惯例）；`..` 加入 @operator；nil/empty/blank → @constant.builtin；PR 正文注明 `reversed` 的语法限制。新增 3 个断言，现 17/17 绿，去掉 highlights.scm 时 17/17 红。
