# AUDIT: higher-kinded-j/higher-kinded-j (main @ ac42282)

只运行了 `hkj-book/check.sh`（node 脚本、python 脚本、npm ci 安装 mermaid-check 的锁定依赖、fetch_mermaid.sh 下载 mermaid.min.js）。未跑 Gradle。仓库有 .claude/skills 且接受 Cursor Agent 提交，无 AI 禁令；PR 模板已按结构填写；无 CLA/DCO。

扫描结论：gradle-wrapper.jar 是标准 Gradle wrapper；secret-paths 三条都是注释里的 "local state" 误报。

# Audit: /home/user/work/hkj  (3071 text files scanned)

## Auto-executing surface (install/build/test hooks)
- -: none

## npm lifecycle hooks
- -: none = 

## Committed binaries
- gradle/wrapper/gradle-wrapper.jar (45633 bytes)

## Pattern findings

### secret-paths (3)
- hkj-examples/src/test/java/org/higherkindedj/tutorial/effect/Tutorial02_EffectPathAdvanced.java:66: `*   <li>Use {@link MutableContext} to maintain workflow-local state.`
- hkj-examples/src/test/java/org/higherkindedj/tutorial/effect/Tutorial02_EffectPathAdvanced.java:272: `* Exercise 5: {@link MutableContext} — workflow-local state.`
- hkj-benchmarks/src/jmh/java/org/higherkindedj/benchmarks/ConcurrencyScalingBenchmark.java:29: `*   <li>Thread-local state isolation should be maintained`
