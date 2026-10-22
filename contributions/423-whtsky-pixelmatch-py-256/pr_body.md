<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KMcyNnzD6JeAFXoMMWEfs3D)_

## Description

This ports upstream pixelmatch v8's `ignoreMask` (mapbox/pixelmatch#171) as `ignore_mask`, following the acceptance criteria in the issue. It behaves like upstream:

- **`pixelmatch.core.pixelmatch(..., ignore_mask=...)`:** takes one value per pixel (`width * height` long, e.g. `list[int]` or `bytes`). Pixels with a non-zero value are not compared. They are drawn as unchanged (the grayscale background) in the diff output, and they don't count towards the mismatch or trigger `fail_fast`. A mask of the wrong length raises `ValueError`.
- **Fast path:** if the images only differ inside the mask, the identical-images fast path is taken (returns `0` and draws the grayscale background). This matches the `!ignoreMask || !ignoreMask[i]` check in upstream's identical loop.
- **`pixelmatch.contrib.PIL.pixelmatch(..., ignore_mask=...)`:** accepts either a `PIL.Image` of the same size or a sequence. The image is converted to `"L"`, so any non-black pixel is ignored, and mode `"1"`, `"L"` and RGB masks all work. A size mismatch raises `ValueError`.
- **Anti-aliasing:** detection still looks at neighbouring pixels regardless of the mask, as upstream does.
- **README:** the API section documents the new parameter.

Tests in `test_pixelmatch.py`:

- **Half-mask on the `1a`/`1b` fixtures:** the top half is masked, as in upstream's test. The mismatch equals the number of diff pixels in the unmasked half of the unmasked run. Masked pixels are drawn exactly like an unchanged image, and unmasked pixels are drawn exactly as without a mask.
- **Fast path:** differences only inside the mask give 0 for both the normal and the `fail_fast` call, and the output equals the identical-image output.
- **Size validation:** for core, and for PIL with both a list and an image mask.
- **PIL equivalence:** list, mode `"1"` and mode `"L"` masks give the same count and output as core.

I didn't touch the Changelog section of the README since entries there link the PR number; happy to add one if you'd like.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #256

## Checklist

- [x] Tests pass locally:
  - `pytest --mypy --cov=pixelmatch --cov-report term-missing --benchmark-disable` gives 51 passed and mypy is clean. The only uncovered lines are the existing image-size checks in `core.py`.
  - `black --check .` is clean.
  - Without the change, the 4 new tests fail.
- [ ] `CHANGELOG` (README section): not updated, see above
- [x] Documentation updated (README API section)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
