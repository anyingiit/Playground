# pmxt-dev/pmxt#2353 — Escrow.withdrawals 校验顺序 SDK 漂移（Python 侧）

| 项 | 值 |
|---|---|
| Issue | https://github.com/pmxt-dev/pmxt/issues/2353 |
| Tier | 新锐 |
| Labels | P2: medium, bug, component: ts-sdk, effort: small, good first issue, python, sdk-drift, sdk-parity, type: inconsistency |
| Status | ✅ ready（patch + PR 文案已写好，2026-10-01 复核） |
| 重复 PR 检查 | 2026-10-01：搜 `is:pr 2353` 无结果；搜 `withdrawals`/`escrow` 只找到 #1055（2026-06，早于本 issue，改的是 TS 侧在 withdrawals 里带 wallet，不是同一件事）；issue 无 assignee、无评论、Development 栏里没有关联 PR |
| AI 政策 | CONTRIBUTING / .github / labels 都没有禁止 AI 的规定；`good first issue` 的描述只是 "Good for newcomers" |
| Base | `main` @ 4a367d81 |

## 问题理解
TS 的 `withdrawals` 先 `resolveWalletAddress` 再检查 `include`；Python 反过来，先检查 `include`。所以在没有钱包地址、`include=""` 时，两边抛出的错误不同（TS 抛 `MissingWalletAddress`，Python 抛 `ValidationError`）。

## 合理性判断
这个 issue 是项目自己的 SDK 漂移审计开出来的，项目明确追求两个 SDK 一致（有 sdk-parity 标签）。issue 说要和 #1892（deposit_tx）的处理方式保持一致。#1892 目前还开着，但 TS 侧以及 Python 的 `approve_tx` 都是先解析地址，所以选「先解析地址」，只改 Python 一侧。TS 侧不用动。

## 改动
- `sdks/python/pmxt/escrow.py`：把 `self._wallet_address(address)` 移到 `include` 校验之前。
- 新增 `sdks/python/tests/test_escrow_withdrawals.py`，共 3 个测试：校验顺序、空 include 的报错、请求路径的构造。

## 验证
环境：venv，`pip install -e sdks/python pytest pytest-asyncio httpx black eth-account`。`pmxt_internal` 不在仓库里，先按 `core/package.json` 的 `generate:sdk:python` 用 `npx @openapitools/openapi-generator-cli generate ...` 生成到 `sdks/python/generated`（这个目录被 gitignore 了）。
- 修复前（base）：`pytest` 结果 267 passed, 66 deselected。
- 🔴 红：只把修复撤回，跑 `pytest tests/test_escrow_withdrawals.py`，结果 1 failed, 2 passed（失败的是 `test_missing_wallet_address_is_checked_before_empty_include`，抛的是 ValidationError）。
- 🟢 绿：`cd sdks/python && pytest`，结果 270 passed, 66 deselected。
- `black --check tests/test_escrow_withdrawals.py` 通过。`pmxt/escrow.py` 在 base 上就过不了 black（`_wallet_address` 里有一处字符串拼接，和本次改动无关），所以没有整体 reformat，免得 diff 里混进无关改动。CI 只在 publish 时跑 pytest，没有 lint job。
- 没跑：TS 侧的 `npm test`（这次没改 TS）；带 integration 标记的测试（需要 sidecar）。

## 需要提交者注意
- 提交作者是 anyingiit <49945850+anyingiit@users.noreply.github.com>。仓库**不需要** DCO，用 Conventional Commits。
- PR 正文里有 Claude Code 的披露段。项目没有反对 AI 的政策。
- 没写 changelog：根目录的 `changelog.md` 看起来是维护者发版时统一写的。PR 里已经说明，维护者要的话可以补。
- #1892（deposit_tx）还开着，本 PR 没碰它。如果维护者最后决定在 #1892 用「先校验参数」的顺序，可能需要调整本 PR。

## 如何提交
```bash
git clone https://github.com/anyingiit/pmxt && cd pmxt   # 先在 GitHub 上 fork pmxt-dev/pmxt
git remote add upstream https://github.com/pmxt-dev/pmxt && git fetch upstream
git checkout -b fix/python-escrow-withdrawals-validation-order upstream/main
git am /path/to/0001-fix-python-sdk-resolve-wallet-address-before-include.patch
git push -u origin fix/python-escrow-withdrawals-validation-order
gh pr create --repo pmxt-dev/pmxt --base main --head anyingiit:fix/python-escrow-withdrawals-validation-order \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`

## PR body
见 `pr_body.md`
