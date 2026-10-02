# zitadel/oidc #967 — content-type not checked during discovery

| 项 | 值 |
|---|---|
| Issue | https://github.com/zitadel/oidc/issues/967 |
| Tier | 自由 (~1.7k stars) |
| Labels | 无 (Bug type) |
| Status | ✅ ready |
| 重复 PR 检查 | 2026-10-01: /pulls?q=967 与 `content-type` 关键词搜索均无相关 open/merged PR；issue 未分配、无评论认领、时间线无关联 PR |
| Base | `main` @ 7cf807b |

## 问题理解
OIDC Discovery 1.0 §4.2 要求 provider configuration 响应使用 `application/json`。`client.Discover()` 通过 `httphelper.HttpRequest()` 发请求，完全不检查 `Content-Type`。

## 合理性判断
规范明确要求（MUST），issue 指出了具体代码位置，合理。仓库无 AI 贡献禁令（CONTRIBUTING / .github / labels 均未提及）。

## 改动
- `pkg/http/http.go`: 新增 `HttpJSONRequest`（与 `HttpRequest` 相同，但 200 响应必须是 `application/json`，用 `mime.ParseMediaType` 解析，允许 charset 参数与大小写差异）；两者共享内部 `httpRequest`。`HttpRequest` 行为不变。
- `pkg/http/errors.go`: 新增 `ErrInvalidContentType`。
- `pkg/client/client.go`: `Discover` 改用 `HttpJSONRequest`，错误仍与 `oidc.ErrDiscoveryFailed` join。
- 测试：新增 `TestDiscover_ContentType`；`rp/relying_party_test.go` 中 3 个 httptest discovery 服务器补上 `Content-Type: application/json`（否则 Go 会嗅探为 `text/plain`）。

## 验证
- Red（无修复，仅测试）：`go test ./pkg/client/ -run TestDiscover_ContentType` → missing / text/plain / text/html 三个子用例 FAIL（期望 ErrDiscoveryFailed，得到 nil）。
- Green：`go test -race ./pkg/...` → 全部 ok（与 CI `release.yml` 相同的包集合）。
- `go vet ./pkg/client/... ./pkg/http/... ./example/...` 无输出；`gofmt -l pkg/client pkg/http` 无输出（`pkg/oidc/jwt_profile.go` 在 main 上本来就未 gofmt，与本改动无关）。
- 注意：`TestDiscover/spotify` 会访问外网 accounts.spotify.com（本地通过）。

## 需要提交者注意
- **行为变更**：对返回错误 content-type 的不合规 OP，discovery 将失败。PR body 已说明并表示可改为可选项；若维护者要求，可加一个 option。
- PR 标题须符合 `.github/semantic.yml`（`fix(client): ...` 合规，titleOnly 校验）。
- 不需要 DCO / AI trailer。PR body 采用了仓库模板的章节（Which Problems / How / Additional Changes / Additional Context）并嵌入 brief 的 disclosure 与 checklist。
- commit 作者：anyingiit <49945850+anyingiit@users.noreply.github.com>。

## 如何提交
```bash
tools/submit_pr.sh contributions/074-zitadel-oidc-967 zitadel/oidc main fix/discovery-content-type contributions/074-zitadel-oidc-967/pr_title.txt contributions/074-zitadel-oidc-967/pr_body.md
```
手动方式：fork 后 `git checkout -b fix/discovery-content-type origin/main && git am 0001-*.patch && git push`，然后以 `pr_title.txt` / `pr_body.md` 开 PR（base `main`）。

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。
