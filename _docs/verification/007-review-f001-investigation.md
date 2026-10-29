#007 F001 developer investigation —2026-10-29

Outcome: NOT REPRODUCED; independent QA recheck required. No application or committed browser-helper change. Original QA1 FAIL remains in [007 QA](007-review-qa.md); do not treat developer repeat passes as independent clearance.

Exact unchanged implementation: `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8` on task/007-review, investigation starts after QA records `ca6970e328c72daf7e87528249c7dc7edf3bddf8`. All intervening tracked changes are task/evidence records. Firefox159.0 through owned loopback geckodriver4445; PostgreSQL17:55432 disposable database; synthetic existing `ready()` fixture/PASS_A. No secrets, submitted values, cookies or email addresses logged.

## Targeted evidence

- First probe: copy the committed `test_review_native.py` into ignored `.local/verification/007/test_firefox_probe.py`, select Firefox100 only, retain complete keyboard/error/submit/return/resubmit/approval flow. Wrap Django BaseHandler response to print only method, request path, status and redirect path. Around sign-in print only field lengths/focus/error count and resulting path/heading. Command: `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest .local/verification/007/test_firefox_probe.py -k native_submission -q -s`: **1 passed/1 deselected in9.68s**, clean teardown.
- Before sign-in: login length18, password length24, focus=password, form errors0. Actual HTTP: `GET /accounts/login/ 200`, `POST /accounts/login/ 302 /`, `GET / 302 /households/1/board/`, `GET /households/1/board/ 200`. Resulting heading Done Together, no form errors. Complete Firefox100 flow passed.
- Fresh repeat: ignored `.local/verification/007/test_firefox_repeat.py`, restrict the same committed journey to Firefox100 and200, retain the **unchanged** `native.signin` helper with no extra pre-click browser queries/waits. Only server-side sanitized response trace added. Same command with repeat filename: **1 passed/1 deselected in17.42s**, both installed Firefox159 native100/200 complete flows PASS, clean teardown. Each sign-in showed actual POST302→GET302→boardGET200. Wrong-PIN and empty-note requests400; corrected submission, return, resubmission and approval302, with exactly one approval per work item.
- Four fresh Firefox screenshots (`firefox-{100,200}-{error,returned}.png`) visually inspected: readable error/explanation text, normal vertical scroll and no horizontal overflow. Keyboard fields/focus/labels/native dimensions verified by the retained journey assertions.

Verbose sanitized evidence/scripts: ignored `.local/verification/007/{f001-probe.log,f001-repeat.log,test_firefox_probe.py,test_firefox_repeat.py}`. Owned driver22654 stopped exit0; all probe suites/browser profiles/live servers finished. ProjectPG17 and unrelatedPG13 preserved.

## Diagnosis and routing

No current evidence establishes the cause of the QA-only login failure. The successful trace rules out a persistent Firefox sign-in denial in these isolated repeats; it does not prove a particular environmental or timing cause for the earlier attempt. Do not invent a product/harness fix or weaken browser coverage. Retain the unchanged independent97-server, Chrome100/200 and browser-timezone PASS evidence. Route the same QA to a narrow Firefox100/200 recheck with sanitized server method/status/redirect capture; if failure recurs, capture that failing request trace before changing code.

Task returns In review, F001 **not yet QA-cleared**.007 QA1/3 FAIL history and batch2 6/10 preserved; coordinator will count the next developer-to-QA dispatch as attempt2/3 even though implementation is unchanged. No merge/push. User resume edit preserved/excluded.
