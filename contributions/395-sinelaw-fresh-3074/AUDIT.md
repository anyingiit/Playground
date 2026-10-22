# AUDIT — sinelaw/fresh @ 4caedcd

Shallow clone (`--depth 50`) of `main`. Reviewed what runs on `cargo build` / `cargo test -p fresh-editor --test all_tests`:

| Item | Reviewed | Verdict |
|---|---|---|
| `build.rs` (fresh-editor, fresh-editor-core, fresh-quickjs-sys, fresh-update) | run `git rev-parse --short HEAD`, `esbuild --version` (optional precompiling of bundled plugins), `cc -print-multiarch`; write generated tables/grammars into `OUT_DIR`; no network | benign |
| `scripts/*.sh`, `package.json` scripts | release/packaging/schema helpers; not run (only `cargo` was run) | benign, not run |
| Tests | spawn PTYs with the user's shell and small scripts in temp dirs; per-test temp workdirs | benign |

No committed binaries executed. Verdict: no malicious code found.
