## Description

`Encoder::set_palette` accepted any byte slice and the encoder wrote it into `PLTE` unchanged, so a palette of e.g. 1024 bytes produced a file that pngcheck rejects ("invalid number of PLTE entries"). `write_header` now returns a format error (`InvalidPaletteLength`, checked next to the existing width/height/colour-type checks) when the palette is empty, longer than 256 entries, or not a multiple of 3 bytes. I went with an error rather than the `assert!` suggested in the issue so it matches how the encoder already reports other invalid header input; happy to switch to a panic if you prefer.

A regression test covers the invalid lengths (0, 4, 771 and 1024 bytes) and the two valid boundaries (3 and 768 bytes); it fails without the fix. Also added a `CHANGES.md` entry and a note on `set_palette`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #584

## Checklist

- [x] Tests pass locally (`cargo test --workspace --all-targets`: all pass, lib 102 passed / 1 ignored; `cargo test --doc`: 8 passed; `cargo check --tests --no-default-features`: OK; `cargo fmt -- --check`: clean)
- [x] `CHANGES.md` is updated (if applicable): Unreleased → Fixes entry referencing #584
- [x] Documentation is updated (if applicable): `set_palette` doc comment states the allowed length
