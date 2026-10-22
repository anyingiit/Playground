Thanks @theofidry, good point. I pushed a temporary commit (marked DO NOT MERGE) that sends the text log to `php://stdout` in `infection.json5` and wraps the `explode()` in `formatDiff()` with a no-op `array_values()`. Its UnwrapArrayValues mutant survives, so the "Mutation Testing (annotations)" job on this PR should print the escaped mutant with a colored diff. That job will go red on purpose because of `--min-msi=100`.

Once you've had a look at the log I'll revert that commit, or feel free to drop it yourself.
