# Verification:010 independent affected QA attempt2

Overall verdict: **PASS — all27ACs verified with fresh affected checks and explicitly retained independent QA1 evidence.** Final orchestrator release requirements review remains pending.
Task/specification: [010](../tasks/010-release-verification.md); all27ACs read before fix summary.
Immutable correction: `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`, branch `task/010-release-verification`; developer records `a3a6ba51c3045ebb51d271fd21a3761ecf1e92d0`, QA2 dispatch tip `e3073bdfe08af6c3fc32b06642ae875198f74fe6` (documentation only).
Reviewer/independence: same independent final-release QA, gpt-6.1-sol/high. Historical [QA1 FAIL](010-release-qa.md), evidence commit `c895bcefbf4a8c795af3956f80c251d52191345e`, preserved; developer fix evidence was context, not proof.
Environment/date:2026-10-29; macOS26.7.1 x86_64, Python3.13.15/Django5.2.18/psycopg3.3.6/pytest9.2.0; installed Chrome156.0.8078.48/Firefox159.0; same PostgreSQL17.11PID65494:55432 and unrelated PostgreSQL13PID858:5432. Synthetic data only. Ignored artifacts `.local/verification/010-qa2/` (basenames below).

## Revision and retention proof

`git diff 3769e5c9dba30388c7aa127af9fb2124f62444d0 dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3 -- accounts households chores board config static templates manage.py pyproject.toml uv.lock tests/unit tests/integration tests/conftest.py` is empty. Only3 verification-code paths changed: `tests/e2e/test_pins.py` locked-state assertions, `tests/e2e/test_review_native.py` failure cleanup, `tools/verify_household_browsers.py` native keyboard readiness/actual focus assertions. Later tip changes documentation only. Shared-helper source inspection confirms real Tab input, no DOM focus repair, and stricter atomic focus/outline/label checks.

Retained R1 means exact independent QA1 execution at `3769e5c9dba30388c7aa127af9fb2124f62444d0`, not a prior task/developer verdict:166server PASS152.82s including real60sec no-browser scheduler/races; six non-PIN bundled cases PASS; actual local SMTP/61sec idle/restart/privacy/domain/security/schema/static facts. Both bundled PIN cases are fresh and supersede old PIN verdicts;2fresh+6retained=8 unique bundled cases. Both QA1 failures remain historical and were not counted as passing.

PIN SMTP/idle/restart procedures import the changed shared helper for traversal. Retain only their actual mail delivery, elapsed61sec lock/retained-board/disabled-control observations, selected-identity stored records and restart/privacy facts: product and these assertions are unchanged. Their keyboard/focus claims are recertified by the entire fresh native suite instead of inherited. Account SMTP helper and the six non-PIN bundled tests are unchanged and do not use the revised native helper.

Locked sync succeeds; runtime versions match QA1 (`environment.json`). `.env`, projectPG `postgresql.conf` and `pg_hba.conf` metadata predate the QA1 server run (`retained-local-configuration-metadata.json`); no configuration/service replacement occurred. Actual inspected starting processes were only both PostgreSQL instances. No source/configuration/test/helper changes during QA2. All13 native tests rerun because shared helper changed.

## Acceptance evidence

N2=complete fresh13 native tests, including four fresh true-keyboard K2 J01–J05 journeys; B2=fresh bundledPIN2; C2=fresh12 actual native focus controls. R1 rows reference the exact observations/commands in [QA1's full matrix](010-release-qa.md), qualified above. No requirement is inferred solely from source or a developer verdict.

| AC / requirement | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- |
|001 /REQ001|Verified access/recovery; reject unverified/invalid/expired/reused links/old password|R1 account security/S166, bundled accounts and actual SMTP/restart retained; K2 fresh registration/verification/recovery/revisit4 PASS|PASS|
|002 /REQ002|Intended recipient once; wrong/reused/expired deny; replacement|R1 exact7day/recipient/replacement/concurrent limits and SMTP4 retained; K2 fresh recipient join4 PASS|PASS|
|003 /REQ003|Equal parent management; foreign UI/direct isolation|R1 equal-rights/two-household guards and explicit other-parent identity retained; K2 second-parent management PASS|PASS|
|004 /REQ004|Protected child/own PIN reset, own password, leading zeroes, replaced denial|R1 exact password/PIN/hash/reset/isolation retained; B2 complete child/name/PIN and own-PIN replacement/error journeys PASS both engines; K2 reset/old denial4 PASS|PASS|
|005 /REQ005|Either parent unlocks; wrong/child/locked requests cannot manage|R1 direct role/authority/identity guards retained; B2 locked board/recoverable unlock and K2/N2 parent actions PASS|PASS|
|006 /REQ006|Exact60s relock; passive/child activity cannot extend; board stays|R1 exact59/60/nonextension plus real61sec stable Chrome/Firefox retained; N2 passive snapshot expiry/direct403/retained board PASS|PASS|
|007 /REQ007|Five failures/five minutes across contexts; exact retry/success reset|R1 account/PIN/process/session/concurrent/source-window security evidence retained; actual limits unchanged/enabled in fresh browser cases|PASS|
|008 /REQ008|Correct child/mixed states/text and empty guidance|R1 actual HTTP mixed snapshots retained; N2 actual returned/overdue/completed cards and K2 empty/awaiting/completed states PASS; synthetic layout test supplemental only|PASS|
|009 /REQ009|Old active visible; current completions direct; older history hidden/retained|R1 storage/week boundaries retained; N2 actual stars/completions/reload and idle no-write Monday rollover PASS|PASS|
|010 /REQ010|Create one-off/daily/weekdays; invalid/foreign no partial work; P03/no claiming|R1 invalid/foreign/direct/P03 cases retained; N2 one-off/edit/delete/validation and K2 true-keyboard date/select/schedules4 PASS|PASS|
|011 /REQ011|Shared identity/date; local overdue and household calendar/DST|R1 calendar/DST/receipt boundaries retained; N2 actual LA/Tokyo metadata/awaiting/midnight/return classification plus DST identity/date PASS|PASS|
|012 /REQ012|One unfinished across days including awaiting; no backlog|R1 final3 actual HTTP recurrence/approval/scheduler integration cases retained unchanged|PASS|
|013 /REQ013|LateMonday approvedWednesday createsWednesday once; unscheduled waits|R1 scheduled/unscheduled HTTP cases and scheduler/approval/uniqueness races retained|PASS|
|014 /REQ014|Edits preserve current/completed snapshots; future uses changes|R1 title/assignment/schedule HTTP assertions retained; N2/K2 future-only edit UI PASS|PASS|
|015 /REQ015|Delete unfinished/stops recurrence; retain earned history/stars|R1 actual HTTP deletion/approval/scheduler/fresh-process retention retained; N2 recurrence deletion UI PASS|PASS|
|016 /REQ016|Only assigned child PIN; wrong/other/duplicate denied|R1 identity/assignment/CSRF/race guards retained; N2 review PIN errors and K2 replaced child PIN denial/new submission PASS|PASS|
|017 /REQ017|Approve; reject empty return note; display valid note; resubmit|R1 HTTP transitions retained; N2 review all4 engine/zoom flows PASS including previously failing Firefox100 and previously unreached Firefox200; K2 full return/resubmit/approve4 PASS|PASS|
|018 /REQ018|Preserve on-time awaiting classification; late remains overdue; return restores|R1 receipt/midnight/DST/reclassification retained; N2 awaited LA/Tokyo actual state/zone/timeliness, clock jump and late return PASS|PASS|
|019 /REQ019|One durable completion/star across retry/concurrency; submit/return0|R1 independent HTTP/transaction races/rollback/lost response retained; N2 committed response drop/no retry/reconcile exactly1 award PASS|PASS|
|020 /REQ020|Approval-time household Monday/DST week; all-time/history retained|R1 exact Monday/167/169hour weeks retained; N2 idle unchanged-revision weekly rollover/current completion hide/all-time retention PASS|PASS|
|021 /REQ021|Every required accepted mutation visible in other session within5s|N2 fresh36 events/9 classes/all4 observer engine/zoom contexts,0.9949–1.9487sec; `sync-latencies.json`/`sync-summary.json`; independent profiles on this one Mac, no physical-second-computer claim|PASS|
|022 /REQ022|Offline view retained/disabled writes; fresh authorized reconnect before enable|N2 Chrome actual offline + both engines controlled transport/500; online hint alone blocked, board/draft preserved, authorized reconnect PASS|PASS|
|023 /REQ023|Valid outcome/explicit refreshed conflict; no false success/duplicates|R1 transaction races retained; N2 four-context draft/caret/stale/current board,500,lost committed response/no retry/reconciliation/expiry PASS; actual Firefox200 scope confirmed|PASS|
|024 /REQ024|Board chores/reviews; protected settings child/PIN/accounts; exclusions|N2/K2 board/settings/recovery journeys PASS; R1 unchanged exclusions retained|PASS|
|025 /REQ025|Household/work/history/stars persist reload/signout/restart/deletion|R1 actual fresh-process award/history/deletion and app/account/selected-identity restart records retained; N2 reload and K2 recovered household with1star4 PASS|PASS|
|026 /REQ026|Stable1280×720/native200%, keyboard/visible focus/labels/text; required checks pass|B2 both PIN cases PASS; N2 all13 PASS including K2 four full true-keyboard journeys; C2 accepts4 actual focused/labeled3px-outline controls, rejects4 outline:none and4 unlabeled controls; meaningful fresh screenshots inspected; F001/F002 cleared|PASS|
|027 /REQ027|Protected credentials, private links/logs, non-echo, CSRF/scoped denial|R1 actual privacy/hash/pepper/headers/CSRF/cookie/direct guards and six captured original paths/password absence from ordinary logs retained; N2 confirmed auth loss clears private board; no credential/private-link values output|PASS|

## Required affected checks

Repository root; `UV_CACHE_DIR=.local/uv-cache`, browser commands also `PLAYWRIGHT_BROWSERS_PATH=.local/playwright`. Disposable database/browser suites ran sequentially; original confirmed handles awaited, never restarted on timeout.

| Exact command/check | Result | Artifact |
| --- | --- | --- |
|`uv run pytest tests/e2e/test_pins.py --browser chromium --browser firefox -q`|2PASS23.13s, exit0; actual locked board/unlock/management absence plus complete child/PIN replacement flows|`bundled-pins.log`|
|`RUN_NATIVE_BOARD=1 RUN_NATIVE_CHORES=1 RUN_NATIVE_RECURRENCE=1 RUN_NATIVE_REVIEW=1 RUN_NATIVE_STARS=1 RUN_NATIVE_SYNC=1 RUN_NATIVE_RELEASE=1 uv run pytest tests/e2e/test_board_native.py tests/e2e/test_chores_native.py tests/e2e/test_recurrence_native.py tests/e2e/test_review_native.py tests/e2e/test_stars_native.py tests/e2e/test_sync_native.py tests/e2e/test_release_keyboard_native.py -q -s`|13PASS455.56s, exit0/no skips; nine other native tests plus K2 four fresh keyboard journeys|`native.log`; execution35086 collected|
|`uv run python .local/verification/010-qa2/focus-helper-negative.py`|12/12 actual native controls PASS:4focused/labeled positive solid3px accepted;4focused outline:none rejected;4focused unlabeled rejected; all had true document/element focus and :focus-visible|`focus-helper-negative.py/log/json`; execution65994 collected|
|`uv sync --locked`; `uv run ruff check .`; `uv run ruff format --check .`; `git diff --check`|All exit0; final diff check also PASS|`static.json`, `static-*.log` (exact argv)|
|Required driver `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; stop ownedPID68472 with SIGINT after browser closure|Driver exit0;8000/8025/1025/4445 closed;55432/5432 preserved; disposable testDB0sessions|`geckodriver.log`, `shutdown.json`; driver97224 collected|

C2 used an inspected ignored probe, copied only to redirect its JSON output and add positive-control screenshots. No product/source/helper/test edits, DOM focus repair or fake keyboard events. These synthetic controls validate the verifier; actual product focus is separately asserted during the full N2 review/field journeys.

The full N2 form/conflict test explicitly reapplies native zoom and asserts1280/640×720/360 after navigation, including Firefox200; its four cases PASS. Fresh Firefox200 conflict and uncertain-response PNGs are640×360 (`ff200-screenshot-dimensions.json`), visually inspected. The required actual200 scope is present, so no additional automatic Firefox200 rerun was needed.

## Findings, visual scope and handoff

- **F010-QA001 cleared** at this immutable correction: B2 verifies scoped locked-prefix caption, visible board, enabled visible Unlock and absent management link, then completes all original PIN/reset/replaced-denial behavior in both bundled engines. Original exact-caption failure remains in QA1.
- **F010-QA002 cleared**: fresh N2 completes the original failed Firefox100 note traversal/validation/return/resubmit/approval and Firefox200, with real Tab and atomic `document.hasFocus`, element`:focus`/`:focus-visible`, non-none positive-width outline and label assertions. Independent C2 rejects missing outline/label. No claim that QA reproduced the investigator's historical cause; fresh affected execution and stricter checks establish the corrected verdict. Original failure remains in QA1.

Selected fresh screenshots inspected: real Firefox200 returned-overdue card with parent explanation/submit controls, Firefox200 conflict preserving draft and unknown/no-retry status, Chrome100 keyboard awaiting/completed cards and1star, Firefox200 keyboard household/totals, and actual native positive-focus control outline. QA1's already-inspected unchanged SMTP/idle images retained.56 fresh native screenshots copied by run-time metadata (`fresh-screenshot-manifest.json`); not every generated image is claimed inspected. Synthetic long-name board images supplement layout only. Scrolled/mostly blank Chrome200 returned image is not useful visual proof.

Native200 is640×360 CSS/DPR2 from1280×720, with normal vertical scrolling, not an entire board in one viewport. Firefox200 PNGs are640×360. Same-host independent observer/writer profiles measured all nine mutation classes four times; no physical-second-computer claim. Chrome actual browser offline; Firefox controlled transport/500 failures.

All27ACs PASS, no remaining QA blocker. SameQA2/3; batch2 9/10 and prior attempts unchanged; QA1 FAIL preserved. Only QA evidence records committed; no source/helper/test changes, external issue writes, completion, merge, push or deployment. Owned driver/browser/test sessions closed; both PostgreSQL clusters retained. Original user resumeSHA `987abed09c813aa9f566613ce5a040e905f0d6751b840f08a7ccaa46d8d5627f` unchanged/excluded. Release DB/browser ownership returned to coordinator. Final orchestrator requirements review remains mandatory at this verified code state.
