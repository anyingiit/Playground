## Description

A unit `Chart` with `resolve_scale` / `resolve_axis` / `resolve_legend` works on its own and in a concat, but Vega-Lite does not allow `resolve` on a unit spec inside a layer or facet, so `alt.layer(chart)` / `chart.facet(...)` failed with a confusing `SchemaValidationError` (`LayerChart has no parameter named 'mark'`, `UnitSpecWithFrame has no parameter named 'resolve'`). Following the minimal fix suggested in #3502, `LayerChart` and `FacetChart` now raise a `TypeError` up front, like the existing "Faceted charts cannot be layered" check, telling the user to layer/facet first and then resolve on the compound chart. Concat and repeat are unchanged.

This was prepared with Claude Code (I had some spare quota and am using it on open issues). Please feel free to close it if it doesn't fit.

## Related issue

Closes #3502

## Checklist

- [x] Tests pass locally: new `test_resolve_on_unit_chart_layer_facet_errors` fails without the fix and passes with it; `pytest -n 4 tests/vegalite tests/utils -m "not slow and not datasets_debug and not no_xdist"` → 538 passed; `pytest -n 4 tests/test_examples.py` (same markers) → 552 passed
- [x] `ruff check` / `ruff format --check` clean
- [ ] Docs — n/a (error message only)
