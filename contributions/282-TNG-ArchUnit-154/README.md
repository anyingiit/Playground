# TNG/ArchUnit#154 + #190 — deny-list layer constraints (`mayNotAccessLayers` / `mayNotBeAccessedByLayers`)

| 项 | 值 |
|---|---|
| Issues | https://github.com/TNG/ArchUnit/issues/154 , https://github.com/TNG/ArchUnit/issues/190 （相关已关闭 #1372） |
| Tier | 高星（ArchUnit ~3.5k★，TNG 维护，今天还有提交） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~21:00 UTC：两个 issue 都无关联 PR；PR 搜索 `mayNot`/方法名无结果。#154 自 2021 年分配给 GiorgadzeLuka，但他只做了白名单部分（#592 已合并），正文里已礼貌说明 |
| 维护者态度 | #190 里 codecholeric 说偏好白名单，但"没有拒绝的理由，欢迎 PR"；#154 里约定先做白名单、黑名单以后再看。Javadoc 已说明白名单更安全 |
| AI 政策 | 无 AGENTS.md / PR 模板；CONTRIBUTING 无 AI 条款。正文保留 Motivation + Disclosure 段 |
| Base | `main` @ 5f0884eb |
| DCO | **需要**：提交时用 `--signoff`（补丁已带 Signed-off-by，`--signoff` 不会重复） |
| CLA / CHANGELOG | 无 |
| 需先认领 | 否 |

## 改动
`LayerDependencySpecification` 新增 `mayNotAccessLayers(String...)` 和 `mayNotBeAccessedByLayers(String...)`：只禁止与指定层之间的依赖，其他依赖（包括与不属于任何层的类）都允许。复用 `ifDependencyIsRelevant`，所以 dependency settings 和 `ignoreDependency` 照常生效；参数检查与白名单方法相同，另外拒绝把自身层列进去。

## 验证
- 只有 JDK 21（构建默认要 JDK 25 toolchain），用 `-PtestJavaVersion=21 -x compileJdk25testJava`。
- LayeredArchitectureTest 31/0（含 3 个新测试）；没有主代码时新测试编译不过（红）；断言是精确匹配，白名单式错误实现会多报 Origin→Allowed/Object 而失败。
- 复核前跑过 `:archunit:spotlessCheck :archunit:architectureTest :archunit:test` 全量：15896 个测试 0 失败；采纳复核建议后重跑 spotlessCheck + LayeredArchitectureTest 通过。

## 如何提交
```
tools/submit_pr.sh contributions/282-TNG-ArchUnit-154 TNG/ArchUnit main layer-deny-lists contributions/282-TNG-ArchUnit-154/pr_title.txt contributions/282-TNG-ArchUnit-154/pr_body.md --signoff
```

## 独立复核（2026-10-22，独立 agent）
- PASS：新克隆干净应用，测试 31/0 复现；方向（ORIGIN/TARGET）、dependency settings、ignoreDependency、多个 whereLayer、optional layer 都检查过；提交信息符合 CONTRIBUTING（小写祈使、<70 字符、DCO、`Resolves:`）。
- 采纳：① 层禁止自身会把层内依赖全报出 → 现在直接拒绝并加测试；② ORIGIN 方向缺"层外类访问"用例 → 测试去掉 Allowed 层，使其成为层外类，验证不报；③ 正文说明 #154 的旧 assignee。
- 未改：用户指南只举一个例子、也没列白名单方法，不需要改文档。
