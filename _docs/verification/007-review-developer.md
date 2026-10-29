# Verification:007 developer

Overall verdict: PASS (developer checks; independent QA pending)
Task: [007 review](../tasks/007-review.md), six ACs and prepared V01–V07.
Implementation: `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8`, branch `task/007-review` from readiness `257d035bc86cc699088fb6a65d57871235f0c24b`.
Reviewer: implementing developer, not independent QA. Date:2026-10-29.
Environment: documented macOS/Python3.13.15/Django5.2.18/PostgreSQL17 loopback55432; synthetic isolated test databases. Installed Chrome156.0.8078.48/Firefox159.0; native100%=1280×720 and200%=640×360 CSS pixels. No external email, real personal data or new dependencies.

| AC | Executed evidence / expected and observed result | Result |
| --- | --- | --- |
|001|Actual HTTP submission accepts assigned0007, rejects Birch0123; stale/duplicate cannot transition. Wrong PINs on to-do/awaiting/completed persist five failures across sessions; correct PIN remains blocked299s, succeeds/authenticates at300s without extending restriction. Changed assignment after verification conflicts. Child actions neither grant nor touch parent authority.|PASS|
|002|Actual submit→required-note validation→return→visible explanation→resubmit→selected other-parent approval. Blank/whitespace explanations rejected; no award on submit/return. Locked/expired parent requests deny; both parents' selected identities exercised.|PASS|
|003|Server receipt interpreted in validated IANA zone, fabricated clock ignored. LA/Tokyo same instant yields on-time/late; exact local midnight and repeated DST hour checks. Browser clocks advance two days: awaiting flag stays shared; return restores local overdue; resubmission recalculates late.|PASS|
|004|Independent PostgreSQL transactions and two independent HTTP board sessions compete; approval yields one completion and unique durable one-star Approval. Lost committed response is injected after handler commit; exact retry409 refreshes with one award. Recurrence approval covers scheduledWednesday/unscheduledTuesday/same-day/no-backlog; scheduler overlap produces one new eligible item. Award failure rolls back completion/cursor/generated work/revision and permits retry.|PASS|
|005|Approval-versus-return/delete/edit/scheduler and simultaneous submissions; valid compatible results or409. Stale/missing/deleted POST shows current scoped board. P03 edit/delete after real return, completed deletion denial and actual recurring deletion preserve earned Approval/completed snapshot. Future edits leave completed snapshot unchanged.|PASS|
|006|Two actual households, foreign routes, CSRF, wrong/locked/expired roles, no PIN/hash echo; generic503 omits private DB detail in response/log. Sign-out/in and two fresh Python/Django processes restore actual completed/award/deleted-definition state. Installed stable four native engine/zoom flows cover labels/focus/keyboard text entry/submission, PIN recovery, required note/return/resubmit/approval and no horizontal overflow. Eight viewport screenshots inspected; additional Chrome200 paint-settled viewport capture shows the full readable explanation despite a blank compositor region above it.|PASS|

Executed commands from root (`UV_CACHE_DIR=.local/uv-cache uv run` prefix):

- `pytest tests/integration/test_review.py -q`:24 passed initial feature set.
- `pytest tests/integration/test_review.py tests/integration/test_recurrence.py tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -k 'not real_no_browser_once_loop_sixty_restart' -q`:88 passed,2 test-harness failures; corrected below. All65 affected regression cases now pass across these scoped runs plus corrected board rerun.
- `pytest tests/integration/test_review.py tests/integration/test_board.py -q`:33 passed in23.21s, including corrected board fixture/restart guard and added rollback/lost-response/deleted-conflict checks.
- `pytest tests/integration/test_review.py -k 'competing_independent_transactions or assignment_changed or expired_parent or simultaneous_http' -q`:9 passed/23 deselected in7.87s. Final collection32 unique review cases, all executed/pass across scoped runs; no empty selector.
- `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright ... pytest tests/e2e/test_review_native.py -q -s`:browser-local timezone test1 PASS; initial native-select harness failed. Corrected native selector then four installed cases PASS. Final exact native selector `-k native_submission`:1 passed/1 deselected in29.97s, no teardown warning. Native select choices are assigned after keyboard/label/focus checks because OS popup key handling differs; text entry and submits use keyboard.
- `pytest .local/verification/007/test_visual_probe.py -q`:narrow actual HTTP return→stableChrome200 rendered-note/paint-settled screenshot probe PASS. Screenshot/API quirks are separate from product overflow checks.
- `python manage.py migrate`, `check`, `makemigrations --check --dry-run`, `collectstatic --noinput`:exit0; migration0003 applied, no drift/issues,3 changed assets copied/8 unmodified. `ruff check .`, `ruff format --check .` (136 files), `git diff --check`:PASS.

Findings resolved:004 synthetic card incorrectly used positional `persisted=True` for its nonnumeric identity; changed to explicit `overdue=True`. Fresh-process probe initially used test settings whose guard correctly denies app/test database equality; corrected to local settings with isolated testDB override. Native select popup keys replaced with the established focused-option assignment convention. Playwright ORM context initially left one disposable DB session; close now occurs inside its event-loop context, final run teardown clean. Earlier failures remain in ignored logs, not counted as passes.

Logs/screenshots: ignored `.local/verification/007/` (`review-board.log`, `concurrency-final.log`, `native.log`, `native-clean-final.log`, `visual-probe.log`, engine/zoom `-error.png`/`-returned.png`, `chrome-200-returned-viewport.png`). Browser/server profiles close; owned geckodriver stopped exit0. PG17 retained and unrelatedPG13 preserved. No push/deployment. User `_docs/resume.md` untouched/excluded.

Retained evidence: [006 QA](006-recurrence-qa.md) at47268781b08fedb63330fcaaf27a98a3ee260c77 for unchanged scheduler command/recurrence module, including real no-browser60-second loop/restart. This task adds fresh actual award/recurrence HTTP and concurrency checks; no unchanged minute wait/account mail/PIN idle journey repeated.008 owns totals/current-week completion projection;009 synchronization/offline;010 full integrated regression. No claim that these later features pass.

Route:In review for independent QA,007 attempt0/3 before dispatch; active batch2 6/10 and prior histories preserved. No implementation blocker.
