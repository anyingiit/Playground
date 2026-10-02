## Description

Adds a `--json` flag to `sentrysearch stats` that prints the index stats as one JSON object, so scripts no longer have to parse the human-readable output:

```console
$ sentrysearch stats --json
{
  "backend": "local",
  "model": "qwen2b",
  "total_chunks": 10,
  "unique_source_files": 2,
  "source_files": [
    "/footage/a.mp4",
    "/footage/b.mp4"
  ],
  "missing_files": [
    "/footage/b.mp4"
  ]
}
$ sentrysearch stats --json | jq .total_chunks
10
```

- Keys follow the issue: `backend` (from `store.get_backend()`), `model` (`null` when none is set), `total_chunks`, `unique_source_files`, `source_files`, and `missing_files` (the source files that `os.path.exists` no longer finds, which the text output marks as `[missing]`).
- An empty index still prints a valid object with `total_chunks: 0` and empty lists instead of the "Index is empty" message, so `jq` pipelines don't break.
- Without `--json` the output is byte-for-byte the same as before.
- Uses only the stdlib `json` module, so there are no new dependencies. The output is pretty-printed with `indent=2`.
- I added a line to the "Managing the index" examples in `README.md` and `README.zh.md`, since CONTRIBUTING asks for README updates when a user-visible flag is added.

There is no cost or performance impact. The flag reads the same `get_stats()` data as the text output and makes no API calls.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #62

## Checklist

- [x] Tests pass locally (Python 3.12, `uv sync --group test`)
  - New tests in `tests/test_cli.py::TestStatsCommand`:
    - `test_stats_json_with_data` checks the full object, including `missing_files`, using a real temporary file that exists and one that doesn't.
    - `test_stats_json_empty` covers an empty index (no index detected, so the backend falls back to `gemini` and `model` is `null`).
    - `test_stats_without_json_is_human_readable` pins the exact plain output.
  - Without the change, both JSON tests fail with `No such option: --json`. With it, `uv run pytest tests/test_cli.py -k stats` passes (5 passed).
  - `uv run pytest --cov --cov-report=term-missing`: 441 passed.
  - I also ran it by hand: against a fresh, empty index (`HOME=$(mktemp -d) sentrysearch stats --json`) it prints a valid object with zero counts. Against a small real index (two chunks added through `SentryStore.add_chunks`, one with a deleted source file), `stats --json | jq .total_chunks` printed `2` and `missing_files` listed only the deleted file.
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the repo has no changelog.
- [x] Documentation is updated (if applicable): `README.md` and `README.zh.md`.
