# 213 — PyCQA/pyflakes#548: 遮蔽内置名后 del，再用时误报 F821

| 项 | 内容 |
|---|---|
| Issue | https://github.com/PyCQA/pyflakes/issues/548 |
| 层级 | 自由（约 1.4k stars，但 flake8 依赖，使用面极广） |
| Labels | 无（2020 年报告，无评论） |
| Base 分支 | `main`（补丁基于 f0a8b98） |
| 状态 | ✅ 可提交（合并概率偏低，见下） |
| 重复检查 | 2026-10-22：无评论、无指派、无关联 PR |
| AI 政策 | 仓库无 CONTRIBUTING/AI 条款 |
| CLA/DCO | 无 |

## 问题理解
模块级 `int = 42; del int; int('42')` 被报 F821。原因：模块作用域预置 Builtin 绑定，重新赋值替换了它，`del` 直接删除名字后再无绑定。

## 改动
`Checker.handleNodeDelete`：用 `scope.pop` 取出被删绑定；若在模块作用域、名字属于内置（含自定义 builtins）、且被删的不是 Builtin 本身，则补回 `Builtin(name)`。删除从未被遮蔽的内置名维持原行为。

## 验证
- 新增 2 个测试；不带修复时都失败（红），带修复全过。
- 按 tox：`coverage run -m unittest discover pyflakes` 799 OK；`flake8 pyflakes setup.py` 通过；新代码 100% 覆盖。总覆盖 99% 是因为 root 下跳过 test_permissionDenied（基线同样如此）。

## 需要提交者注意
- 近 40 个提交全部由维护者 asottile 本人完成，另有 16 个外部 PR 挂着未处理，被合并的概率不高；可放在队列靠后。
- 提交信息风格为小写短句，已照做。NEWS 由维护者发版时写。

## 如何提交
```
git clone https://github.com/PyCQA/pyflakes && cd pyflakes && git checkout -b del-shadowed-builtin origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
另一 agent：`git am` 成功、测试/flake8 通过、红→绿确认；对 doctest、class 体、global、条件 del、F811/F401、`__all__`、star import 等对比前后输出，无误报回归。按其建议：删掉了固化旧行为的 `test_delUnshadowedBuiltin`（与 2018 年未合并的 #355 有交集），在 PR 正文说明"连续两次 del 不再报第二次"的副作用，修正测试数。结论：OK。

## 跳过原因（2026-10-22）

开 PR 时 GitHub 返回 CreatePullRequest 权限被拒：该仓库不允许 anyingiit 创建 PR。分支已推到 anyingiit 的 fork。如果以后想提交，需要先在 issue 下问维护者是否接受外部 PR，或请维护者从 fork 分支接手。
