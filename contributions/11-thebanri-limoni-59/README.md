# thebanri/limoni #59: Sixel encoder allocates per pixel when building its palette

Status: ✅ ready (patch + PR text done, not submitted)

| Item | Value |
| --- | --- |
| Issue | https://github.com/thebanri/limoni/issues/59 |
| Tier | 新锐 |
| Labels | good first issue, graphics, performance |
| Status | open, unassigned, no comments (opened 2026-09-24 by the maintainer @thebanri) |
| Duplicate-PR check | none. The repo has 21 PRs, all closed, and none mentions sixel, palette or #59 (checked 2026-09-24) |
| Base | `main` @ `730214bd` (release: v0.9.0) |
| Patch | `0001-perf-graphics-stop-EncodeSixel-allocating-per-pixel.patch` |

## 为什么算「新锐」

- Limoni 是一个 Go 终端 UI 引擎（有 56 star）。它做的是真东西：零分配渲染的 diff、软件 3D 光栅化、四种图像协议，以及 semantic tree/MCP 自动化。它还有完整的 CHANGELOG、CI（race、零分配门禁、wasm 构建）和 benchmark 方法论文档。
- 仓库本周依然活跃：2026-09-24 发布 v0.9.0，并合并了 #54；#59 是维护者当天开的。
- 维护者是真人，而且会认真处理外部 PR：
  - #27（team-humaki）合并时维护者留言："Merged — thank you. Stripping C0 and DEL before writing OSC 2 is the right call…"，还说明了自己在合并时做的两处调整。
  - #52（costajohnt）合并时，维护者把 #46 的测试并了进来，并修了一个 io.EOF 问题。
  - 另外合并过 #25/#26/#28/#43 等外部贡献。
- 不是 issue farm：每个 issue 都给出了具体的数字和参照 PR（#54 里 EncodeKitty 的分配从 51,000 降到 42），CHANGELOG 里也记录了同样的数据。

## 问题理解

`graphics.EncodeSixel` 会先把图缩放成 `resized`，然后分两步处理：

1. `buildPalette` 用 `color.RGBAModel.Convert(img.At(x, y))` 逐像素读取，并写入 `map[color.RGBA]bool`。
2. 按 6 行一个 band 做量化，每个像素再调用一次 `resized.At(x, y)`、`pix.RGBA()`、`pal.Convert(pix)`，最后查 `map[color.Color]int`。

`image.Image.At` 每次都会把返回值装箱成 `color.Color`，也就是每个像素一次堆分配。基线 `BenchmarkEncodeSixel` 为 51,211 allocs/op、371 KB/op。issue 要求参照 #54，用 `rgbaAt` 读取像素，去掉逐像素装箱，并用 `-benchmem` 前后对比。

## 合理性判断

- 这是维护者自己开的 good first issue，符合 CLAUDE.md 和 CONTRIBUTING 的硬性原则："Zero allocations on the hot path" 和 "Use `strconv.AppendInt` / byte buffers rather than `fmt.Sprintf` in hot paths"。
- `rgbaAt` 已经存在（在 #54 中加入），直接复用即可。
- 这是纯性能改动，不改公开 API，输出逐字节一致。`buildPalette` 未导出，而且只有 `EncodeSixel` 一个调用方。

## 改动（`graphics/graphics.go`、`graphics/graphics_test.go`、`CHANGELOG.md`）

- `buildPalette` 改用 `rgbaAt` 读取像素，返回 `[]color.RGBA`（不装箱）和「颜色→下标」的 map，颜色顺序仍是首次出现顺序，最多 256 色。达到上限后直接返回；原实现达到上限后仍会继续遍历，但不再添加颜色，所以结果相同。
- 新增 `paletteIndex(pal, index, r, g, b, a)`：
  - 如果像素的 16 位值正好是 8 位值 ×0x101（`*image.RGBA` 必然满足），直接查 map。
  - 其他情况（例如 RGBA64 或 NRGBA 预乘后精度超过 8 位，或者颜色超过 256 色没进调色板），用与 `color.Palette.Index` 完全相同的最近色算法（同一个 `sqDiff`、同样的 tie-break），所以任何图像类型选出的下标都与原来一致。
- band 循环改用 `rgbaAt` 和 `paletteIndex`。
- 调色板头、`#n` 颜色切换和 `!n` 重复计数改为 `strconv.AppendInt` 写入 `bytes.Buffer`，不再用 `fmt.Sprintf`（原来每次切换颜色、每段重复都会分配一次）。
- 新增测试 `TestEncodeSixelDoesNotAllocatePerPixel`：480×384 的帧（184,320 像素）分配次数不得超过 100（修复后实际为 41）。
- 在 CHANGELOG 的 `[Unreleased]` 下加了 `### Changed` 条目（Keep a Changelog 格式）。

## 验证（Go 1.25.0，linux/amd64；均在 `/home/user/work/limoni` 中运行）

| 命令 | 结果 |
| --- | --- |
| 在 base 的 `graphics.go` 上跑新测试：`go test ./graphics -run TestEncodeSixelDoesNotAllocatePerPixel -count=1` | 🔴 FAIL: `EncodeSixel made 374229 allocations for a 480×384 frame` |
| 在修复后的代码上跑同一条命令 | 🟢 ok |
| `go test ./graphics -run '^$' -bench EncodeSixel -benchmem`（base） | 51211 allocs/op，371078 B/op，约 2.0 ms/op |
| 同一 benchmark（修复后） | **11 allocs/op**，166346 B/op，约 1.3–1.8 ms/op（共享 4 核机器，耗时有噪声） |
| 输出一致性（临时 fingerprint 测试，未提交）：5 种图像（RGBA 渐变、NRGBA 半透明、RGBA64 16 位、Gray、少色带透明）× transparent on/off × 3 种尺寸，共 30 组 `EncodeSixel` 输出的 SHA-256，以及 `buildPalette` 的结果 | 修复前后 **完全一致** |
| `gofmt -l .` | 无输出 |
| `go build ./...`、`go vet ./...` | OK |
| `go test ./...`（全仓） | 全部 ok，exit 0 |
| `go test -race ./graphics` | ok |
| `go -C tools/limonivet test ./...`，然后构建 limonivet 并运行 `limonivet ./...` | ok / 无报告 |
| `GOOS=js GOARCH=wasm go build ./examples/wasm`、`go build ./examples/3d_viewer` | OK |

未验证：没有在真实的 Sixel 终端里看效果。不过输出逐字节不变，所以渲染结果不会变。

## 如何提交

```bash
git clone https://github.com/<you>/limoni.git && cd limoni   # fork of thebanri/limoni
git checkout -b perf/sixel-palette-allocs origin/main
git am /path/to/0001-perf-graphics-stop-EncodeSixel-allocating-per-pixel.patch
git push -u origin perf/sixel-palette-allocs
# open PR against thebanri/limoni:main
```

仓库不要求 DCO 或 Signed-off-by，commit 采用 Conventional Commits 格式（`perf(graphics): ...`）。

---

## PR title

```
perf(graphics): stop EncodeSixel allocating per pixel
```

## PR body

```markdown
## Description

`EncodeSixel` read every pixel through `image.Image.At` twice: once in `buildPalette` (via
`color.RGBAModel.Convert`) and again in the band loop before quantising with `color.Palette.Convert`.
Every read boxed a `color.Color`. Colour switches and runs were also formatted with `fmt.Sprintf`.
`BenchmarkEncodeSixel` made ~51,000 allocations per frame.

This follows what #54 did for `EncodeKitty`:

- Pixels are read with `rgbaAt`.
- `buildPalette` returns `[]color.RGBA` plus each colour's index. The order is still first
  appearance, capped at 256 colours.
- A new `paletteIndex` handles quantising. For an exact 8-bit match it looks the colour up in that
  map. Otherwise (a pixel with more than 8 bits of precision, such as RGBA64 or premultiplied NRGBA,
  or a colour that didn't fit in the palette) it runs the same nearest-colour search as
  `color.Palette.Index` on the unboxed values: same `sqDiff`, same tie-breaking. So the chosen index
  is identical for every image type.
- Numbers in the escape sequence are appended with `strconv.AppendInt` instead of `fmt.Sprintf`.

The output is unchanged byte for byte. I compared SHA-256s of 30 encodings before and after:
RGBA, NRGBA with alpha, RGBA64, Gray and a sparse-colour transparent image, each with
`transparent` on and off, at three sizes.

`TestEncodeSixelDoesNotAllocatePerPixel` keeps a 480×384 frame (184,320 pixels) under 100
allocations. It now makes 41: the resize, the output buffer growing and the palette map.
The test fails on `main` with 374,229 allocations.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #59

## How it was verified

Go 1.25.0, linux/amd64:

- [x] `go test ./...` and `go vet ./...` pass. `gofmt -l .` is clean, `go test -race ./graphics` passes, and `limonivet ./...` reports nothing.
- [x] New test is red on `main` and green with the change: `go test ./graphics -run TestEncodeSixelDoesNotAllocatePerPixel`.
- [x] `GOOS=js GOARCH=wasm go build ./examples/wasm` builds.
- [ ] Rendering changes: not tried in a real Sixel terminal. The escape sequence is byte-identical to `main` (hash comparison above).
- [x] `CHANGELOG.md` is updated: a `### Changed` entry under `[Unreleased]`.
- [ ] Documentation is updated: n/a (no user-facing API or behaviour change).

## Benchmarks

`go test ./graphics -run '^$' -bench EncodeSixel -benchmem`, same machine (a shared 4-core VM, so ns/op is noisy):

| | ns/op | B/op | allocs/op |
| --- | ---: | ---: | ---: |
| `main` (730214b) | ~2,000,000 | 371,078 | 51,211 |
| this PR | ~1,300,000–1,800,000 | 166,346 | 11 |
```
