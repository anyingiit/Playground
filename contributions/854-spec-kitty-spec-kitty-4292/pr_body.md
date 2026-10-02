## Issue

closes #4292

## Change

No user- or operator-visible behaviour changes: `mypy --strict src/charter/offering/agent_profiles/repository.py` is now clean (it reported three `no-any-return` errors on `main`), and a gate test keeps it that way.

**Typing (`src/charter/offering/agent_profiles/repository.py`).** Under the `charter.*` `follow_imports = "skip"` override in `pyproject.toml`, cross-module charter imports resolve as `Any` when the file is checked on its own. Three functions returned such values directly:

- `_score_profile() -> float`: `profile.routing_priority` (`AgentProfile` is `Any`)
- `AgentProfileRepository._default_built_in_dir() -> Path`: `built_in_dir(ArtifactKind.AGENT_PROFILE)`
- `AgentProfileRepository.profile_channel_reached() -> frozenset[str]`: `profile_channel_reachable(...)`

As the issue suggests, each value is now bound to an annotated local (`int`, `Path`, `frozenset[str]`, the callee's real declared type) before it is returned. There is no `# type: ignore` and no `cast`, and the runtime is unchanged.

**Gate (`tests/doctrine/agent_profiles/test_repository_mypy_strict.py`, new).** Runs `python -m mypy --strict` on the file and asserts it exits 0 with no `no-any-return`. It follows the existing `tests/cross_cutting/test_mypy_strict_mission_step_contracts.py` / `tests/specify_cli/missions/test_read_path_resolver_redundant_cast_gate.py` pattern, including the `integration` + `slow` markers.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. Claude Code prepared both the code change and the test. I reviewed the result and verified it as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it. No hard feelings at all 🙂

## Tests run

```
uv sync --frozen --extra test --extra lint
uv run python -m mypy --strict src/charter/offering/agent_profiles/repository.py  # before: 3 errors (lines 164, 270, 956, no-any-return); after: Success: no issues found in 1 source file
uv run python -m pytest -q tests/doctrine/agent_profiles/test_repository_mypy_strict.py  # without the src change: 1 failed (the 3 no-any-return errors); with it: 1 passed
uv run python -m pytest -q -n2 tests/doctrine/agent_profiles tests/charter/test_profile_channel_delivery.py tests/charter/test_context_profile.py tests/charter/test_doctrine_service_lineage_accessor.py tests/architectural/test_charter_sole_door_agent_profile_repository.py  # 192 passed
uv run python -m pytest -q -n2 tests/architectural/test_fast_tier_marker_completeness.py tests/architectural/test_marker_job_completeness.py tests/architectural/test_module_shard_registry.py tests/architectural/test_interpreter_shard_coverage.py tests/architectural/test_quarantine_marker.py tests/architectural/test_performance_marker_guard.py  # 73 passed
uv run ruff check src/charter/offering/agent_profiles/repository.py tests/doctrine/agent_profiles/test_repository_mypy_strict.py  # All checks passed!
uv run ruff format --check .  # 2953 files already formatted
uv run python -m mypy --strict tests/doctrine/agent_profiles/test_repository_mypy_strict.py  # Success: no issues found in 1 source file
```

Self-review:
- Each annotated local uses the callee's real declared return type (`AgentProfile.routing_priority: int`, `built_in_dir(...) -> Path`, `profile_channel_reachable(...) -> frozenset[str]`). Nothing is widened or silenced.
- The diff contains no `type: ignore`, no `cast`, and no change to the `pyproject.toml` mypy overrides.

## Blast radius

Discovery: `git grep -n "_default_built_in_dir\|profile_channel_reached\|_score_profile" -- src`
Files:
- src/charter/offering/agent_profiles/repository.py (the only file changed; callers in `src/charter/activation/context_renderers/profile_sections.py` see the same signatures and the same runtime values)
- tests/doctrine/agent_profiles/test_repository_mypy_strict.py (new)

## Deferred

- None.
