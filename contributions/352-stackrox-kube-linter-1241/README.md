# stackrox/kube-linter#1241

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/stackrox/kube-linter/issues/1241 — env-value-from misses envFrom and volume-mounted ConfigMap/Secret references |
| Tier | 自由 |
| Labels | 无（issue 未打标签） |
| Status | ✅ ready — patch + PR 文本已完成，测试 red→green，lint 通过 |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=1241`、`/pulls?q=envFrom` 均无相关 PR；issue 无评论、无 assignee |
| Base | `main` @ e23dee8 |

## 问题理解
`env-value-from` 文档称检测"使用了不在部署中的 secret/configmap"，但实现只看 `env[].valueFrom`。通过 `envFrom`（整体注入）或 pod `volumes` 挂载的 ConfigMap/Secret 不存在时不报错。issue 建议扩展现有检查或新建 `dangling-*` 检查。

## 合理性判断
合理：属于该检查宣称范围内的遗漏。该检查默认不启用，扩展只影响主动开启的用户。最近 #1249（命名空间匹配）也是对同一检查的修复，维护者接受此类改动。未发现 AI 禁令（CONTRIBUTING/labels 无相关规则；有一个无描述的 `ai-review` 标签）。

## 改动
- `pkg/templates/envvarvaluefrom/template.go`：
  - 增加 `container.EnvFrom[].ConfigMapRef/SecretRef`：只检查对象存在（key 为空）。
  - 新增 `lintVolumes`：pod 级 `volumes[].secret/configMap`，检查对象存在，并检查 `items` 中列出的 key；对象缺失只报一次。
  - `optional: true`、`IgnoredSecrets/IgnoredConfigMaps`、命名空间匹配沿用原逻辑。
  - `checkResourceReference` 改为接收 subject（`container "x"` / `volume "y"`），原有消息文本不变。
  - 模板描述加上 "or volumes"。
- `template_test.go`：新增 `TestEnvFromReferences`、`TestVolumeReferences`。
- `tests/checks/env-var-value-from.yml` + `e2etests/bats-tests.sh`：新增 envFrom + volume 用例，期望报告数 4→6。
- `docs/generated/templates.md`：用构建出的二进制重新生成（checks.md 无变化）。
- 未覆盖 projected volume（PR 中已说明，可按维护者要求补）。

## 验证
- Red：仅还原 template.go，`go test ./pkg/templates/envvarvaluefrom/` → `TestEnvFromReferences`、`TestVolumeReferences` FAIL。
- Green：`go test ./pkg/templates/envvarvaluefrom/...` → ok。
- `go test ./pkg/... ./internal/... ./docs/... ./cmd/...` → 全部 ok（`pkg/lintcontext` 的 `TestCreateContextsWithIgnorePaths` 第一次失败是因为我把 GOCACHE/GOMODCACHE 放在仓库内，移出后通过，与改动无关）。
- `golangci-lint run ./pkg/templates/envvarvaluefrom/...`（tool-imports 中锁定版本）→ 0 issues。
- `KUBE_LINTER_BIN=<built> bats e2etests/bats-tests.sh -f env` → 4/4 ok。
- `gofmt -l` 对改动文件无输出。

## 需要提交者注意
- 仓库不要求 DCO（人类 PR 无 Signed-off-by），也没有 AI trailer 要求，故未加。
- commit 作者：anyingiit <49945850+anyingiit@users.noreply.github.com>，Conventional 风格 `fix: ...`，正文含 `Fixes #1241`。
- 仓库无 PR 模板、无 CHANGELOG。
- PR body 中注明了 projected volume 未覆盖；若维护者更想要单独的 `dangling-*` 检查，需要重做。

## 如何提交
```bash
git clone https://github.com/<you>/kube-linter && cd kube-linter
git checkout -b env-value-from-envfrom-volumes origin/main
git am /path/to/0001-fix-check-envFrom-and-volume-references-in-env-value.patch
git push -u origin env-value-from-envfrom-volumes
# 或在 Playground 中：
tools/submit_pr.sh contributions/352-stackrox-kube-linter-1241 stackrox/kube-linter main env-value-from-envfrom-volumes contributions/352-stackrox-kube-linter-1241/pr_title.txt contributions/352-stackrox-kube-linter-1241/pr_body.md
```

PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。
