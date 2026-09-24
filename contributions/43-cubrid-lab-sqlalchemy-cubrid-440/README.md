# cubrid-lab/sqlalchemy-cubrid#440 — `String(0)` silently compiles to `VARCHAR(4096)`

| Item | Value |
|---|---|
| Issue | https://github.com/cubrid-lab/sqlalchemy-cubrid/issues/440 |
| Tier | 自由 |
| Labels | area: compiler, bug, good first issue, help wanted, size: S |
| Status | ✅ ready — patch + PR text done (2026-09-24) |
| Duplicate-PR check | Open PRs: #455 (unrelated, -493 reflection), dependabot #450–452, #374 (docs), so none for #440. Issue open, unassigned, 0 comments. Checked at the start and again right before finishing |
| Base | `main` @ 75361c09 |
| Patch | `0001-fix-compiler-reject-explicit-zero-VARCHAR-NVARCHAR-l.patch` |

## 问题理解
`CubridTypeCompiler.visit_VARCHAR` 用 `elif type_.length:` 判断长度是否给定，`length=0` 为假值，于是 `String(0)` / `VARCHAR(0)` 被当成“没指定长度”，静默编译为 `VARCHAR(4096)`。`visit_NVARCHAR` 的写法相同：`NVARCHAR(0)` 和 `VARCHAR(0, national=True)` 会变成 `NCHAR VARYING(4096)`。issue 要求区分 `None`（使用默认值）和显式 `0`，并建议对 `0` 抛出 `CompileError`，因为 CUBRID 的 VARCHAR 长度必须 ≥ 1。

## 合理性判断
- issue 由维护者（yeongseon）提出，写明了验收标准（`0` 不再变成 4096，`None` 仍使用默认值，并为两种情况加回归测试）。
- 仓库在积极维护，也合并外部 PR（例如 #445 pratipc、tayfuryldzz）。
- AI 政策：没有禁止。维护者自己的 commit 就是 agent 写的（AGENTS.md 的 commit 模板里有 Sisyphus trailer），labels 里有 `automated`（“Created or mostly authored by a bot/agent”）。`good first issue` 的 label 描述只是 “Good for newcomers”，没有“仅限人类”的限制。

## 改动
- `sqlalchemy_cubrid/compiler.py`：新增 `_reject_zero_length()`。`visit_VARCHAR` 和 `visit_NVARCHAR` 遇到 `length == 0` 时抛出 `CompileError("CUBRID does not support VARCHAR(0); ...")`，并把判断改为 `length is not None`。
- `test/test_compiler.py`：`test_varchar_zero_length_raises` 覆盖 `sa.String(0)`、`sa.Unicode(0)`、`sa.VARCHAR(0)`、`cubrid VARCHAR(0)`；`test_nvarchar_zero_length_raises` 覆盖 `sa.NVARCHAR(0)`、`cubrid NVARCHAR(0)`、`cubrid VARCHAR(0, national=True)`；另加 `test_string_no_length_uses_default`（`String()` 仍是 `VARCHAR(4096)`）。
- 文档（AGENTS.md 要求改行为时同步文档，CI 有 docs-sync 检查）：`docs/TYPES.md`、`docs/ko/TYPES.md` 补了一句说明；运行 `scripts/generate_llms_full.py` 重新生成了 `docs/llms-full.txt`（CI 有漂移检查）；`CHANGELOG.md` 的 `[Unreleased] / Fixed` 加了一条。

## 验证
环境：Python 3.11.15，venv 在 `/home/user/work/` 下，`pip install -e . pytest pytest-cov pytest-asyncio hypothesis ruff==0.16.8 mypy==2.3.1 alembic`，SQLAlchemy 2.0.54。
- Red（新测试 + 未修改的 `compiler.py`）：`pytest test/ -q -m "not integration"` → **7 failed**（都是 `DID NOT RAISE CompileError`），772 passed。
- Green：`pytest test/ -q -m "not integration" --cov=sqlalchemy_cubrid --cov-fail-under=95` → **779 passed**，132 deselected（integration），coverage 95.51%（门槛 95%）。
- `ruff check sqlalchemy_cubrid/ test/` → All checks passed；`ruff format --check` → 47 files already formatted。
- `mypy sqlalchemy_cubrid/ --config-file=pyproject.toml` → 17 errors in 5 files，**与 base 完全相同**（本地 SQLAlchemy/alembic 版本的类型问题，与本改动无关）。
- `python scripts/generate_llms_full.py` 后 `llms-full.txt` 只改了那一行，说明原本是同步的。
- 未运行：integration / compliance suite（需要 Docker + CUBRID，本环境没有）。改动只涉及 DDL 字符串编译，offline 测试已覆盖。

## 需要提交者注意
- **行为变化**：没有取值的非 native `Enum`（`sa.Enum(native_enum=False)`，SQLAlchemy 算出的 length=0）以前编译为 `VARCHAR(4096)`，现在会抛 `CompileError`。这种列什么值都存不了，风险很低，但 PR 里已经写明，是否保留旧行为由维护者决定。
- `CHAR(0)` / `NCHAR(0)` 也有类似的真值判断（会渲染成 `CHAR` / `NCHAR`），但不在本 issue 范围内（`BIT(0)` 是另一个 issue #441），PR 里作为可能的后续提了一句。
- 仓库 commit 规范是 `<type>(<scope>): ...` + 要点列表 + `Closes #N`，patch 遵守了。按 brief 的要求，**没有**加 AGENTS.md 模板里的 Sisyphus/Co-authored-by trailer（那是维护者自己的 agent）。
- PR 模板要求勾 `make check` / `make test`。上面列的是等价命令，mypy 的既有错误在 base 上也一样。
- 不需要 DCO。

## 如何提交
```bash
git clone https://github.com/cubrid-lab/sqlalchemy-cubrid && cd sqlalchemy-cubrid
git checkout -b fix/varchar-zero-length-440 origin/main
git am /path/to/0001-fix-compiler-reject-explicit-zero-VARCHAR-NVARCHAR-l.patch
git push <your-fork> fix/varchar-zero-length-440
```

## PR title
fix(compiler): reject explicit zero VARCHAR/NVARCHAR length instead of using 4096

## PR body
```markdown
## Summary

`visit_VARCHAR` and `visit_NVARCHAR` checked the length by truthiness, so an explicit `length=0` was treated like "no length given" and `String(0)` / `VARCHAR(0)` / `NVARCHAR(0)` silently compiled to `VARCHAR(4096)` / `NCHAR VARYING(4096)`. This keeps `length=None` on the documented default and raises `CompileError` for an explicit 0, as the issue suggests, since CUBRID has no zero-length VARCHAR.

One side effect to be aware of: a non-native `Enum` with no values (SQLAlchemy computes length 0 for it) used to become `VARCHAR(4096)` and now also raises. Such a column cannot hold any value anyway, but I'm happy to special-case it if you'd rather keep the old output. `CHAR(0)`/`NCHAR(0)` have a similar truthiness check (they render as bare `CHAR`/`NCHAR`); I left them alone to keep this PR to #440.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Changes

- `sqlalchemy_cubrid/compiler.py`: add `_reject_zero_length()`; `visit_VARCHAR` / `visit_NVARCHAR` raise `CompileError` for `length == 0` and use `length is not None` for the explicit-length branch
- `test/test_compiler.py`: regression tests for `String(0)`, `Unicode(0)`, `sa.VARCHAR(0)`, `VARCHAR(0)`, `sa.NVARCHAR(0)`, `NVARCHAR(0)`, `VARCHAR(0, national=True)`, plus `String()` still giving `VARCHAR(4096)`
- `docs/TYPES.md`, `docs/ko/TYPES.md`: note on explicit zero length; `docs/llms-full.txt` regenerated with `scripts/generate_llms_full.py`
- `CHANGELOG.md`: entry under `[Unreleased] / Fixed`

## Type of Change

- [x] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Chore (maintenance, dependencies, CI, etc.)

## Checklist

- [x] My code follows the project's code style (`ruff check` / `ruff format --check sqlalchemy_cubrid/ test/` clean)
- [x] I have run `make check` (lint + typecheck): ruff clean; `mypy sqlalchemy_cubrid/` reports the same 17 errors on `main` and on this branch with my local SQLAlchemy 2.0.54 / alembic 1.20, none in the changed code
- [x] I have run `make test` and all tests pass: `pytest test/ -m "not integration" --cov=sqlalchemy_cubrid --cov-fail-under=95` → 779 passed, coverage 95.51% (without the compiler change the new tests fail: 7 failed). Integration tests not run locally (no CUBRID container)
- [x] I have added tests for new functionality (if applicable)
- [x] I have updated documentation for any behavior/API/version/config change
- [x] My changes do not introduce new warnings

## Related Issues

Closes #440
```
