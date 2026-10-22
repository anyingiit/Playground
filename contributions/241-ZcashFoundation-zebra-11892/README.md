# ZcashFoundation/zebra#11892: TEX addresses get an empty script / P2PKH binary encoding

| 项 | 值 |
|---|---|
| Issue | https://github.com/ZcashFoundation/zebra/issues/11892 |
| Tier | 新锐（Zcash Foundation，~2.5k★，非常活跃） |
| Labels | good first issue |
| Status | ✅ ready（只做 `script()` 部分，PR 写 "Part of #11892"） |
| 重复 PR 检查 | 2026-10-22 19:30 UTC：`repo:ZcashFoundation/zebra 11892` → 0；`Tex script` → 只有已关闭的旧 PR；issue 无评论、无 assignee、无关联 PR。相关 #11880（Display 修复，open，作者 ≠ 维护者，已被 oxarbitrage 批准）只改 Display |
| AI 政策 | **允许，需披露**（CONTRIBUTING "AI-Assisted Contributions"）：PR 里写明工具和用途；**commit 不得带 Co-Authored-By AI trailer；commit 和 PR 描述都不得带 "Generated with …" 页脚** |
| Base | `main` @ 6c0bfba |
| DCO / CLA | 均不需要 |
| 需先认领 | **建议先在 issue 评论一句**再开 PR（AGENTS.md 的“贡献闸门”要求 issue 有团队成员认可；本 issue 由维护者 oxarbitrage 本人创建并打 good first issue，满足“团队已认可这项工作”，但先评论更稳妥） |

## 问题理解
Issue 指出 `transparent::Address` 两处对 `Tex` 处理不对：
1. `script()` 对 `Tex` 返回空脚本（任何人可花）；ZIP 320 下 TEX 就是 P2PKH 目的地，应返回 P2PKH 脚本。
2. `zcash_serialize` 把 TEX 写成 P2PKH 前缀，反序列化成 P2PKH。建议改为返回 `InvalidInput` 错误并移除/弃用 `tex_address_prefix()`（breaking，issue 自己建议单独 `!` PR）。

## 合理性 / 范围选择
- 只做第 1 部分。第 2 部分依赖 #11880：当前 `Display` 仍通过 `zcash_serialize` 编码，若现在让 `Tex` 序列化报错，`Display` 会输出空缓冲的 Base58Check。#11880 合并后再做更合适；PR 的 Reviewer Notes 解释了这点。
- 现有调用：唯一非测试调用 `subsidy/check.rs` 的 funding stream 校验，而 testnet 参数构建器已拒绝 TEX 地址，所以行为对节点无影响。

## 改动
- `zebra-chain/src/transparent/address.rs`：`Address::PayToPublicKeyHash { .. } | Address::Tex { .. }` 合并分支；更新 doc comment；新增测试 `tex_script_is_p2pkh_script`（三种网络，非空且与同 hash 的 P2PKH 脚本相等）。
- `.changes/unreleased/zebra-chain-Fixed-20261022-193000.yaml`：changie 片段（`fix` 类型 PR 必需）。
- commit：`fix(chain): give TEX addresses the P2PKH script`（Conventional Commits，无 AI trailer）。

## 验证（toolchain 1.91.0，按 rust-toolchain.toml）
- 红：回退非测试改动后 `cargo test -p zebra-chain --lib -- --exact transparent::address::tests::tex_script_is_p2pkh_script` → FAILED（非空断言）
- 绿：恢复后 → 1 passed
- `cargo fmt --all -- --check` → 干净
- `cargo clippy -p zebra-chain --all-targets -- -D warnings` → 干净
- `cargo nextest run -p zebra-chain` → 341 passed, 0 skipped
- 未跑：workspace 全量 nextest / clippy（只改了 zebra-chain 一个私有分支逻辑，其他 crate 不调用 Tex 的 script()）

## 需要提交者注意
- **PR 正文不要加 "🤖 Generated with Claude Code" 页脚**（AGENTS.md 明令禁止）；AI 披露写在模板的 “AI Disclosure” 段（pr_body.md 已写好）。项目归属标记行如需保留请放在最前，但不要加 Generated-with 页脚。
- PR 模板（Summary / Reviewer Notes / Evidence / Merge Danger / AI Disclosure）已按 zebra-pr skill 填好。
- 建议开 PR 前在 issue 下评论："I'd like to take the `script()` part of this; the serialization part seems better after #11880. PR coming shortly."

## 如何提交
```
tools/submit_pr.sh contributions/241-ZcashFoundation-zebra-11892 ZcashFoundation/zebra main tex-p2pkh-script contributions/241-ZcashFoundation-zebra-11892/pr_title.txt contributions/241-ZcashFoundation-zebra-11892/pr_body.md
```
（手动：fork → `git checkout -b tex-p2pkh-script origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 19:55 UTC）
- 上游：#11892 open、未指派、无评论；PR 搜索 `11892` / `TEX script is:open` → 0。#11880 仍 open（已获批准），其 Development 栏关联了 #11892：若 #11880 合并时自动关闭 #11892，本 PR 写 "Part of" 仍然正确，但提交时留意 issue 状态。
- 新浅克隆 `git am` 干净；作者 anyingiit noreply；无 Co-Authored-By。
- 红→绿确认；fmt / clippy -p zebra-chain 干净；`cargo nextest run -p zebra-chain` 341/341。
- 代码符合 ZIP 320；changie 片段格式与现有一致；PR 正文符合模板与 zebra-pr skill，无 Generated-with 页脚。
- 结论：PASS（提醒：提交时不要加 "Generated with Claude Code" 页脚）
