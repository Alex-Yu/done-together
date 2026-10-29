# Verification:009 developer

Overall verdict: PASS (developer verification; independent QA pending)
Task / specification: [009](../tasks/009-synchronization.md), [prepared S01–S08](plans/007-010-review-sync-release.md)
Revision: `497a573349f791833bdcee3683b3b1c23ed11ad0` on `task/009-synchronization`; later commit contains records only.
Reviewer / independence: task developer; independent QA next.
Environment: existing locked Python3.13/Django5.2/PostgreSQL17 loopback55432, macOS; installed Chrome156.0.8078.48/Firefox159.0. Synthetic disposable test data only. PostgreSQL13:5432 preserved.
Date:2026-10-29

## Acceptance evidence

| Criterion | Procedure / expected | Observed evidence | Verdict |
| --- | --- | --- | --- |
| AC-001 | S01–03: independently authenticated native profiles; each accepted mutation visible on other board≤5s; unchanged polls preserve DOM; idle boundaries refresh | `test_native_sync_offline_focus_conflicts`:36 events below, unchanged board element identity, PIN value/focus/selection preserved across changed snapshots. `test_idle_household_week_and_local_midnight`: Chrome/Firefox idle Monday refresh hides old completion/resets weekly total while retaining all-time1 and revision; actual30-second local-date timer updates overdue without mutation/event. Snapshot serialization test excludes a competing committed write until next revision. | PASS |
| AC-002 | S04/05/07: preserve last board, disable writes without queue; fresh authorized resync before enable; no false committed result; clear confirmed lost access | Native four engine/zoom cases inject unreachable transport; online hint during failure leaves writes disabled and board text unchanged; restored authorized snapshot enables. Actual Chrome network-offline and transient500 cases also pass. Actual approval commits before its response is discarded: no success/navigation/retry, one award, disabled uncertain form, explicit result-check instruction; returning to board shows completion. Session deletion clears private board in each observer. No service worker/browser storage/cache introduced; household responses remain no-store. | PASS |
| AC-003 | S02/05/06: preserve open draft/caret and reject incompatible stale writes; no duplicate awards; passive reads never extend parent authority | Native open edit retains draft/selection through remote edit and poll; stale submit returns explicit conflict/current board while retaining draft. Native lost-response/retry guard produces exactly one approval. Fresh109 server tests include review/edit/delete/scheduler races, rollback, repeated/lost-response approvals and stale versions. Child edits now require original household revision. Snapshot/view/child requests preserve last_activity; exact60-second server expiry removes parent actions while board stays visible. | PASS |
| AC-004 | S07/08: scoped reads/mutations, CSRF/parent/child guards, persistence/privacy, keyboard/focus/text failure states, native100/200 | Four new sync checks plus105 affected server cases pass: foreign/anonymous/unverified snapshots deny, hashes absent, no-store, expired parent write denied, persistence/CSRF/limiter/domain races retained fresh. Both installed engines at100/200: labeled PIN reached via Tab, visible outline, text status, draft/focus preservation and no horizontal overflow. Required Firefox200 form conflict/unknown-result case was narrowly repeated with zoom asserted after every navigation; readable conflict and uncertain-status screenshots inspected. | PASS |

## Measured synchronization

Both sessions run on **this one Mac**, using independent profiles/session cookies. Writer is installed Chrome; observer is independent installed Chrome or Firefox. This is user-approved same-host evidence, **not two physical computers**. Native Chrome/Firefox100%=1280×720 CSS pixels;200%=640×360 with actual browser zoom. The request-handler clock is captured after successful POST302/domain transaction completion; actual observer DOM appearance is read on the same Python monotonic clock. No manual refresh. All36 events passed; range0.9051–2.0266s. Detailed timestamps remain ignored `.local/verification/009/latencies.json`.

| Event | Chrome100 | Chrome200 | Firefox100 | Firefox200 |
| --- | --- | --- | --- | --- |
| child-create | 1.3221s | 1.3555s | 0.9886s | 1.2809s |
| child-profile | 1.8817s | 1.8819s | 1.9267s | 2.0266s |
| chore-create | 1.8740s | 1.9260s | 1.7430s | 0.9051s |
| chore-edit | 1.8730s | 1.8397s | 1.8552s | 1.7021s |
| submission | 1.8974s | 1.9407s | 1.9039s | 1.8441s |
| return | 1.8884s | 1.8000s | 1.8647s | 1.8863s |
| resubmission | 1.8453s | 1.8804s | 1.8608s | 1.8976s |
| approval-and-totals | 1.8825s | 1.9579s | 1.8743s | 1.8552s |
| chore-delete | 1.9354s | 1.8592s | 1.8639s | 1.8857s |

## Required checks

Commands below run with `UV_CACHE_DIR=.local/uv-cache uv run`; database suites ran sequentially.

| Command / check | Observed result | Evidence / scope |
| --- | --- | --- |
| `pytest tests/integration/test_sync.py tests/integration/test_pins.py -q` |24 passed13.66s | Initial targeted4 sync/20 PIN cases; included again below, not added to unique count. |
| `pytest tests/integration/test_sync.py tests/integration/test_stars.py tests/integration/test_review.py tests/integration/test_board.py tests/integration/test_pins.py tests/integration/test_chores.py tests/integration/test_recurrence.py -k 'not real_no_browser_once_loop_sixty_restart' -q` |109 passed,1 deselected58.84s; exit0 | Four new sync tests and105 affected regressions. One automatic approval-review timeout occurred before process start; authorized single retry ran successfully. No unavailable run claimed. |
| `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; `RUN_NATIVE_SYNC=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_sync_native.py -q -s` |3 tests passed213.57s; exit0 | Four observer engine/zoom cases; four open-form cases; two idle engine cases. `.local/verification/009/native.log`, latency JSON, screenshots. Initial Firefox form navigation reset zoom; do not count that later form segment as200% evidence. First observer-only200% focus/offline/reconnect coverage remains valid. |
| `SYNC_NATIVE_CASE=firefox-2 RUN_NATIVE_SYNC=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_sync_native.py -k open_form -q -s` |1 passed,2 deselected15.44s; exit0 | Narrow missing Firefox200 conflict/500/lost-response/expiry case; explicit viewport/zoom assertions after each navigation. `.local/verification/009/firefox200.log`; `firefox-200-{conflict,uncertain,reconciled}.png`. No broad replay. |
| `python manage.py check`; `python manage.py makemigrations --check --dry-run`; `python manage.py collectstatic --noinput` | PASS: no issues/no changes; 3 static files copied9 unmodified | No schema/dependency change. |
| `ruff check .`; `ruff format --check .`; `git diff --check` | PASS;149 files formatted | Final implementation/test source. |

## Findings and retained evidence

Resolved during implementation: child writes previously incremented a stale revision without serializing the household; now locks/F increments cover every accepted child change and stale child-name edits reject explicitly. Review form's field named `action` shadows the DOM property; async submission now reads the action attribute. Rendering validation/conflict pages disposes old polling/timers/listeners; parent expiry preserves open drafts and board rather than navigating away.

Initial test timestamp module lookup and multi-statement Firefox execution were harness defects, corrected before passing native evidence. Chrome transient `/null` requests came from Playwright auto-invoking a fault-injection assignment that returned a function; the helper now ends those assignments with a nonfunction value. These do not represent ordinary product requests.

Visual review: readable100% offline status/retained content, Chrome200 reconciled board, Firefox200 offline form and narrowly captured200% conflict/unknown-result/board views. Ordinary vertical scrolling remains available; DOM overflow assertions passed. Blank `chrome-200-offline.png` is a capture artifact and **is not counted as visual evidence**. Earlier Firefox form screenshots that reset zoom likewise are not counted as200% evidence; the narrow repeat closes that gap.

Retain unchanged account/email and independent scheduler elapsed-minute/restart evidence at [007 QA3](007-review-qa-attempt-3.md), [006 developer](006-recurrence-developer.md), and [008 developer](008-stars-developer.md). Their domain scheduling/approval/storage/account code and dependencies are unchanged; affected109 server cases freshly verified persistence, guards and races. No unrelated account-email or real scheduler-minute journey replay. Full integrated verification remains010.

Owned browser/test-server sessions closed and geckodriver stopped exit0. PostgreSQL17 and unrelated13 retained. User `_docs/resume.md` preserved/excluded. No merge/push/deployment.

## Verdict rationale

All four criteria have developer evidence; task is In review. Independent QA must verify the immutable implementation; no completion/integration or physical-second-computer claim.
