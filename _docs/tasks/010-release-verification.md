# 010: Integrated release verification and browser/accessibility checks

Status: Done
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/10
Local task: `_docs/tasks/010-release-verification.md`
Requirement links: [REQ-001](../plan.md), [REQ-002](../plan.md), [REQ-003](../plan.md), [REQ-004](../plan.md), [REQ-005](../plan.md), [REQ-006](../plan.md), [REQ-007](../plan.md), [REQ-008](../plan.md), [REQ-009](../plan.md), [REQ-010](../plan.md), [REQ-011](../plan.md), [REQ-012](../plan.md), [REQ-013](../plan.md), [REQ-014](../plan.md), [REQ-015](../plan.md), [REQ-016](../plan.md), [REQ-017](../plan.md), [REQ-018](../plan.md), [REQ-019](../plan.md), [REQ-020](../plan.md), [REQ-021](../plan.md), [REQ-022](../plan.md), [REQ-023](../plan.md), [REQ-024](../plan.md), [REQ-025](../plan.md), [REQ-026](../plan.md), [REQ-027](../plan.md)
Dependencies: [009](009-synchronization.md) Done and integrated into `develop`; PM readiness review after that dependency.

## Goal

Verify all agreed release requirements on the integrated delivery revision.

## Acceptance criteria

- [x] AC-001: REQ-001: Verified parents can sign in; unverified accounts cannot access household data; password recovery invalidates the old password; invalid/expired links deny access.
- [x] AC-002: REQ-002: Intended verified recipient joins once; wrong-address, reused, and expired invitations fail; an expired invitation can be replaced.
- [x] AC-003: REQ-003: Either member parent can manage the household; outsiders cannot read or change it through UI or direct requests.
- [x] AC-004: REQ-004: Protected settings add children/reset child PINs; own password authorizes own parent PIN reset; replaced PINs fail. Four-digit PINs preserve leading zeroes.
- [x] AC-005: REQ-005: Either valid parent PIN unlocks management; child/incorrect PINs and locked requests cannot perform parent actions.
- [x] AC-006: REQ-006: After 60 seconds, management requires a PIN again. Board viewing and child activity do not extend parent access.
- [x] AC-007: REQ-007: Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits.
- [x] AC-008: REQ-008: Mixed-state assignments appear under the correct child; states are understandable without color alone; empty states guide setup.
- [x] AC-009: REQ-009: Older overdue work remains visible; current-week completions are directly accessible; older completions leave the column but remain stored.
- [x] AC-010: REQ-010: Parent can create each type; missing/invalid title, child, or date/schedule cannot create partial work. Children cannot claim or reassign work.
- [x] AC-011: REQ-011: Different-timezone computers agree on occurrence identity and dates but may show different overdue labels at the same instant.
- [x] AC-012: REQ-012: Leaving daily work unfinished over several days, including awaiting approval, produces one outstanding item and no backlog after approval.
- [x] AC-013: REQ-013: Approving overdue Monday work on scheduled Wednesday completes Monday and creates Wednesday once; an unscheduled approval day waits for the next scheduled day.
- [x] AC-014: REQ-014: Editing title, assignment, or schedule leaves current occurrence details and completed history unchanged; subsequent occurrences use the edit.
- [x] AC-015: REQ-015: Deleting a definition removes to-do/awaiting-approval work and stops recurrence; prior approvals/history/star totals persist.
- [x] AC-016: REQ-016: Correct PIN moves eligible work to awaiting approval; incorrect/another child's PIN or duplicate requests cannot create unauthorized transitions.
- [x] AC-017: REQ-017: Approval completes work; empty return note is rejected; valid return shows the note and restores to-do; child can retry.
- [x] AC-018: REQ-018: Submission before deadline remains non-overdue after it while awaiting approval; return after deadline restores overdue. Apply P-04 timeliness classification.
- [x] AC-019: REQ-019: Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none.
- [x] AC-020: REQ-020: Monday approval counts in the new week even for Sunday work; weekly rollover preserves history and all-time totals.
- [x] AC-021: REQ-021: Two independent browser sessions/profiles on this Mac cover child/profile, chore create/edit/delete, submissions, returns/approvals, and resulting totals without manual refresh; each server-accepted mutation becomes visible within five seconds (P-06). User accepted this same-host setup on 2026-10-29 for the two-computer synchronization evidence gate. Evidence must identify both sessions as one-host and must not claim testing across two physical computers.
- [x] AC-022: REQ-022: Disconnect preserves visible board and disables actions; reconnect refreshes data automatically before actions resume.
- [x] AC-023: REQ-023: Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed.
- [x] AC-024: REQ-024: Chores/reviews are managed on the board; accounts/children/PINs in settings; no separate dashboard, sounds, or reminder notifications are required.
- [x] AC-025: REQ-025: Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded.
- [x] AC-026: REQ-026: Core journeys work with keyboard and visible focus, labeled inputs, and text status equivalents; agreed browser/viewport/zoom checks pass.
- [x] AC-027: REQ-027: Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. Readiness was recorded after dependency/grooming integration using valid PM review; all final completion gates have now passed. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

QA verifies the exact integrated delivery revision against every AC-001–027, not only prior task verdicts. Record a requirement→journey→test/manual evidence matrix, actual commands/results, stable browser versions and unverified limitations. Use synthetic households and separate test PostgreSQL/in-memory mail; local Mailpit account/invitation capture is explicit and no external provider/deployment is authorized.

- AC-001–007/027, J-01/J-05: Fresh registration/verification/recovery/invitation through captured email; one-hour/seven-day expiry/single use/wrong recipient, one-household/two-parent concurrent limits, actual household isolation, selected-parent password reset, either-parent unlock, five-failure/five-minute identity limits across contexts, 60-second parent-only inactivity and CSRF/private-log checks.
- AC-008–018/024, J-02/J-03/J-04: Keyboard board/settings setup and each real one-off/daily/weekday workflow; exact P-03 edit/delete restrictions, returned notes/resubmission, browser-local timeliness across zones, late/unscheduled recurrence, no-browser scheduler recovery/overlap, future-only edits/deletion retaining earned records. No synthetic service-only fixture substitutes for final integrated HTTP/browser behavior.
- AC-019/020/025, J-03/J-04: Competing approvals award one durable star; approval-time household Monday boundaries/DST rollover, visible current-week completions/all active work and all-time persistence after reload/sign-out/server/scheduler restart and recurrence deletion.
- AC-021–023/026, J-05: Measure each required mutation class at ≤5 seconds from server acceptance to other-session render without manual refresh, using two independent sessions/profiles on this Mac; record same-host independence honestly with no claim of two-physical-computer testing. Also preserve unsaved focus/forms, failed/lost responses, stale conflicts, offline preserved view with disabled writes and fresh authorized reconnect; installed stable Chrome/Firefox at1280×720 and native200% zoom, keyboard/focus/labels/status equivalents. Bundled Playwright Firefox does not certify installed stable Firefox.
- Execute validated commands.md Django checks, drift, Ruff lint/format, full PostgreSQL server/concurrency suite, both bundled browser suites, static collection and scheduler once/loop checks. Document startup/readiness/clean shutdown and services left running; unavailable required check is BLOCKED.
- Orchestrator requirements review occurs at this release stage only and records outcome/evidence at the same final code revision. Final delivery needs independent integrated QA PASS plus this release review PASS. Defects become scoped tasks/fixes with fresh QA and repeat affected release evidence; do not weaken requirements. This task is release verification, not deployment or a second implementation of features.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Parallel preparation is not readiness: dependency integration, grooming integration onto develop and current PM review remain pending. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM parallel scope review: 2026-10-28; acceptance IDs/behavior retained, concrete per-criterion checks and later integration ownership recorded. Draft until dependency/grooming integration and current readiness review; isolated grooming commit supplied to orchestrator for develop integration.

- Implementation summary: Integrated release verification prepared/executed; fixed lost invitation success after synchronized redirect and pre-membership polling blocking join. Added complete true-keyboard native journeys, HTTP recurrence/history coverage and corrected verification fixture/document/identity timing. No new product feature/dependency.
- Task branch / verified implementation commit: `task/010-release-verification` / `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`; independent QA2 PASS evidence `a1c0752baa0ccdb92554e67ffd8ce587844781f7`.
- Changed files / revision: QA1 correction changes only bundled PIN assertions, shared native focus verification and native review failure cleanup; product/backend/configuration unchanged from3769e5c. Documentation-only handoff follows; user resume.md excluded.
- Final branch tip / delivery commit / integration results: Task branch completion tip and integrated delivery `374c2ad42d1ac4b40bb111fc31bf3ed4cf1b66d2`; fast-forward into develop, identical reviewed code.28 affected integration cases plus migrate/check/drift/Ruff160/diff PASS; [integration](../verification/010-release-integration.md).
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: Scoped QA1 fixes: bundled PIN2 PASS18.46s, native review4 engine/zoom cases PASS31.33s,12 actual native focus/outline/label positive/negative controls PASS, Ruff157/diff PASS. Fresh QA1 domain/server166/security/config/SMTP/idle/restart evidence retained by exact unchanged product diff. QA1 FAIL remains historical; QA2 must recertify all13 native tests plus affected bundled PIN cases.
- Verification record: Independent [QA2 PASS](../verification/010-release-qa-attempt-2.md), historical [QA1 FAIL](../verification/010-release-qa.md), [final requirements PASS](../verification/010-release-requirements.md), [integration PASS](../verification/010-release-integration.md).
- Completion / integration evidence / outcome: Done/integrated locally after independent QA2 and final requirements review PASS, all27 ACs. Exact-code merge equivalence and final28 affected integration cases PASS. Active batch2 now10/10;0102/3, all history retained.
- Orchestrator final release requirements review / evidence / outcome: [Final requirements review](../verification/010-release-requirements.md) PASS all27REQ/ACs, seven defaults and five journeys atdc456af; final merge must preserve reviewed code.
- Remaining risks or blockers: No in-scope blocker. Approved local/same-host/synthetic evidence limits remain documented; production operations outside scope. No push/deployment; issue10 Done/integrated exact body/CLOSED readback verified.

## Resumed readiness —2026-10-29

- User explicitly resumed delivery with010;009 Done/integrated. Authoritative issue10 inspected OPEN/Draft with identical scope. Reused unchanged PM grooming `8feda09b8b827736f832fd8dff6a48ece0e7075d` and approved clarification `d0be1b30912e489cd54f61fc2c1f720b34ff7f76`, both ancestors of develop `4c19eed3d87edbe70fea0beb51096996710ab9aa`. Ready; fresh developer verification preparation next.
-010 QA attempts0/3; active batch2 remains9/10; all historical counters preserved. No push/deployment. Existing user resume.md edit excluded.

## Integrated verification preparation —2026-10-29

- Branch `task/010-release-verification` from Ready `6ea156f15d03a1a4553bcadaffbd14a025fe6cd5`; unchanged PM scope. QA0/3, batch2 9/10; historical counts preserved.
- Baseline full PostgreSQL server/concurrency/scheduler suite:163 PASS145.09s. Baseline bundled engines:6 PASS,2 FAIL,9 native skips. F010-001: synchronization fetch consumed invitation success flash on redirect then issued a second GET. F010-002: invitation join bootstrap incorrectly polled a member-only snapshot, clearing the join UI before membership. Narrow integrated corrections preserve the confirmed fetched redirect document and opt authorized member pages into synchronization explicitly, including locked own-PIN recovery. Both affected bundled household cases now PASS20.73s; full final gates follow.
- Adding true keyboard-only installed-browser J01–J05 verification, including native select/date paths; existing focus-plus-JS-value checks alone do not certify that gate. Product scope and ACs unchanged.
- Issue10 In progress/F010-001/002 exact body/OPEN readback verified by coordinator (`.local/verification/010/issue10-progress-readback.json`); next implementation review/evidence synchronization pending coordinator handoff. No developer external writes. No push/deployment. Existing user resume.md edit preserved/excluded.

## Developer review handoff —2026-10-29

- In review at immutable `3769e5c9dba30388c7aa127af9fb2124f62444d0`. [Developer27AC matrix](../verification/010-release-developer.md) records final outcomes, exact commands, same-host measurements, fresh screenshots and qualified historical verifier failures. Product/configuration unchanged after3cc00aa; later fixes strengthen tests/helpers only.
- QA0100/3 before dispatch; batch2 remains9/10; all historical attempts preserved. Independent final QA next, then orchestrator final requirements review. No routine user approval/push/merge/deployment.
- App/Mailpit/driver exit0; owned listeners closed; disposable DB0 sessions. PG17:55432 and unrelatedPG13:5432 retained. Existing user resume.md content/hash unchanged and excluded. Issue10 current In progress exact readback previously verified; In review/implementation/evidence synchronization pending coordinator normal handoff.

## Independent release QA dispatch —2026-10-29

- Fresh independent gpt-6.1-sol/high QA attempt1/3 at immutable `3769e5c9dba30388c7aa127af9fb2124f62444d0`, records-only developer tip `57c8596935c0149d94d031f926a8a33f48e73ad1`. All27 ACs and full final-release gates required; batch2 remains9/10, all previous counts preserved. No source changes, pushes or deployment during QA.

## QA1 FAIL / same-developer fix routing —2026-10-29

- Independent QA1 FAIL at `3769e5c9dba30388c7aa127af9fb2124f62444d0`, evidence `c895bcefbf4a8c795af3956f80c251d52191345e` / [record](../verification/010-release-qa.md).26AC PASS;026FAIL.166server PASS; bundled7PASS/1FAIL; native12PASS/1FAIL including keyboard4PASS; actual SMTP/idle/restart/security/operational gates PASS;36 same-host events1.1863–1.9300s.
- F010-QA001: bundled PIN locked-caption assertion stale. F010-QA002: Firefox100 native return-note outline assertion failed; cause unproven. Same developer must resolve both without weakening ACs; limited high investigation for focus failure. QA released services/DB ownership cleanly; all owned services stopped/PGs preserved.
- Attempts0101/3; batch2 9/10, earlier counts retained. Reuse fresh unchanged evidence only after revision/config/environment proof. New immutable correction then independent affectedQA2 required; final requirements review remains pending. No merge/push/deployment; original resume edit preserved.

## QA1 corrections / developer handoff —2026-10-29

- In review at immutable `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`; [scoped fix evidence](../verification/010-release-qa1-fixes-developer.md). QA001 now verifies actual locked board/recoverable controls; QA002 was proven disabled-form/readiness navigation into Firefox chrome with retained activeElement. Corrected helper waits authorized readiness and requires actual focus/visible positive-width outline/label; no DOM focus repair, product change or removed focus check. Native review closes ORM contexts on failures.
- BundledPIN2 PASS18.46s, native review4 cases PASS31.33s,12 positive/negative controls PASS, static checks PASS. Independent QA2 must rerun all13 native tests plus bundledPIN2; only unchanged domain/backend/config/SMTP/idle/restart evidence is retained. Original QA1 FAIL and both findings remain visible.
- QA0101/3 until dispatch; batch2 9/10 and historical counters unchanged. All owned ports closed/testDB0sessions; PG17/13 preserved. Original resume.md hash unchanged/excluded. Issue10 QA1 FAIL/In progress exact readback verified; correction In review/hash/evidence sync pending coordinator. No merge/push/deployment.

## Independent QA2 dispatch —2026-10-29

- Same independent finalQA gpt-6.1-sol/high at immutable `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`, records tip `a3a6ba51c3045ebb51d271fd21a3761ecf1e92d0`. Attempts0102/3,batch2 9/10;QA1FAIL preserved. All13native and affected bundledPIN2 rerun; retained fresh unchangedQA1 evidence requires explicit diff/environment proof. Final requirements review still pending. No merge/push/deployment.

## Independent QA2 PASS / final review —2026-10-29

- IndependentQA2 PASS all27 at `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`, evidence tip `a1c0752baa0ccdb92554e67ffd8ce587844781f7`, [record](../verification/010-release-qa-attempt-2.md). FreshPIN2/native13/keyboard4/focuscontrols12 PASS;36 same-host events0.9949–1.9487s; retained independentQA1 server/SMTP/idle/restart/security/schema evidence explicitly revision/environment-bound. F010-QA001/002 cleared;QA1FAIL retained.
- Final orchestrator requirements review underway at identicalcode. Task stays In review,0102/3,batch2 9/10; no merge/push/deployment. Owned verification services stopped/PGs/userresume preserved.

## Completion gate —2026-10-29

- All27 ACs independently verified byQA2 atdc456af; final high requirements review PASS for all requirements/defaults/journeys. QA1FAIL and retry history preserved. Done records permit exact-code-preserving local integration; no additional product/test/helper change.
- QA0102/3; batch2 remains9/10 until integration succeeds, then010 uses its remaining slot. No new batch or retries. Original user resume preserved. No push/deployment.

## Integrated completion —2026-10-29

- Fast-forward delivery `374c2ad42d1ac4b40bb111fc31bf3ed4cf1b66d2` on develop preserves reviewed implementation `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3` exactly (only docs differ). [Final integration](../verification/010-release-integration.md) PASS28 affected cases19.68s plus schema/system/lint/format/diff. IndependentQA2 and final requirements review PASS retained at identical code; all27ACs checked complete.
- Bootstrap/001–010 Done/integrated; batch2 now10/10,0102/3/historical counts unchanged. No new task/batch. Userresume exact, owned services stopped/testDB0,PG17/13 preserved. No pushes/deployment.

## Issue reconciliation —2026-10-29

- Issue10 Done/integrated body and CLOSED state verified after successful integration. All12 mapped delivery issues11/12/1–10 verified CLOSED. Source remains unpushed; local source links may not resolve remotely. No remaining delivery blocker or pending authorized issue update.
