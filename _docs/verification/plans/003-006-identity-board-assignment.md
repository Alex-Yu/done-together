# Prepared QA scenarios —003 through006

Status: PREPARATION ONLY; execute on each supplied implementation commit after PM readiness. Shared fixtures, clocks, isolation and evidence rules are in [README](README.md). No check below has run against future implementation.

##003: child/PIN management and parent authority

Task: [003](../../tasks/003-pins.md). Scope ownership agreed with PM: protect existing002 household management/settings with parent unlock; household creation/join remain verified-account bootstrap. Actual chore submission belongs to007.

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| P01 / AC001 | Unlock settings; add child using leading-zero PIN; reload/sign out/in; reset child's PIN; try old/new PIN through available credential verification boundary | Child/profile persists; leading zero retained as part of string; replaced credential fails, new one succeeds; no plaintext read-back |
| P02 / AC001 | Establish/reset selected parent's own PIN using their own password. Repeat with wrong password, other parent's password and forged selected identity | Only selected parent's own account password authorizes initial/reset operation; invalid attempts leave credential state unchanged. No owner-only privilege |
| P03 / AC001,006 | Submit missing/invalid PIN length/nondecimal characters and invalid child data; use foreign-household child IDs in reset/edit requests | Recoverable validation; no partial profile/credential changes or cross-household disclosure. Do not invent name uniqueness or extra product limits |
| P04 / AC002 | A opens board; select B and enter B's PIN. Try A/B valid PINs, child PIN, wrong PIN, outsider identity, locked direct management POST and missing CSRF | Either member parent may unlock; child/wrong/outsider/locked requests deny parent management; no global unlock shared across independent board sessions |
| P05 / AC003 | Unlock at t0; request management at t0+59s, exactly60s,61s in independent seeded sessions | Authority expires at60s; controls require PIN while board stays visible; direct requests enforce same boundary |
| P06 / AC003 | Between unlock and60s, view/poll board and perform child-only activity. Separately perform accepted explicit parent action at t0+30s; test expiry at t0+89/90s | Passive viewing/polls/child activity never extend authority. Accepted parent activity extends its own selected session's deadline; failed/unauthorized actions do not fabricate activity |
| P07 / AC004 | Four wrong PIN attempts then fifth across sessions/processes; correct PIN while restricted; retry at299/300s; send restricted wrong attempts; concurrent five failures | Shared targeted identity restricted five minutes; no lost failures/deadline extension; exact expiry permits retry; permitted success resets consecutive count. Other identities stay separate |
| P08 / AC005,006 | Inspect hash/pepper separation; response/log non-echo assertions; keyboard/zoom settings/unlock/reset/error journey; restart/reload | PINs/passwords protected and no private values logged; scoped permissions persist; visible labels/focus/status and recoverable errors in both stable browsers |

Evidence must distinguish executable PIN credential checks now from actual child-submission authorization integrated in007. Test settings routes plus every preexisting invitation/household management route so002 verified-only authority does not remain a bypass after003.

##004: shared board and settings navigation

Task: [004](../../tasks/004-board.md). Use synthetic seeded read-model states until actual chore models arrive005; review007 and approval-based totals/rollover008 must later replace seed-only evidence.

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| B01 / AC001 | Render A with zero children, then two children and seeded to-do/due/overdue/awaiting/completed states assigned to each | Empty guidance leads to appropriate protected setup; exactly one column per child; assignments under correct child and textual state/overdue equivalents without color reliance |
| B02 / AC002 | Seed active work including an old overdue item and current-week completed item; keyboard traverse board at100/200% | Active and completed entries directly accessible without expanding a collapsed completion section; old active work is not hidden. Real approval/week filtering rerun008 |
| B03 / AC003 | Follow board→settings→board; review protected controls locked/unlocked; inspect available navigation/screens | Shared board handles chore/review interactions; settings hold accounts/children/PINs; no alternate dashboard/reminder behavior introduced |
| B04 / AC004 | Keyboard-only traverse all current board/settings controls in stable engines; inspect heading/column/state semantics and fresh zoom screenshots | Visible focus, labeled controls and text state/status, readable1280×720/200%, no inaccessible clipped controls |
| B05 / AC005 | Anonymous/unverified/householdB direct board/fragment/settings requests, forged household IDs; parent timeout with open board | No A data/credential leakage; verified membership read boundary and locked parent mutation boundary enforced; board remains visible on parent lock |

##005: one-off dated chores

Task: [005](../../tasks/005-one-off-chores.md). Apply exact P03: edit/delete only to-do; awaiting work must be returned first; completed work cannot be edited/deleted. Recurring deletion has a separate006 exception.

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| O01 / AC001 | Unlocked parent creates title/assigned Aster/dueOct27; inspect stored definition/occurrence and board; edit title/child/date while to-do | One valid assigned occurrence with stable identity; approved one-off edits reflected consistently, no duplicate occurrence |
| O02 / AC001,004 | Missing/blank title, missing/foreign child, invalid/missing calendar date, locked/child/outsider request, absent CSRF | Clear validation/denial; no partial definition/occurrence or unrelated state changes |
| O03 / AC001,003 | Seed to-do/awaiting/completed until007 exists; attempt each edit/delete; submit stale version from a second session | To-do edits/deletion allowed; awaiting/completed denied; stale incompatible update explicit conflict and refreshed state, no lost edit. Later007 actual return→edit/delete rerun |
| O04 / AC002 | Two browser timezone contexts at shared instant2026-10-28T01Z render dueOct27 | Same occurrence ID/date; LA not overdue, Tokyo overdue. No household timezone/date rewriting or invented due times |
| O05 / AC003 | Persist through reload/signout/restart; seed earned completion/star snapshots and attempt deletion; inspect actual models | Stored work remains; completed edit/delete denied, history/award retained. Real approvals/delete preservation rerun007/008 |
| O06 / AC004 | Actual two-household forged IDs across create/edit/delete/read; stable keyboard/200% creation/validation/edit | Isolation and protected controls on server; failed actions never displayed as committed; visible accessible recovery |

##006: recurrence and independent scheduler

Task: [006](../../tasks/006-recurrence.md). Synthetic atomic completion invokes the same domain recurrence boundary now; actual approval+star request transaction integration is007, visible totals008.

| Scenario / AC | Independent procedure | Observable expectation |
| --- | --- | --- |
| R01 / AC001 | Create daily and Mon/Wed definitions on scheduled/unscheduled dates; run reconcile twice; leave browsers closed and run documented once/loop command | First due date on/after creation; next scheduled date waits until due. Browser-independent reconciliation idempotent, no pre-creation or duplicate work |
| R02 / AC001,003 | CreationMon; no unfinished occurrence after gap throughFri; reconcile with no browsers; separately keepMon to-do or awaiting across gap | Gap recovery creates latest eligible scheduled date only; unfinished or awaiting work stays exactly one, no backlog |
| R03 / AC002 | Same schedule/occurrence from LA/Tokyo contexts and household-local midnight/DST boundaries | Household timezone controls identity/due calendar date; browser-local overdue label may differ; daily recurrence follows calendar days, not elapsed24h |
| R04 / AC003,004 | CompleteMon on scheduledWed through atomic completion hook; repeat hook/reconcile; complete on unscheduledTue | Mon retained completed; Wed created once when distinct/eligible. Unscheduled completion waits next scheduled day. Today's already completed work is never recreated |
| R05 / AC005 | While current occurrence exists, edit title/child/schedule; retain prior completions; complete current and reconcile future | Current snapshot and history unchanged; subsequent snapshots use new definition, fixed schedule remains fixed |
| R06 / AC006,007 | Delete recurrence in to-do/awaiting states with earlier completion/award; run scheduler/reload/restart | Unfinished work removed and future creation stopped; completed snapshots/earned stars retained; no cascading history loss |
| R07 / AC003,004,008 | Barrier-release two schedulers, scheduler+completion, scheduler+deletion and edit+completion using independent PostgreSQL connections | Unique definition/date and at-most-one unfinished invariants; definition-first lock order, bounded completion/no deadlock, valid winner or explicit conflict; no duplicate work/awards |
| R08 / AC001,008 | Run --once and loop --interval60 without browser, restart loop after controlled downtime and stop owned process cleanly | Catch-up remains idempotent; no need for browser events; transient failures do not falsely report generation; exact startup/shutdown/retry observations recorded |
| R09 / AC007,008 | Two-household ID forgery, stale edits, locked mutation, malformed weekday schedule; stable keyboard/200% creation/edit/error | No cross-household/child authority bypass, partial writes or false success; accessible consistent state |

At006 completion record service-boundary evidence explicitly; do not mark actual approval requests, stars, visible weekly totals or synchronization verified before their owning tasks.
