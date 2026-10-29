# Verification:006 developer

Overall verdict: PASS (developer checks; independent QA pending)
Task / specification: [006 recurrence](../tasks/006-recurrence.md), [prepared scenarios](plans/003-006-identity-board-assignment.md)
Revision: `47268781b08fedb63330fcaaf27a98a3ee260c77` on `task/006-recurrence`, from readiness `2353402cf6461930c3aaf5483b55ea413e2cba6f`.
Reviewer / independence: task006 developer; independent QA must verify this immutable implementation.
Environment: macOS, managed Python3.13, Django5.2.18, PostgreSQL17 loopback55432, isolated disposable test DB; installed Chrome156.0.8078.48 and Firefox159.0. No external email or real household data.
Date:2026-10-29

## Acceptance evidence

| Criterion | Procedure | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | `test_initial_calendar_and_recovery`, `test_latest_recovery_no_backlog_no_precreation`, validation and real no-browser process test | Daily/weekday creation from local creation date, latest eligible catch-up, independent idempotent scheduler | Daily and selected weekdays; future date waits; gap creates only latest; actual once×2,60-second tick, clean interrupt and restart with browsers closed | PASS |
| AC-002 | `test_household_midnight_dst` four spring/autumn midnight instants; retain005 browser-local evidence | Household calendar controls shared due dates; local browsers may differ in overdue text | Warsaw23/25-hour transitions produce correct dates. Identity/due attributes and `static/js/local-dates.js` unchanged from005 verified implementation `2424cdf4fd056a392977ac4414e51df594be4039`; [005 evidence](005-one-off-developer.md) actual two-browser-zone result retained | PASS |
| AC-003 | Initial/recovery and database invariants tests | One unfinished item, including awaiting, no backlog | To-do/awaiting across multiple scheduled days stay one; conditional uniqueness rejects competing date, date uniqueness rejects completed-date repeat | PASS |
| AC-004 | `test_late_completion_fixed_schedule_and_no_today_duplicate`, scheduler/completion race | Monday completed on Wednesday creates Wednesday once; Tuesday waits; today never duplicates | Both scheduled/unscheduled outcomes observed through transaction-owning completion boundary; retry conflicts; no approval HTTP/star claim | PASS |
| AC-005 | `test_future_snapshots_delete_retains_completed`; native edits; edit/completion race | Current/history snapshots unchanged; future uses edited title/child/schedule | Current and older title/child/date retained; Wednesday future snapshot uses edited assignment/schedule; native daily edit preserves current title | PASS |
| AC-006 | Two deletion-state variants and generation/delete/completion races | Remove unfinished, stop schedule, retain completions | To-do/awaiting removed; completed snapshots survive with null definition; reconciliation cannot regenerate deleted schedules | PASS |
| AC-007 | HTTP sign-out/in/reload, actual scheduler process restart and retained deletion snapshots | Durable definition/work/history | Same persisted definition/work restored across processes; completed captured assignments retained after deletion. Actual awards/totals integrated007–008 | PASS |
| AC-008 | HTTP scope/authority/CSRF/version/failure checks; six PostgreSQL races; native four cases; failure/restart command | Isolated protected writes, explicit failure/conflict, valid races, accessible forms | Two actual households/foreign child denied; locked and missing CSRF denied; stale edit/delete409, DB503 without success; independent connection races bounded/no duplicates; generic failed scheduler then safe retry; keyboard/labeled focus/zoom checks pass | PASS |

## Required checks

Use prefix `UV_CACHE_DIR=.local/uv-cache uv run`; all disposable database suites were strictly sequential.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `pytest tests/integration/test_recurrence.py -q` |28 passed in74.91s | `.local/verification/006/backend.txt`; includes actual60-second no-browser loop and SIGINT exit0 |
| `pytest tests/integration/test_recurrence.py::test_real_scheduler_connection_failure_then_restart tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -q` |38 passed in20.05s | `.local/verification/006/affected.txt`:1 added recurrence check +37 regressions; refused loopback DB port returns generic nonzero, correctly connected fresh process succeeds |
| `pytest tests/integration/test_recurrence.py -k independent_transaction_races -q` |6 passed/23 deselected in4.28s | `.local/verification/006/races.txt`; strengthened generation-vs-edit/delete to have no unfinished work, so generation is eligible.29 unique recurrence checks total |
| `RUN_NATIVE_RECURRENCE=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright ... pytest tests/e2e/test_recurrence_native.py -q -s` |1 test/four engine×zoom cases passed in23.95s | `.local/verification/006/native.txt`; actual100%1280×720/200%640×360; weekday checkbox Space/Tab interaction, focus/labels, server validation, edit/delete; native selects assigned after focus checks |
| Eight native screenshots | Visually inspected | `.local/verification/006/{chrome,firefox}-{100,200}-{error,delete}.png`: readable text, vertical scrolling, no horizontal overflow |
| `python manage.py migrate` |0002 applied OK | `.local/verification/006/migrate.txt` |
| `python manage.py makemigrations --check --dry-run`; `python manage.py check` | No changes; no issues | exit0 |
| `ruff check .`; `ruff format --check .`; `git diff --check` | All pass |130 formatted Python files; exit0 |
| `python manage.py collectstatic --noinput` | exit0 |3 copied/7 unchanged |

No dependency/lock/settings/auth/local-date-JS changes; retain unchanged005 locked-environment and earlier account/SMTP/actual inactivity evidence. Full integrated suites and complete browser journeys remain010. Owned driver/browser/live server/scheduler processes stopped cleanly; projectPG17 remains55432 and unrelatedPG13 remains5432. No push/deployment.

## Findings and limits

Initial affected run:62 passed/2 failed due to verification fixtures (reused fixed username; test atomic connection closed by the scheduler's legitimate connection cleanup). Corrected isolated foreign fixture and transaction-enabled command test; fresh targeted results above pass. No unresolved product finding.

Actual child submission/protected approval/unique star award remains007, approval totals/weekly visibility008, synchronization009. The completion service owns a transaction and is intended to nest within007's award transaction, with consistent household→definition→occurrence locking; no test-only product endpoint or fake review workflow was added. No approval model exists yet, so retained earned-star behavior is a later integration obligation rather than a fabricated006 award assertion.
