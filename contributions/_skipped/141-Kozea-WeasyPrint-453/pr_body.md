This adds the `print-color-adjust` property (economy | exact, inherited, initial economy), so `print-color-adjust: exact` is no longer reported as an unknown property. WeasyPrint never removes backgrounds or changes colors, so both values give the same output; the docs now say so in a new "CSS Color Adjustment Module Level 1" paragraph. Validation tests added in tests/css/test_validation.py.

Disclosure: I prepared this with an AI assistant (Claude Code) and checked it locally. Feel free to close it if it doesn't fit.

Fix #453.
