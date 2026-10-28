# Developer correction:002 F001

Overall verdict:PENDING — fresh affected QA required.
Task/specification:[002](../tasks/002-households.md); prior finding:[QA attempt1 F001](002-households-qa.md).
Revision:Fix implementation hash recorded after commit.
Reviewer/independence:Developer self-check; independent QA pending.
Environment:Existing locked Python3.13.15/Django5.2.18/PostgreSQL17.11, disposable testDB, DEBUGTrue fault fixtures.
Date:2026-10-28

## Correction

`AccountSafetyMiddleware.process_exception` now includes `/households/` in the DatabaseError recovery prefix check, matching its existing household source/privacy handling. The already database-independent unavailable template supplies generic recoverable503 without provider/connection details. No authority, CSRF, referrer/cache policy or domain state rule was relaxed.

## Executed evidence

| Check | Observed |
| --- | --- |
| `uv run pytest tests/integration/test_households.py -k domain_database_failures -q` |4 passed/17 deselected in1.42s |
| `uv run pytest -c pyproject.toml .local/qa_households_extra.py -q --tb=short` |Original independent failing probe now1 passed in0.87s; QA probe unmodified |
| `uv run pytest tests/unit tests/integration -q` |53 passed in10.46s |
| `uv run python manage.py check` |Exit0, no issues |
| `uv run python manage.py makemigrations --check --dry-run` |Exit0, no changes |
| Ruff lint/format and git diff check |Exit0 |

The four committed regressions cover create service after limiter/verified guard, settings rendering, invitation service transaction and join service. DEBUGTrue responses must be generic503 with retry guidance/no-store/same-origin; actual configured request-handler output must have a safe Service Unavailable entry, no private synthetic marker or traceback, and no private join nonce. Household/membership/invitation counts/consumption remain unchanged; retry succeeds after fault removal. Invitation service test raises during send inside its transaction, proving rollback.

Initial test-only capfd capture did not receive the configured logger stream; changed to directly capture the real handler output, then all assertions pass. Product response was already503 after the source fix. No private values were printed.

## Evidence retained

Only the exception route prefix and new tests change implementation. Prior QA AC001–003 plus6 bundled-browser/native100/200/actualSMTP/race/restart positive evidence remains applicable to unchanged normal paths; fresh QA must decide affected AC004/005 at the new commit. No browser source/markup/service/schema/dependencies changed; unchanged browser suites were not rerun.

## State

Task returns In review; attempt1/3 retained until QA2 dispatch, active batch2 completions1/10. No app/mail/driver processes started by this fix; projectPG17 remains55432 and unrelatedPG13 preserved. No merge/push/deployment.
