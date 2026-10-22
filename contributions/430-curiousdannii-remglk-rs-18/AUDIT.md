# AUDIT — curiousdannii/remglk-rs @ 6e52722

- `tools/audit_repo.py` findings:
  - The only auto-executing surface is `remglk_capi/build.rs`. It only uses `cc::Build` to compile the bundled C files in `src/glk/`. I read it in full.
  - The repo has no committed binaries. The `.ulx` and `.gblorb` files are Glulx test game files, run by glulxe in the regtests.
  - Pattern finding: `env-dump` in `tests/regtest.py`. That file is the downloaded plotex regtest.py, which is gitignored and not part of the repo. It passes the environment on to the interpreter it runs, which is normal behaviour.
- The test setup fetches third-party code:
  - glulxe, from erkyrath/glulxe via git clone. This is the same source that `tests/prepare.sh` downloads as a tarball.
  - regtest.py, from erkyrath/plotex.
  - Both come from erkyrath, the author of Glk and Glulx.
- The Inform 6 compiler is DavidKinder/Inform6 at tag v6.44, compiled locally with cc.
- The new test game `echolinetest.ulx` is compiled from the included `.inf` source. That source makes only Glk calls.
- AI policy: none in the README or repo.
- CLA/DCO: none.
