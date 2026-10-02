## Purpose and Motivation

Fixes #7556.

`LinExp_SetCalc` picks the `_aa`, `_ak` or `_ka` calc function as soon as *one* input of the `srclo`/`srchi` or `dstlo`/`dsthi` pair is audio rate. Those functions then advanced *both* inputs of the pair once per sample (`ZXP`). A scalar or control-rate partner only has a single sample, so it was read past the end of its buffer and the output went "off the rails", e.g.

```supercollider
{ LinExp.ar(DC.ar(0.5), -1.0, 1.0, 1.0, DC.ar(2.0)) }.plot  // dstlo scalar, dsthi audio -> _ka
```

This PR keeps the existing calc-function selection and the per-variant hoisting, but only advances inputs whose rate is `calc_FullRate`; the other inputs are read as constants (step 0). The existing arithmetic (`/` and `sc_reciprocal`) is unchanged, so outputs for the previously-correct cases (all-audio pairs, all-scalar/kr) are bit-identical.

A regression test `TestCoreUGens:test_linexp_mixedRateInputs` is added. It renders `LinExp.ar(DC.ar(0.5), srclo, srchi, dstlo, dsthi)` for every combination (3^4 = 81) of scalar / `DC.kr` / `DC.ar` range inputs and compares against `0.5.linexp(-1, 1, 1, 2)` (= 1.6817928).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Types of changes

- Bug fix

## To-do list

- [x] Code is tested
- [x] All tests are passing
- [ ] Updated documentation — n/a (behaviour now matches the documented one)
- [x] This PR is ready for review

### How it was tested

Linux (Ubuntu 24.04, GCC 13), Release build with `-DSC_QT=OFF -DSUPERNOVA=OFF`, scsynth on JACK's dummy driver:

- `TestCoreUGens:test_linexp_mixedRateInputs` without the fix: **56 failures** (every mixed-rate combination; e.g. `[scalar, scalar, scalar, audio]` outputs `nan` / `216232.64` / ... instead of `1.6817928`). With the fix: all 81 combinations pass.
- Full `TestCoreUGens.run` with the fix: 652 passes, 1 failure (`test_demand` - "Duty should free itself after a limited sequence"), which fails the same way on unpatched `develop` in this environment (JACK dummy driver, non-realtime), so it is unrelated.
- Additionally, a standalone C++ harness that drives `LinExp_Ctor` + the selected calc function with fake wires (non-audio inputs are a 1-sample buffer followed by NaN poison) checked all 81 rate combinations against `dstlo * pow(dsthi/dstlo, (in-srclo)/(srchi-srclo))`: 56/81 wrong before, 0/81 after (with and without `NOVA_SIMD`).

## Merge notes

No `CHANGELOG.md` edit since it is compiled at release time. Suggested release note: *"LinExp.ar: fix garbage output when an audio-rate range input is combined with a scalar or control-rate one (#7556)"*.
