## Description

Fixes #2232. `FormWriter::writeFormObjects()` gave every SVG (and WMF) form XObject a `/Group` with `/S /Transparency`. As the issue shows with hand-edited PDFs, the macOS print pipeline drops all page content painted after such a form, even for a fully opaque SVG.

The group is only needed when the SVG paints something translucent, so this change writes it only then:

- `Svg` tracks whether the drawing uses transparency: a fill/stroke opacity below 1 (paths, text, and `opacity` / `fill-opacity` / `stroke-opacity` from attributes or styles), a gradient with a stop opacity below 1 (the gradients that get a soft mask), or an embedded raster image with an alpha mask. `ImageSVG()` returns this as `transparency` in the image info.
- `FormWriter` writes `/Group` and the group object only when `transparency` is set. WMF images never set it, so they no longer get a group either (WMF has no transparency).

Translucent SVGs are written exactly as before (a default non-isolated, non-knockout group composites the same as no group, so dropping it for every SVG would also be an option — happy to switch to that if you prefer). For opaque SVGs the only difference in the output is the missing form-level group; the page-level group is untouched. Rendering is unchanged: rasterising the issue's reproduction (and a `fill-opacity="0.5"` variant) with poppler's `pdftoppm` gives byte-identical images before and after the change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code (declared on the third line of the commit message, as CONTRIBUTING asks) and verified as listed below. I could not test printing on macOS myself; the fix follows the issue's own finding that removing the form-level `/Group` makes the page print correctly. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2232

## Checklist

- [x] Tests pass locally — new `tests/Issues/Issue2232Test.php` (6 tests): an opaque SVG has no form `/Group`; SVGs with `fill-opacity`, `stroke-opacity`, `opacity`, text `fill-opacity` and a gradient `stop-opacity` keep the group, which points to a `/S /Transparency` object. Without the fix the opaque test fails; with the transparency tracking disabled the five translucent cases fail. `vendor/bin/phpunit` → 992 tests, the only error is `ImbTest::testInit` ("IMB barcodes require bcmath extension"), which fails the same way on `development` in my environment (no bcmath). `composer cs` (phpcs on the changed files) and PHPStan 2.3 (`phpstan analyse`) are clean. Snapshot tests were not run (no imagick here).
- [x] `CHANGELOG.md` is updated — Bugfixes entry under mPDF 8.3.x.
- [ ] Documentation is updated — n/a, no API or config change.
