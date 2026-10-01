# AUDIT — rust-embedded/heapless @ a50891c

`python3 tools/audit_repo.py /home/user/work/heapless` (49 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| build.rs (cargo build script, runs on build/test) | Read full file | Benign: probes target features (atomics / ARM LL/SC) by compiling a tiny `#![no_std]` probe with `$RUSTC` into `OUT_DIR` (code from anyhow's build.rs). No network, no file access outside OUT_DIR. |
| build.rs:63/68 `Command::new(wrapper/rustc)` | Same | Benign: invokes rustc (or RUSTC_WRAPPER) for the probe only. |
| npm hooks / committed binaries | — | None. |

Verdict: no malicious code found; safe to build/test.
