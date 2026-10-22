# Malicious-code audit — mitsuhiko/minijinja @ 5978498 (main), 2026-10-01 (re-verified HEAD unchanged at implementation time)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/w6-minijinja-956` (372 text files), then manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `minijinja-py/build.rs` | one line: `pyo3_build_config::use_pyo3_cfgs()` | benign |
| `minijinja-cli/build.rs` | generates man page / shell completions only when `ASSET_OUT_DIR` is set; no network/exec | benign (not built here) |
| `examples/build-script/build.rs`, `examples/embedding/build.rs` | example crates (template embedding demo); not built here | benign |
| `minijinja-js/package.json` `prepare = npm run build` | wasm-pack build of the JS binding; npm not used here | benign (not run) |
| `.github/workflows/*` pipe-to-shell (wasm-pack, cargo-dist, rustup installers) | CI-only, official vendor URLs; not executed locally | benign |
| `.github/workflows/publish-npm.yml` `rm -f ~/.npmrc` | cleanup of npm token after publish in CI | benign |
| `minijinja-py/Makefile` | creates `.venv`, `pip install maturin pytest markupsafe black pyright`, `maturin develop`, `pytest` | benign |
| `minijinja-py/tests/*.py` | plain pytest tests, no conftest.py, no subprocess/network | benign |
| Committed binaries | none | — |

Verdict: **no malicious code found**; safe to build `minijinja-py` with maturin in an isolated venv under /home/user/work and run its pytest suite.
