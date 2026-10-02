# grpc-ecosystem/grpc-gateway #2824 — Replace openapiv2 path template parser with httprule parser

| 项 | 值 |
|---|---|
| Issue | https://github.com/grpc-ecosystem/grpc-gateway/issues/2824 |
| Tier | 高星（grpc-gateway，约 19k stars） |
| Labels | enhancement, help wanted |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 仍 open，无人分配，也没有评论。`pulls?q=2824` 只搜到 #2825（2022 年合并，是另一个 verb 修复，PR 里维护者写了 "ideally we'd unify these two parsers (see #2824)"）。关键词 `httprule openapiv2 parser` 只搜到 #1947（2021）。#7191（2026-08 合并）只修了 path 拼接，没有统一 parser。没有 open 的重复 PR。 |
| Base | `main` @ 80a27b1（2026-10-01） |

## 问题理解
仓库里有两套 http.proto 路径模板解析器：`internal/httprule`（给 protoc-gen-grpc-gateway 生成 handler 用）和 `protoc-gen-openapiv2/internal/genopenapi` 里手写的下推自动机（`templateToParts` + `processParametersInSegment`）。issue 由维护者 johanbrandhorst 开，要求 openapiv2 也改用 httprule 的解析器，让两个生成器的结果一致。

## 合理性判断
- 维护者自己提的 issue，标了 help wanted，#2825 里也明确说过想统一这两个 parser。
- 相关的 #2833（httprule 接受规范外模板的问题）维护者倾向于"不收紧 httprule，让 openapiv2 更健壮"。本改动没有动 httprule 的解析规则，只新增了一个只读的导出函数，和 #2833 不冲突。
- 真实流程里，`templateToParts` 收到的模板一定已经被 `httprule.Parse` 校验过（`internal/descriptor/services.go` 加载 registry 时就会解析，解析失败直接报错）。所以旧 parser 额外"容忍"的写法（缺开头的 /、结尾 /、`/foo/:bar`）在实际生成中根本到不了这里，只出现在单元测试里。

## 改动
- `internal/httprule/parse.go`：新增导出类型 `Segment{FieldPath, Value}` 和 `SplitTemplate(tmpl) ([]Segment, verb, error)`；`Parse` 改为调用内部 `parse`，返回值不变。
- `genopenapi/template.go`：`templateToParts` 改用 `SplitTemplate`，输出格式保持不变（首项 ""、`{name}`/`{name=pattern}`、末项 `:verb`）。删除 `processParametersInSegment`。模板以 ":" 结尾时，httprule 解析出的 verb 为空，这里保留这个冒号，让既有测试 `TestRenderServicesWithColonLastInPath` 继续通过。
- `genopenapi/BUILD.bazel`：加 `//internal/httprule` 依赖。
- 测试：新增 `TestSplitTemplate`；`TestTemplateToOpenAPIPath` 增加 `/`、`/:customMethod`、`/v1/a:b:customMethod`、`/v1/{name=**}`；`TestFQMNToRegexpMap` 增加 `/{test=*}`。httprule 会拒绝的旧测试输入已调整：camel-case 用例补上开头的 /，expand-slashed 用例去掉结尾的 /，删除 `/{test1}/{test2}/`（两处）、`/test/{name=*}/`、`/{name=prefix/*}/:customMethod`、`/foo/:bar`。
- 唯一的可见行为变化：显式写 `{name=*}` 时，不再生成多余的 `pattern: "[^/]+"`，和 `{name}` 一样处理（gateway 本来也把两者当成同一个）。仓库里没有任何 proto 用到 `{x=*}`。

## 验证（Go 1.26.0，GOCACHE/GOMODCACHE 在 /home/user/work 下，GOFLAGS=-p=2）
- Red（`git stash` 掉 parse.go / template.go / BUILD.bazel，只保留新测试）：`go test ./internal/httprule/ ./protoc-gen-openapiv2/internal/genopenapi/` 结果：httprule 编译失败（`undefined: SplitTemplate`）；genopenapi 的 `TestFQMNToRegexpMap` 失败（`/{test=*}` 得到 `map[test:[^/]+]`）。
- Green：两个包都 ok。
- `go test ./internal/... ./protoc-gen-openapiv2/... ./protoc-gen-grpc-gateway/... ./protoc-gen-openapiv3/...`：全部 ok。
- `go tool staticcheck ./internal/httprule/ ./protoc-gen-openapiv2/...`（CI 的 lint job 用的就是 staticcheck）：无输出。`gofmt -l internal protoc-gen-openapiv2`：无输出。`go build ./...`：ok。
- 差分验证（临时测试，未提交）：把旧 `templateToParts` 拷进测试，用仓库里 .proto/.yaml 中出现的全部 145 个不同路径模板，分别在 json_names 开/关两种设置下对比新旧实现的 OpenAPI path 和 regexp map，结果全部一致。
- `go vet ./protoc-gen-openapiv2/internal/genopenapi/` 会报 template_test.go:12993 "copies lock"，这是 base 上已有的问题，和本改动无关（CI 不跑 go vet）。
- **没有运行**：Bazel（`bazel test`/gazelle）、`make generate`、buf lint。BUILD 只手工加了一行 gazelle 也会加的依赖，没有生成文件需要更新。

## 需要提交者注意
- 仓库没有 AI 政策（CONTRIBUTING、.github、labels 都查过），不要求 DCO。labels 里有历史遗留的 `cla: yes/no`，如果 PR 上出现 Google CLA 检查，需要先签 CLA。
- PR 正文按仓库模板写（References / Contributing Guidelines / Brief description / Other comments），里面嵌入了 chefs-pick 格式的各节。
- 删除了 #7191 加的两个用例（`/{name=prefix/*}/:customMethod`、`/foo/:bar`），因为 `httprule.Parse` 会拒绝这两个模板，生成器实际上收不到它们。PR 正文已说明；如果维护者希望保留，可以改成直接对 `partsToOpenAPIPath` 做测试。
- 显式 `{name=*}` 不再生成 pattern 的行为变化，PR 正文已说明。
- 按模板要求，开 PR 后建议在 issue 下留言链接这个 PR。

## 如何提交
```bash
git clone https://github.com/grpc-ecosystem/grpc-gateway && cd grpc-gateway
git checkout -b openapiv2-httprule-parser origin/main
git am /home/user/Playground/contributions/090-grpc-ecosystem-grpc-gateway-2824/0001-Use-the-httprule-parser-for-openapiv2-path-templates.patch
go test ./internal/... ./protoc-gen-openapiv2/... && go tool staticcheck ./...
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/090-grpc-ecosystem-grpc-gateway-2824 grpc-ecosystem/grpc-gateway main openapiv2-httprule-parser contributions/090-grpc-ecosystem-grpc-gateway-2824/pr_title.txt contributions/090-grpc-ecosystem-grpc-gateway-2824/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
