# ruby/rdoc#1782 — C parser makes a class its own superclass when a variable is reused

| 项 | 值 |
|---|---|
| Issue | https://github.com/ruby/rdoc/issues/1782 |
| Tier | 高星（ruby/rdoc） |
| Labels | 无 |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~20:40 UTC：issue 无评论/assignee；#1785（tompng，已合）只修了无限递归，没修父类错误；open PR 中无引用 1782 或 rb_const_get 的。**#1831（open）改了同一行 `parent_name = ...`**，后合者需小 rebase，正文已说明 |
| AI 政策 | 仓库 AGENTS.md：PR 正文 2–4 段、无 Test plan、**不加 AI 署名**。本正文照此写，提交时不要补 disclosure 段 |
| Base | `master` @ 0b82ffd |
| DCO / CLA / CHANGELOG | 无 |
| 需先认领 | 否 |
| 注意 | 与 277 同仓库，互不冲突（277 改 stats.rb，278 改 parser/c.rb、store.rb） |

## 改动
- `Parser::C#const_get_name`：父类变量未知时，在文件里找 `var = rb_const_get(_at)(under, rb_intern(_const)("Name"))`；只有唯一一种赋值时才采用（`rb_cObject` → `Name`，其他已知模块 → `Under::Name`），多处赋不同常量就放弃，保留变量名。
- `Store#resolve_c_superclasses`：不再把类解析成自己的父类（issue 里提的最低修复）。

## 验证
- c_test 110/0、store_test 89/0；回退 lib/ 后 3 个新测试失败。全量 2559，仅两个环境性失败（root、US-ASCII），与 master 相同。rubocop 无告警。
- issue 样例：`Example::Socket < Example::Socket` → `< Socket`。
- kgio 真实源码：Kgio::Socket/TCPSocket/TCPServer/UNIXSocket/UNIXServer 都得到正确父类；Ruby 自身 ext/*.c 182 个类父类前后一致，耗时不变。

## 如何提交
```
tools/submit_pr.sh contributions/278-ruby-rdoc-1782 ruby/rdoc master c-const-get-superclass contributions/278-ruby-rdoc-1782/pr_title.txt contributions/278-ruby-rdoc-1782/pr_body.md
```

## 独立复核（2026-10-22，独立 agent，两轮）
- 第一轮 FAIL：首次匹配胜出，变量被多次赋值时会静默给出错误父类（`A::Y < IO`）→ 改为唯一性判断并加测试；建议正文提 #1831 冲突 → 已加。
- 第二轮 PASS：全部复现（含 kgio、Ruby ext 对比、multi.c），正文符合 AGENTS.md。
