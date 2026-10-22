# AUDIT — BSC-ES/autosubmit @ 5919cd9

- This is the same repository and clone audited for 422 (BSC-ES/autosubmit#3240). See `contributions/422-BSC-ES-autosubmit-3240/AUDIT.md`. The base commit is the same, 5919cd9.
- `tools/audit_repo.py` showed no new suspicious findings.
- Only `test/unit/config` and `test/unit/git` were run:
  - Both directories' conftest files and `test/unit/conftest.py` were read. They contain only mocks and tmp_path fixtures, with no network calls.
  - Runs used `USER=root` in the uv venv.
- AI policy: CONTRIBUTING has no AI clause. CLA/DCO: none.
