# AUDIT — lycheeverse/lychee @ c11d779 (shallow clone 2026-10-01)

Tool: `python3 tools/audit_repo.py /home/user/work/lychee` (243 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| lychee-bin/build.rs (cargo build script, `Command::new("git")`) | Read in full: runs `git show --no-patch --format=%cs HEAD` and exports `GIT_DATE` env for the man page | benign |
| fixtures/fragments/zero.bin (2 B), fixtures/dump_inputs/subfolder/example.bin (0 B) | Tiny test fixtures | benign |
| raw-ip-url: valid.rs:294 (127.0.0.0), filter/mod.rs:284-285 (169.254.x link-local) | Unit test constants for IP filtering | benign |
| npm lifecycle hooks | none | n/a |

No network downloads at build/test time beyond crates.io deps (Cargo.lock pinned). Verdict: **safe to build/test**.
