# Independent QA: task 007 review

Overall verdict: **FAIL**. Date: 2026-10-29. Reviewer: fresh independent QA; no implementation changes.

Implementation: `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8`, branch `task/007-review`. QA checkpoint before tests: `23cc848698a0bfb5da5405829dee8dcb379bda4b`; implementation code/configuration were unchanged. Environment: macOS, Python 3.13.15, Django 5.2, PostgreSQL 17 on loopback 55432, Chrome 156.0.8078.48, Firefox 159.0. Synthetic isolated fixtures only.

| AC | Independent evidence | Verdict |
|---|---|---|
| AC-001 | Actual submission, wrong/other-child PIN restrictions across eligible and ineligible states, duplicate/stale requests, shared lockout boundaries, assignment-change conflict, and no parent-authority extension covered by the PostgreSQL feature/affected suite. | PASS |
| AC-002 | Submit → required-note validation → return → explanation visibility → resubmit → approval and authorization/error paths covered by the PostgreSQL suite. | PASS |
| AC-003 | Server receipt/browser-zone classification, fabricated client clock rejection, midnight/DST boundaries, awaiting stability, return and resubmission behavior covered by server tests; LA/Tokyo browser-timezone journey passed. | PASS |
| AC-004 | Independent transaction and HTTP approval races, exact one-star/completion, recurrence hook and scheduler overlap, rollback/retry, lost-response retry, no-backlog behavior covered by the PostgreSQL suite. | PASS |
| AC-005 | Stale approval/return/delete/edit/scheduler conflicts, actual return before P-03 edits/deletes, completed retention, recurring deletion and persistence restart covered by the PostgreSQL suite. | PASS |
| AC-006 | Isolation, CSRF, permission separation, private failure handling, persistence and Chrome journeys passed. Required Firefox 159 native journey failed: Firefox stayed on the sign-in form after the sign-in attempt instead of reaching the board. No visible error was rendered; the form was back at `/accounts/login/` with empty credential fields. HTTP response status/body was not captured. | FAIL |

## Checks

- `UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_review.py tests/integration/test_recurrence.py tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -k 'not real_no_browser_once_loop_sixty_restart' -q`: **97 passed, 1 deselected**, 62.44s. PostgreSQL test suites ran sequentially. The exact excluded real 60-second scheduler/restart scenario is unchanged from earlier retained evidence.
- `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_review_native.py -q -s`: twice with project geckodriver running, each **1 failed, 1 passed**. Chrome 156 native 100%/200% submit/return/resubmit/approve passed; LA/Tokyo timezone browser test passed. Firefox 159 started but stayed on its sign-in page after sign-in, so the native journey did not reach chore submission. A run without geckodriver first failed at driver connection and is treated as environment setup, not a product result.
- The exact implementation revision matched the developer handoff; `git diff 8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8..HEAD` contained only task/evidence bookkeeping at review time. No product code changed.

## Finding F001 — Firefox native review journey does not reach board

Starting state: fresh test database/fixture and Firefox 159 launched headless by the documented loopback geckodriver. Reproduction: run the native review command above. Chrome 100% and 200% subjourneys pass; the following Firefox subjourney navigates to the test-server `/accounts/login/`, submits sign-in, then remains on that page instead of showing `Done Together`; the test times out waiting for the board. Sanitized follow-up inspection showed no visible alert/error text and empty login/password fields after the page returned. No credentials or private values were captured. The HTTP status and response body were not recorded, so cause remains undetermined. Developer evidence records all four installed browser/zoom journeys passing; this independent discrepancy must be resolved before task completion.

## Handoff

Attempt `0071/3` is FAIL and remains in review; batch 2 remains `6/10`. Route F001 to the same developer thread for a narrow Firefox sign-in/harness investigation. Do not mark task Done or integrate until the cause is corrected or repeatably shown to be a local harness issue and the required Firefox coverage passes. Fresh QA after a new implementation revision is attempt `2/3`. Project geckodriver was stopped after checks; PostgreSQL 17 remains available on 55432 and unrelated PostgreSQL 13 on 5432 was preserved. User `_docs/resume.md` remains untouched and excluded.
