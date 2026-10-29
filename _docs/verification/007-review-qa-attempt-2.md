# Independent QA: task 007 Firefox recheck, attempt 2

Overall verdict: **BLOCKED**. Date: 2026-10-29. Reviewer: same independent QA agent; no application or test-helper edits.

Implementation remains `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8` on `task/007-review`. Attempt checkpoint: `7c065f4dd0113be50c164c4daa85d69b5ef37da1`. Developer investigation tip reviewed: `3e7d141739dde7235d580b31c40c34bb1fc0a1a6`. The implementation revision is unchanged; intervening tracked changes are documentation only. Environment: macOS, Python 3.13.15, PostgreSQL 17 on loopback 55432, Firefox 159.0 through project geckodriver on loopback 4445. Synthetic test fixture only.

| Criterion | Evidence | Result |
|---|---|---|
| AC-001–005 | Retained from independent QA1 at the same unchanged implementation: 97 affected PostgreSQL tests passed, including child PIN restrictions, required-note return/resubmission, timezone timeliness, atomic one-star/recurrence, stale/race behavior, privacy and persistence. The unchanged Chrome and LA/Tokyo checks from QA1 also remain applicable. QA1 FAIL record remains preserved. | PASS, retained |
| AC-006 | Firefox 159 native 100%/200% sign-in/review coverage was independently reattempted twice but neither run reached the form workflow. Both received HTTP `GET /` 200 and `GET /accounts/login/` 200, then timed out waiting for the `Sign in` heading before filling or submitting. No login POST was issued. This recheck does not establish that the product fails or passes the required Firefox flow. | BLOCKED |

## Checks

- `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest .local/verification/007/test_firefox_probe.py -k native_submission -q -s`: **1 failed, 1 deselected in 17.76s**. Sanitized server output showed only `GET / 200`, `GET /accounts/login/ 200`; timeout occurred at the initial heading wait before the probe's field/focus/error diagnostics. Teardown warned that one session still accessed the disposable test database.
- `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest .local/verification/007/test_firefox_repeat.py -k native_submission -q -s`: **1 failed, 1 deselected in 21.87s**, with one teardown warning. This run used the unchanged `native.signin` helper. The captured log `.local/verification/007/f001-qa2-repeat.log` records `GET / 200` and `GET /accounts/login/ 200`, followed by the same `Sign in` heading timeout. It contains no POST, form values, credentials, cookies, or private data.
- Developer F001 investigation evidence was inspected but not accepted as independent clearance: its Firefox100 and100/200 journeys passed with sanitized POST302→redirect→board200 traces; the earlier QA1 result remained unresolved.

## Finding F001 remains unresolved

This QA2 recheck differs from QA1's failure, which occurred after a sign-in attempt and returned to the sign-in page. Both QA2 runs timed out before form interaction even though the login page endpoint returned200. The final browser URL, page title, heading text, body length/content, and response body were not captured before stopping; do not infer their values. No further browser attempts were made. The required Firefox journey is still unverified. Route a narrow high-reasoning investigation to resolve the discrepancy before the final QA attempt.

## Handoff

Attempt `0072/3` is BLOCKED; retain QA1 attempt1 FAIL and batch2 `6/10`. Do not mark task Done or integrate. After an identified cause/correction, fresh QA attempt3/3 is required. The project-owned geckodriver was stopped; no pytest/browser process remained. The disposable `test_done_together` database had zero active sessions after the runs and was left untouched. PostgreSQL17 remains on55432; unrelated PostgreSQL13 on5432 is preserved. User `_docs/resume.md` remains untouched and excluded.
