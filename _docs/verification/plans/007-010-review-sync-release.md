# Prepared QA scenarios —007 through010

Status: PREPARATION ONLY; no future implementation has been tested. Use [shared fixtures/evidence rules](README.md) and current groomed tasks at the actual exact-commit handoff.

##007: child submission, parent review and overdue rules

Task: [007](../../tasks/007-review.md). This is the real request integration gate for prior seeded state/recurrence evidence: occurrence transition, exactly one durable approval/star and recurrence reconciliation must be one transaction.

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| V01 / AC001 | Assigned Aster enters own PIN and submits to-do; repeat request; try Birch/outsider/incorrect PIN and locked-parent substitution | Only assigned child's valid PIN moves eligible work to awaiting once; no award; duplicate/unauthorized transition cannot affect another child or establish parent authority |
| V02 / AC002 | Unlocked A/B parent approves awaiting work; return another with empty/whitespace note then valid explanation; resubmit returned item | Approval completes work/one star. Empty explanation rejected atomically; valid explanation shown and to-do restored; child can resubmit. No approval/return using child/locked/outsider authority |
| V03 / AC003 | DueOct27 submit at shared2026-10-28T01Z in LA; view in Tokyo after deadline; separately submit late in Tokyo; return after date deadline | LA submission classified on-time from server receipt instant interpreted in submitting browser zone, preserved across computers while awaiting; late classification remains overdue; return removes awaiting exception and restores local overdue |
| V04 / AC003 | Supply invalid timezone and fabricated client clock timestamp; test midnight just-before/at/after boundary and return/resubmission | Server validates timezone and derives receipt time, never trusts submitted clock. Classification changes only through allowed return/resubmission; no data mutation on invalid context |
| V05 / AC004,005 | Barrier-release two parent approvals from independent board sessions; retry after lost response; concurrent return/approve and delete/approve | Exactly one completion/unique durable award, no extra star. State-compatible winner or explicit conflict; no completed history deletion or stale overwrite |
| V06 / AC004,005 | Approve overdueMon on scheduledWed; compete approval with scheduler; approve on unscheduled day; inspect constraints/rollback | Completion/star/recurrence atomic; today's distinct eligible occurrence once, no missed-date backlog. Failed transaction leaves neither partial award nor orphan work |
| V07 / AC006 | Two-household foreign occurrence/definition/child IDs; missing CSRF, parent expiry and repeated badPIN direct requests; stable keyboard/zoom submit/return/error | Isolation, P05 identity limits and server authority hold across endpoints; no false success/credential echo; explanatory states accessible |

Before execution, map these scenario numbers to the current task's stable AC identifiers; PM may refine ownership without changing product rules. Reuse committed selectors only after inspecting actual tests.

##008: weekly/all-time stars and completion visibility

Task: [008](../../tasks/008-stars.md).

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| W01 / AC001 | Real active work due in earlier week plus approvals before/current week; render and keyboard traverse without expanding anything | All unfinished work including old overdue remains; current-week completions directly visible; earlier completions hidden but stored |
| W02 / AC002 | Submit/return/resubmit then approve; repeat/retry/concurrent approvals across sessions | Submission/returns0 stars; single successful approval1 star. Exactly one award/completion under retries/concurrency; totals derived from durable approvals |
| W03 / AC003 | Sunday due item approved at household Monday00:00; approvals just before/at next Monday; browser remains open across boundary without mutation | Approval time determines week. At exact boundary new week begins; prior visible completions leave/current totals reset as appropriate; all-time unchanged |
| W04 / AC003 | HouseholdWarsaw DST weeksMar23→30 andOct19→26; compare approval instants around local boundary with browser in different zone | Week interval uses household calendar Mondays, including167/169-hour weeks; browser timezone does not alter weekly counts or inclusion |
| W05 / AC004 | Delete recurrence with past approvals; reload/signout/restart and revisit both browsers | Stored completion snapshots/approval records/all-time totals survive; no separate history screen required |
| W06 / AC005 | Foreign household/child totals and fragment IDs; locked mutations; stable keyboard/200% text totals/status | No other household history/totals exposed; authorization and accessible direct completion visibility preserved |

##009: synchronization, conflicts and offline recovery

Task: [009](../../tasks/009-synchronization.md). Use two independent browser sessions; timestamp accepted server mutation and second-board observable result with one monotonic measurement clock. Report each event latency, not just poll interval or average. Both engines are required; include actual distinct-computer evidence if the release environment provides it and record the independence used.

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| S01 / AC001 | A mutates child/profile, chore create/edit/delete, child submission, parent return/approval and stars; observe B with no manual refresh | Each accepted change visible on B≤5s under normal connectivity; correct column/state/totals from one consistent household revision |
| S02 / AC001,004 | Observe unchanged revision polls while B focuses an input, edits unsaved text and has a form open; mutate unrelated state in A | No unnecessary unchanged content replacement; focus/caret/open form/unsaved input preserved across changed refresh; no credential values leaked in fragments |
| S03 / AC001,004 | Keep polling/viewing/child activity across parent60s timeout; cross local midnight and household week rollover without writes | Polls never renew parent authority. Overdue/week display recalculates at time boundary even with unchanged revision; no old authority or stale totals |
| S04 / AC002 | Disconnect B while board open; exercise failed poll and actual attempted mutation; restore browser network but delay fresh authorized snapshot | Last board remains visible, explicit offline/read-only state, actions disabled. Network hint alone does not restore writes; only fresh authorized snapshot enables them |
| S05 / AC002,003 | Drop mutation response after server commits, then reconcile/retry; separately fail before commit; simulate temporary server500/unreachable | No unconfirmed optimistic success or queued offline writes. Reconnect reveals actual committed result without duplicate work/award; failed-before-commit action stays uncommitted with clear error |
| S06 / AC003 | Two clients edit same revision; stale review/delete versus approval; recurrence scheduler overlaps; fail snapshot request mid-update | Valid compatible result or explicit conflict plus refresh, never incompatible lost update, duplicate occurrence or star. Snapshot revision/content consistent |
| S07 / AC002,004 | Expire/revoke confirmed board authorization or sign out while B visible; inspect storage/cache behavior | Confirmed authorization failure/signout clears private board; transient network failure preserves last view. No service worker/private persistent offline cache; offline reload/startup not promised |
| S08 / AC004 | Two actual households and forged revision/fragment IDs; stable keyboard/200% offline/conflict messages and reconnect | Scoped polling/read/mutation boundaries remain; no false success or inaccessible recovery/focus loss |

Do not mark synchronization PASS from a two-second timer in source or a single request response. Preserve event timestamp evidence and actual second-session render observations; measure each required mutation category.

##010: integrated release gate and evidence matrix

Task: [010](../../tasks/010-release-verification.md). QA verifies the exact integrated delivery hash after009 integration, all27 ACs/J01–J05/P01–P07 and documented regression/scheduler/browser commands. Per-task historic evidence alone is insufficient where later integration can invalidate behavior. The orchestrator performs the user's retained final release requirements review only after final QA.

| Release AC / requirements | Integrated executable/manual scenario and required observation |
| --- | --- |
|001 /REQ001| Fresh register/verify/sign-in/recover/old-password denial; exact one-hour and malformed/reused link cases; unverified actual household access denied |
|002 /REQ002| Intended verified second parent joins once; wrong-recipient/expired/reused seven-day link rejected; replacement succeeds; actual local SMTP capture |
|003 /REQ003| Both parents manage after their own unlock; actual two-household UI/direct endpoint/fragment isolation, no owner-only restrictions |
|004 /REQ004| Add/reset child and own parentPIN via own password; leading zeros preserved; replaced/wrong PIN denies |
|005 /REQ005| Parent B unlocks board opened by A; child/incorrect/outsider/locked requests cannot manage |
|006 /REQ006|60s exact server/client expiry, board remains; polling/viewing/child traffic do not extend |
|007 /REQ007| Password/each targeted PIN identity5 failures/5min across sessions/processes/concurrency; correct blocked until expiry, no deadline extension, success clears; supplementary source limits |
|008 /REQ008| Real mixed due/overdue/awaiting/completed work appears under correct child, textual states/empty setup guidance |
|009 /REQ009| Older overdue still active; current-week completion directly visible; rollover hides older history without deletion |
|010 /REQ010| Create one-off/daily/weekday chores; invalid title/date/schedule/foreign child causes no partial work; no child claim/reassignment; exact P03 edit/delete |
|011 /REQ011| Shared dates/identity across LA/Tokyo; browser-local overdue differences; household calendar scheduling and DST boundaries |
|012 /REQ012| Daily unfinished/awaiting across many days stays one; later approval never generates backlog |
|013 /REQ013| LateMon approval scheduledWed createsWed once; unscheduled day waits; fixed schedule and completed-today identity retained |
|014 /REQ014| Recurrence title/child/schedule edits leave current/completed snapshots; future work uses edits |
|015 /REQ015| Recurrence deletion removes unfinished/stops scheduler generation while retaining actual approvals/history/stars |
|016 /REQ016| Assigned child's valid PIN only; duplicate/foreign/wrongPIN submissions denied; no unauthorized transition |
|017 /REQ017| Approval/required-note return/resubmit real browser journey, no invalid partial change |
|018 /REQ018| On-time/late submission classification shared across zones; awaiting preserves on-time exception, late return overdue again |
|019 /REQ019| Concurrent/retried/lost-response approvals exactly one completion/award; submission/return zero |
|020 /REQ020| Sunday work approvedMonday belongs new household week; DST and no-write rollover preserve all-time/history |
|021 /REQ021| Per-event measured≤5s accepted mutation→other-board render for children/chores/submission/review/totals, no manual refresh |
|022 /REQ022| Preserve open board offline, disabled writes/status; fresh authorized resync before enabling, no offline queue |
|023 /REQ023| Stale edit/review/deletion/scheduler races and lost responses produce valid result/conflict without false success or duplication |
|024 /REQ024| Actual board handles chores/reviews; protected settings accounts/children/PINs; no separate dashboard/reminder additions |
|025 /REQ025| Full household/work/history/stars persist reload/signout/process restart; chore deletion retention verified; excluded deletion controls absent |
|026 /REQ026| StableChrome/Firefox actual versions1280×720/native200%, keyboard-only allJ01–J05, visible focus/labels/text status/error/recovery, fresh screenshot review |
|027 /REQ027| Hash/pepper separation, access links private/sanitized logs/referrers/no-store, credential non-echo, CSRF/session/cookie controls and all unauthorized direct requests |

### Integrated journey order

1. J01: synthetic parent registers/verifies, creates timezone household, sets parentPIN/adds two children, invites second parent; second recipient registers/verifies/joins and opens independent computer board. Check empty-state guidance and invalid recipient/link cases.
2. J02: each parent unlocks own identity, create one-off/daily/weekday assignments; invalid input/stale edit/locked direct requests; future-only recurring edit and P03 one-off restrictions.
3. J03: child's valid/wrong/other-childPIN submission; parent return with required explanation and child resubmit; competing approvals exactly one star; timeout/CSRF failures.
4. J04: no-browser scheduler restart/gap catch-up; unfinished recurring persistence; late completion fixed schedule; weekly/overall progress and boundary rollover.
5. J05: childPIN reset/own parentPIN recovery, password recovery, offline board read-only, lost response/reconnect-before-enable, five-second other-board updates and private signout clearing.

Run full PostgreSQL suites and both bundled engines sequentially on the exact delivery state; separately execute stable browsers/keyboard/zoom and startup/shutdown/independent scheduler procedures. Record command exit codes/counts, services and ownership, actual timestamps/latencies, screenshot observations, final full delivery hash and remaining blockers. Defects return to developer with reproduction and a fresh QA verdict after the changed commit; final review cannot override a FAIL/BLOCKED or omitted criterion. No hosting/deployment/public launch is implied.
