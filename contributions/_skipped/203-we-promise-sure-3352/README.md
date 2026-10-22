# we-promise/sure#3352 — Super admin household member cannot split transactions（跳过）

- Issue: https://github.com/we-promise/sure/issues/3352 （open，无 assignee，label: bug；2026-10-22 检查无相关 PR）
- Status: ⏭️ skipped

## 跳过原因
1. **无法本地 red→green**：Rails 测试需要 PostgreSQL（+ Redis/Sidekiq），本机无 `psql`/`pg_ctl`/`redis-server`，Homebrew 也未安装；按要求不安装系统服务，因此无法跑 `bin/rails test`。
2. **需要设计决策**：唯一评论（jimmyface）指出根因不是 split 本身，而是账户默认不共享给其他 super admin——是否让 super admin 绕过账户共享（account sharing / AccountShare 权限）是产品/安全层面的决定，issue 本身还在 "Details to confirm" 阶段（是隐藏、禁用还是报错均未确认），维护者尚未表态。

## 若日后再做
- 先请维护者确认期望行为（super admin 是否应对同 family 的所有账户有写权限，或仅修 split 的授权检查）。
- 需要带 Postgres 的环境运行 `bin/rails test test/controllers/transactions/*split*` 之类测试。
