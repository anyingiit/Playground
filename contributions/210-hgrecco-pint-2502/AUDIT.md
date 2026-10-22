# AUDIT — hgrecco/pint @ c603d6d

`python3 tools/audit_repo.py` on a depth-30 clone: 132 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks / committed binaries | none reported | — |
| 24 × `pickle.loads(pickle.dumps(...))` in `pint/testsuite/*` | round-trip pickling tests of Quantity/Unit/errors objects created in-test | benign |
| `.devcontainer/devcontainer.json` postCreateCommand | `pip install -e '.[test]'` + docs reqs + pre-commit; not run here | benign |
| `pint/testsuite/conftest.py` | plain pytest fixtures (registries) | benign |

Verdict: nothing suspicious; safe to install and run tests.
