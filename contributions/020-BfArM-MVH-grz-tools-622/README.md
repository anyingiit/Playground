# BfArM-MVH/grz-tools#622 — Database configuration masks password with `***`

| Item | Value |
|---|---|
| Issue | https://github.com/BfArM-MVH/grz-tools/issues/622 |
| Tier | 自由 |
| Labels | good first issue, priority: low, type: bug |
| Status | ✅ ready (patch + PR text), not submitted |
| Base | `main` @ `6ed9cb04bede9fc9b34b7ce6d3aa9a0df9d42ae4` (2026-09-24) |
| Duplicate-PR check | Issue has no assignee, comments, linked PRs or branches (re-checked at the end). Fetched every open/recent PR head #624–#694 via `refs/pull/*/head`: none change the line; no PR > #694 existed at the final re-check. |

## 问题理解

`grz-db` 的 `SubmissionDb._get_alembic_config()` 用
`alembic_cfg.set_main_option("sqlalchemy.url", str(self.engine.url))` 把数据库 URL 交给 Alembic。
SQLAlchemy 2.x 的 `str(URL)` 等价于 `render_as_string(hide_password=True)`，密码被替换为 `***`。
Alembic 的 `migrations/env.py` 再用这个 URL 建 engine 连接，所以所有走 Alembic 的操作
（`initialize_schema` / `db init` / `db upgrade` / 首次写入前的 schema 检查 `_at_latest_schema`）
在有密码的数据库（生产 PostgreSQL）上都会以密码 `***` 登录 → 认证失败。
测试夹具用 sqlite 或 `trust` 认证的 PostgreSQL（无密码），所以现有测试发现不了。

修 issue 时发现的第二个坑：Alembic 的 `Config` 基于 `ConfigParser`（有插值），`set_main_option`
文档要求 `%` 写成 `%%`。含特殊字符的密码经 URL 编码后会出现 `%xx`（如 `%` → `%25`），
不转义会抛 `ValueError: invalid interpolation syntax`。所以修复里一并转义。

## 合理性判断

- 明确的 bug，维护者自己标了 `type: bug` + `good first issue`；代码在 main 上仍存在（位置已从 issue 里的第 574 行移到第 1068 行）。
- 修复最小（3 行），不改公共 API。
- AI 政策：CONTRIBUTING.md / .github / AGENTS 等 grep `LLM|AI-generated|Copilot|ChatGPT|generative AI|claude`：无任何 AI 相关规定。
- 维护活跃（近一周多次合并）；贡献者除核心维护者外还有 Virag Sharma、Jo Chen、beoinformatics 等（可能属合作机构，无法确认是否"纯外部"）。issue 标 good first issue 表示欢迎外部贡献。

## 改动

- `packages/grz-db/src/grz_db/models/submission/__init__.py`：
  `render_as_string(hide_password=False)` 代替 `str()`，并 `.replace("%", "%%")` 适配 ConfigParser 插值。
- `packages/grz-db/tests/test_submission.py`：新增参数化回归测试
  `test_alembic_config_keeps_the_database_password[s3cret | s3cr%et]`，断言 Alembic 配置里的 URL 解析后密码不变。
  （仅构造 engine，不连库，psycopg 本就是 grz-db 依赖。）
- 无需手写 CHANGELOG：仓库用 release-please 根据 Conventional Commit 的 PR 标题/squash message 自动生成。

## 验证

环境：`uv 0.12.18`（仓库要求 uv ≥ 0.11.22）、Python 3.12，只安装 grz-db：
`uv sync --package grz-db --group test --group lint --python 3.12`（未编译 Rust 的 grz-check）。

1. 复现（修复前）：
   `SubmissionDb('postgresql+psycopg://alice:s3cr%25et@db.example:5432/grz', author=None)._get_alembic_config().get_main_option('sqlalchemy.url')`
   → `'postgresql+psycopg://alice:***@db.example:5432/grz'`
2. Red → green：`pytest -n0 packages/grz-db/tests/test_submission.py -k alembic_config`
   - 修复前：2 failed（`assert '***' == 's3cret'` / `'s3cr%et'`）
   - 只做 `render_as_string` 不转义 `%`：1 passed, 1 failed（`ValueError: invalid interpolation syntax ... position 29`）→ 证明转义必要
   - 完整修复：2 passed
3. 端到端（真实带密码的 PostgreSQL 16，`initdb --auth=scram-sha-256`，密码 `p%w d!`，以非 root 用户启动）：
   `SubmissionDb(url_with_password).initialize_schema()`
   - base：`RuntimeError: Alembic upgrade failed: (psycopg.OperationalError) ... FATAL: password authentication failed for user "grz"`
   - 修复后：`initialize_schema OK`
4. grz-db 全量测试（sqlite + PostgreSQL 两个后端；因 initdb 不能以 root 运行，用非 root 用户执行）：
   `pytest -q -n 2 -p no:cacheprovider packages/grz-db/tests` → **334 passed, 1 skipped**
   （以 root 跑时 PostgreSQL 参数化用例会因 `initdb` 拒绝 root 而 error，与本改动无关。）
5. Lint/format/type：`ruff format --check` → 215 files already formatted；`ruff check` → All checks passed；
   `mypy -p grz_db` → Success: no issues found in 25 source files（base 同样通过）。
   未运行：其他包（grzctl / grz-cli / grz-common / grz-check）的测试与全仓 mypy（未安装这些包；改动只涉及 grz-db）。

## 如何提交

```bash
git clone https://github.com/<you>/grz-tools && cd grz-tools
git checkout -b fix/alembic-url-password origin/main
git am /path/to/0001-fix-grz-db-pass-the-unmasked-database-URL-to-alembic.patch
git push -u origin fix/alembic-url-password
# open PR against BfArM-MVH/grz-tools:main
```

### 需要提交者注意

- **PR 标题必须是带 scope 的 Conventional Commit**（`check-pr.yml` 用 action-semantic-pull-request，`requireScope: true`，scope 在白名单内）：用下面的标题 `fix(grz-db): ...`。
- 仓库 PR 模板要求"把 PR 描述替换为最终 squash commit message"（release-please 会从中读取）。下面的 PR body 以 commit message 风格开头，末尾附了披露段落；若维护者希望 body 只含 commit message，可把披露段落移到一条评论里。
- 仓库无 AI 政策；无 DCO / Signed-off-by 要求（近期 commit 均无）。commit 中无 AI 署名。

## PR title

```
fix(grz-db): pass the unmasked database URL to alembic
```

## PR body

```markdown
## Description

fix(grz-db): pass the unmasked database URL to alembic

`SubmissionDb._get_alembic_config` handed `str(self.engine.url)` to Alembic. SQLAlchemy renders a URL's password as `***` in `str()`, so every Alembic-backed operation (`initialize_schema` / `db init`, `db upgrade`, and the schema check that runs before the first session) connected with the literal password `***` and failed to authenticate against a password-protected database. The test fixtures use sqlite or a trust-auth PostgreSQL, which is why this didn't show up in CI.

The URL is now rendered with `render_as_string(hide_password=False)`. It is also escaped (`%` → `%%`) before `set_main_option`, because Alembic's `Config` is a `ConfigParser` with interpolation: a URL-encoded password (e.g. one containing `%`, encoded as `%25`) would otherwise raise `ValueError: invalid interpolation syntax`.

A parametrized regression test checks that the password survives in the Alembic config, both for a plain password and for one containing `%`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #622

## Checklist

- [x] Tests pass locally (`uv sync --package grz-db --group test --group lint`; `pytest packages/grz-db/tests` → 334 passed, 1 skipped, sqlite + PostgreSQL backends; the new test fails on `main` with `assert '***' == 's3cret'`; `ruff format --check`, `ruff check`, `mypy -p grz_db` clean). Also checked end-to-end against a local PostgreSQL 16 with scram-sha-256 auth: `initialize_schema()` fails with "password authentication failed" on `main` and succeeds with this change.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, generated by release-please from the PR title
- [ ] Documentation is updated (if applicable) — n/a, bug fix only
```
