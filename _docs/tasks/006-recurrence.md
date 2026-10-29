# 006: Recurrence, occurrence generation, future edits, and deletion

Status: Ready
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/6
Local task: `_docs/tasks/006-recurrence.md`
Requirement links: [REQ-010](../plan.md), [REQ-011](../plan.md), [REQ-012](../plan.md), [REQ-013](../plan.md), [REQ-014](../plan.md), [REQ-015](../plan.md), [REQ-025](../plan.md)
Dependencies: [005](005-one-off-chores.md) Done/integrated `c846fffc548961e5c800bd56583e84d3b9cf96c9`; independent QA1 and affected integration gates PASS.

## Goal

Fixed recurring schedules generate shared work without duplicate unfinished occurrences or missed-date backlogs.

## Acceptance criteria

- [ ] AC-001: REQ-010: Create daily and selected-weekday recurring definitions with required title and child; apply P-07 initial generation and no-browser recovery.
- [ ] AC-002: REQ-011: Different-timezone computers agree on occurrence identity and dates but may show different overdue labels at the same instant.
- [ ] AC-003: REQ-012: Leaving daily work unfinished over several days, including awaiting approval, produces one outstanding item and no backlog after approval.
- [ ] AC-004: REQ-013: Approving overdue Monday work on scheduled Wednesday completes Monday and creates Wednesday once; an unscheduled approval day waits for the next scheduled day.
- [ ] AC-005: REQ-014: Editing title, assignment, or schedule leaves current occurrence details and completed history unchanged; subsequent occurrences use the edit.
- [ ] AC-006: REQ-015: Deleting a definition removes to-do/awaiting-approval work and stops recurrence; prior approvals/history/star totals persist.
- [ ] AC-007: REQ-025: Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded.
- [ ] AC-008: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. Ready on2026-10-29: coordinator reused unchanged PM scope review `8feda09b8b827736f832fd8dff6a48ece0e7075d`; dependency005 and grooming integrated; eight criteria/contracts/verification plan unchanged. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

- AC-001/002: Parent-unlocked daily/selected-weekday creation rejects empty/invalid schedule/title/foreign child atomically. Household timezone controls calendar scheduling, browser-local overdue labels retain shared occurrence identity. P-07 creates first scheduled date on/after creation, and recovery with no unfinished work generates only latest eligible date by today; never generate before creation or missed-date backlog. Test timezone/DST boundary instants and fixed weekdays.
- AC-003/004: PostgreSQL fixtures span multiple days with to-do and awaiting work: at most one unfinished occurrence. Complete an overdue Monday fixture atomically through the recurrence completion hook on scheduled Wednesday: retain Monday snapshot and create Wednesday once; unscheduled approval day waits for next scheduled date; completing today's work cannot recreate today. Actual child submission, protected approval HTTP action and unique star award are wired/verified007; no review UI is claimed complete here.
- AC-005/006/007: Edits to title/child/schedule affect future snapshots only, retaining current/completed details. Recurring deletion removes to-do/awaiting work and stops generation, retaining completed snapshots and approval records when present. Exercise synthetic history now and rerun actual award retention after007/008. Persist across reload/sign-out/scheduler restart; fixed recurrence never shifts after late completion.
- AC-008: Independent PostgreSQL transactions test overlapping scheduler runs, generation vs edit/deletion, completion hook vs scheduler and one-unfinished/definition-date uniqueness under definition-first lock order. Household scope, parent guard, CSRF, version conflicts and recoverable failures apply to UI/direct requests. Record `reconcile_recurrence --once` idempotence and `--loop --interval 60` with browsers closed, clean interrupt, observed next scheduled work and safe retry/restart after temporary failure; no Redis/Celery required. Stable-browser accessible schedule/edit/delete journeys plus required regressions.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Dependency005 and grooming integrated; coordinator readiness reuses valid unchanged PM scope review. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM parallel scope review: 2026-10-28; acceptance IDs/behavior retained, concrete per-criterion checks and later integration ownership recorded. Draft until dependency/grooming integration and current readiness review; isolated grooming commit supplied to orchestrator for develop integration.

- Implementation summary: Not started
- Task branch / verified implementation commit: Pending
- Changed files / revision: Parallel grooming in isolated `grooming/future-release`; full commit supplied to orchestrator for integration onto develop before readiness
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: PM scope/architecture/AC-link consistency checked; issue3–10 Draft bodies synchronized/readback during parallel grooming. No implementation verification run or claimed
- Verification record: Pending
- Completion / integration evidence / outcome: Pending
- Remaining risks or blockers: None for implementation. Actual submission/approval/star HTTP workflow remains007; totals008; synchronization009.

- Coordinator readiness2026-10-29: reused PM grooming `8feda09b8b827736f832fd8dff6a48ece0e7075d`, unchanged scope/AC/contracts.005 dependency integrated and37 affected integration tests/static/migration gates PASS. No repeat PM required. Fresh task-only developer next;006 attempts0/3.
