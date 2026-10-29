# Independent QA: task 007 final review, attempt 3

Overall verdict: **PASS**. Date: 2026-10-29. Reviewer: same independent QA agent; no application, committed test, or browser-helper changes made by QA.

Verified target revision: `e68c669d145d9edf2c4cd0aec38669c80ce8776a` on `task/007-review`. The task application remains `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8`; only the verification helper in `tools/verify_household_browsers.py` changed at the fix commit. Targeted comparison confirmed there are no changes to application or committed tests between the application and helper-fix revisions. QA checkpoint: `5fc0a905f110f2cf7ecfab2a4e5acba6f7013312`. Environment: macOS, Python 3.13.15, PostgreSQL17 on loopback55432, Chrome156.0.8078.48, Firefox159.0. Synthetic fixtures only.

QA1 FAIL and QA2 BLOCKED are preserved as historical findings. Narrow investigation established that QA2 omitted the required geckodriver `--allow-system-access` flag; Firefox had rendered the heading, but the hidden zoom setup error was swallowed as a navigation timeout. The helper fix now propagates zoom setup errors and restores Firefox's content context on failures.

| AC | Independent evidence | Result |
|---|---|---|
| AC-001 | Retained independent QA1 evidence at unchanged application revision: assigned-child PIN submission, wrong/other-child PIN restrictions, duplicate/stale/assignment-change denial, shared lockout boundaries, and no child extension of parent authority. The affected PostgreSQL run passed97 cases. | PASS |
| AC-002 | Retained QA1 actual submit → blank-note rejection → return with visible explanation → resubmit → parent approval, plus role/lock/error cases. Final Firefox100/200 journeys also exercised this flow. | PASS |
| AC-003 | Retained QA1 server-receipt and validated browser-timezone, fabricated-clock rejection, midnight/DST, awaiting stability, return/reclassification, and LA/Tokyo browser evidence. The application code is unchanged. | PASS |
| AC-004 | Retained QA1 independent transaction/HTTP approval races, exact single durable award, rollback/lost-response behavior, recurrence hook and scheduler overlap, and no-backlog cases. Both final Firefox zoom flows observed one approval after the retryable return/resubmit journey. | PASS |
| AC-005 | Retained QA1 stale approval/return/delete/edit/scheduler conflict, P-03 after actual return, completed/recurring deletion retention, and persistence checks. The application code is unchanged. | PASS |
| AC-006 | Final Firefox159100% and200% native keyboard journeys passed; wrong PIN and blank note errors were recoverable, successful submit/return/resubmit/approve reached the expected board, and each flow produced exactly one approval. The helper regression probe confirmed missing driver privilege returns an explicit setup error promptly and both ordinary and injected failure paths restore content context. Chrome/server/timezone evidence is retained from QA1. | PASS |

## Final targeted checks

- Started owned driver exactly as documented: `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`.
- `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest .local/verification/007/test_firefox_repeat.py -k native_submission -q -s`: **1 passed, 1 deselected in17.09s**. The single test executes complete Firefox159100% and200% flows. Sanitized request trace: login `POST 302` → redirect `GET 302` → board `GET 200`; invalid PIN/note requests were400; valid submission, return, resubmission, approval redirects were302. No secret or form value was logged. Evidence log: ignored `.local/verification/007/f001-qa3-firefox.log`.
- `UV_CACHE_DIR=.local/uv-cache uv run python .local/verification/007/verify_zoom_fix.py`: **PASS**. Without the privilege flag, the synthetic page heading was present; the helper surfaced Firefox HTTP500 `System access is required` in0.01s and restored content context. With the flag, Firefox native100%=1280×720/DPR1 and200%=640×360/DPR2 passed. Injected zoom-evaluation failure propagated and also restored content context. Evidence log: ignored `.local/verification/007/f001-qa3-zoom-fix.log`.
- Four Firefox100/200 error/returned screenshots from the fresh native journey were visually inspected. Error text and return explanation were readable, PIN input was empty after the wrong-PIN failure, normal vertical scrolling remained available, and no horizontal overflow was observed. At200% the screenshot is the expected640×360 CSS-pixel viewport.
- Retained QA1 checks without repetition: affected PostgreSQL suite **97 passed, 1 deselected**; stable Chrome156100/200 journey and LA/Tokyo timezone browser check passed. No unchanged account email, full-browser journey, or real60-second scheduler rerun.

## Handoff

Final QA attempt `0073/3` PASS. QA1 FAIL and QA2 BLOCKED remain linked history; they are not rewritten. QA evidence/status only; no application changes, Done, merge or push. Issue7 remains In review/open with QA3 result synchronized and exact body/open-state readback verified. Geckodriver and browser sessions were stopped; the disposable test database had zero active sessions. PostgreSQL17 remains on55432 and unrelated PostgreSQL13 on5432 was preserved. User `_docs/resume.md` remains untouched and excluded. The task may proceed to its normal administrative completion/integration handoff; final release gates008–010 remain outstanding.
