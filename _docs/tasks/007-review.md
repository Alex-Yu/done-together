# 007: Child submission, parent review, returns, and overdue rules

Status: In progress
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/7
Local task: `_docs/tasks/007-review.md`
Requirement links: [REQ-016](../plan.md), [REQ-017](../plan.md), [REQ-018](../plan.md), [REQ-019](../plan.md), [REQ-023](../plan.md)
Dependencies: [006](006-recurrence.md) Done/integrated `42e1c982001f9ae687a6451a1b3d3ad25648edcc`; independent QA1 PASS and affected integration gates PASS.

## Goal

Children submit assigned work and parents approve or return it without duplicate rewards.

## Acceptance criteria

- [ ] AC-001: REQ-016: Correct PIN moves eligible work to awaiting approval; incorrect/another child's PIN or duplicate requests cannot create unauthorized transitions.
- [ ] AC-002: REQ-017: Approval completes work; empty return note is rejected; valid return shows the note and restores to-do; child can retry.
- [ ] AC-003: REQ-018: Submission before deadline remains non-overdue after it while awaiting approval; return after deadline restores overdue. Apply P-04 timeliness classification.
- [ ] AC-004: REQ-019: Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none.
- [ ] AC-005: REQ-023: Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed.
- [ ] AC-006: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. Ready on2026-10-29: coordinator reused unchanged PM scope review `8feda09b8b827736f832fd8dff6a48ece0e7075d`; dependency006 and grooming integrated, six criteria/contracts/verification plan unchanged. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

Firefox native verification requires the exact driver launch: `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`. The system-access flag enables privileged native100/200 zoom and is mandatory; missing privilege must surface as setup failure, not a false sign-in timeout. Stop only this owned driver after checks. See [commands](../commands.md).

- AC-001: Actual eligible assigned chore submission accepts only that child's valid PIN; wrong/another-child/outsider/duplicate/stale requests cannot authorize transition or management. Reuse003 identity lockout and test submission endpoint five-failure/five-minute behavior across sessions. No star on submission; no parent-unlock extension from child actions.
- AC-002: Either unlocked parent approves pending work or returns it with a nonblank explanation; whitespace-only/missing note rejected atomically. Return restores to-do and visible note; same child can resubmit. Expired/locked/wrong-household direct requests deny. Parent controls remain on board, with keyboard-accessible labeled forms and honest recoverable errors.
- AC-003: Compute submission classification using server receipt instant and validated submitting-browser timezone; reject invalid context without trusting a submitted clock. Test on-time awaiting work remains non-overdue across later local midnights/different viewers, late submission stays visibly overdue, late return restores overdue and resubmission recalculates classification. Household schedules stay independent of viewer timezone; test midnight/DST boundaries.
- AC-004/005: Atomic approval creates one durable approval/star record and completes the occurrence; repeated/retried/competing independent transactions award exactly one. Test approval-vs-return/delete and stale versions explicitly, compatible outcome or conflict with refreshed state, never lost incompatible edits. Same transaction invokes006 recurrence hook: late scheduled/unscheduled/same-day cases, scheduler overlap and no backlog. Rerun P-03 one-off edit/delete restrictions after real return and recurring deletion preserving actual completions/stars. Visible aggregate UI remains008.
- AC-006: Real two-household unauthorized routes, CSRF, child/parent role separation, sanitized logs/responses, persistence after restart, and DB/request/lost-response failures with no false success. Stable Chrome/Firefox at1280×720/200% cover keyboard/focus, submit/approve/return/resubmit and explanatory notes; required server/concurrency/regression checks remain nonempty. Full reconnect transport behavior is009.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Dependency006 and grooming integrated; coordinator readiness reuses valid unchanged PM review. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM parallel scope review: 2026-10-28; acceptance IDs/behavior retained, concrete per-criterion checks and later integration ownership recorded. Draft until dependency/grooming integration and current readiness review; isolated grooming commit supplied to orchestrator for develop integration.

- Implementation summary: Actual assigned-child PIN submission with independently committed identity limits; server-receipt/browser-zone timeliness; protected required-note return/resubmission and atomic completion/unique one-star approval/recurrence; scoped conflicts and recoverable failures.
- Task branch / verified implementation commit: `task/007-review` / `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8` (developer verified; QA attempt1 FAIL, attempt2 BLOCKED)
- Changed files / revision: Chore model/migration/forms/review service/views, household routes, board read model/templates/local-date/submission JavaScript/CSS, affected board fixture and new review/browser checks; architecture/commands records.
- Final branch tip / delivery commit / integration results: Implementation above; following handoff records only. Integration pending independent QA.
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results:32 unique review cases and65 affected regressions PASS across scoped runs; stable Chrome156/Firefox159 native100/200 four flows and LA/Tokyo timeliness check PASS; migration/system/drift/static/Ruff/diff gates PASS. Exact selectors/results and resolved harness findings in the developer record.
- Verification records: [007 developer](../verification/007-review-developer.md); [independent QA attempt1](../verification/007-review-qa.md); [F001 developer investigation](../verification/007-review-f001-investigation.md); [independent QA attempt2](../verification/007-review-qa-attempt-2.md)
- Completion / integration evidence / outcome: Pending
- Remaining risks or blockers: F001 remains not QA-cleared. QA2 Firefox159 runs received GET `/accounts/login/` 200 but both timed out waiting for the Sign in heading before filling/submitting; page title, heading and response body length were not captured. Developer100/200 passes remain non-independent evidence. Needs narrow high-reasoning investigation and then QA attempt3/3 after correction. Chrome/server/timezone evidence retained. Visible aggregate totals/week filtering008; automatic synchronization/offline009.

- Coordinator readiness2026-10-29: reused PM grooming `8feda09b8b827736f832fd8dff6a48ece0e7075d`, unchanged scope/AC/contracts;006 integrated,65 affected tests/static/migration gates PASS. Actual award creation and deletion retention now mandatory with006 recurrence hook and003 child limiter integration; no scope change. Fresh developer next,0070/3.

- Developer handoff2026-10-29: immutable implementation `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8`; In review, QA0070/3 before dispatch, batch2 6/10. Owned verification browser/server/driver stopped; PG17 retained/PG13 preserved. User resume edit untouched/excluded; no merge/push.

- F001 investigation2026-10-29: returned In progress after independent QA0071 FAIL at8b66f1b; Firefox159 sign-in outcome unresolved. Narrow Firefox100 sanitized HTTP/redirect/focus probe next, then affected100/200 flow verification. No scope/AC change; batch2 6/10,0071/3 preserved.

- F001 developer handback2026-10-29: no code change justified; exact implementation8b66f1b unchanged. Firefox100 probe1 PASS9.68s, unchanged-helper100/200 repeat1 PASS17.42s with sanitized successful HTTP traces. In review for independent targeted recheck; F001 not QA-cleared. QA1 FAIL retained, next dispatch2/3 per coordinator; batch2 6/10.

- F001 proven setup cause2026-10-29: QA2 driver omitted documented `--allow-system-access`; synthetic page heading was present but native zoom returned500/System access required, swallowed by the wait helper. Minimal helper correction now surfaces zoom/setup errors and restores content context in finally. Product unchanged; targeted noflag/withflag and Firefox100/200 checks next. Attempts2/3, batch2 6/10; final QA dispatch3/3.
