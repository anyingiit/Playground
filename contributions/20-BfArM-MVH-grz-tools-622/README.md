# BfArM-MVH/grz-tools#622 — Database configuration masks password with `***`

| Item | Value |
|---|---|
| Issue | https://github.com/BfArM-MVH/grz-tools/issues/622 |
| Tier | 自由 |
| Labels | good first issue, priority: low, type: bug |
| Status | 🚧 in progress — issue chosen, audit next |
| Duplicate-PR check | open PR heads #624–#694 checked: none touch the alembic URL line |

## Notes
- Bug: `SubmissionDb._get_alembic_config` passes `str(self.engine.url)` to Alembic; SQLAlchemy's `str(URL)` masks the password as `***`.
- AI policy: no AI policy in CONTRIBUTING.md / .github (grep for LLM/Copilot/ChatGPT/AI-generated: none).
