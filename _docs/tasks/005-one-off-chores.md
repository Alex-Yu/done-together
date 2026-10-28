# 005: One-off chore assignment and maintenance

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/5
Local task: `_docs/tasks/005-one-off-chores.md`
Requirement links: [REQ-010](../plan.md), [REQ-011](../plan.md), [REQ-025](../plan.md)
Dependencies: [004](004-board.md) Done and integrated into `develop`; PM readiness review after that dependency.

## Goal

Parents can assign and maintain dated one-off work using P-03 rules.

## Acceptance criteria

- [ ] AC-001: REQ-010: Create titled one-off chores with a specific child and due date; reject invalid input without partial work. Apply P-03 edits/deletion. Recurrence is covered by task 006.
- [ ] AC-002: REQ-011: Different-timezone computers agree on occurrence identity and dates but may show different overdue labels at the same instant.
- [ ] AC-003: REQ-025: Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded.
- [ ] AC-004: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

P-03 is binding: one-off edit/delete only in to-do; awaiting approval must first be returned, and completed work cannot be edited/deleted. This differs from recurring deletion in006.

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. This task remains Draft until its dependency is Done/integrated, this grooming is integrated onto `develop`, and current PM readiness is recorded. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

- AC-001: Parent-unlocked board flows create, edit and delete dated one-off work assigned to a household child. Blank title, missing/foreign child, invalid/missing date, expired authority and stale version requests leave definitions/occurrences unchanged. P-03 is exact: edit/delete only while to-do; awaiting-approval must first be returned in007; completed work cannot be edited/deleted. Seed awaiting/completed state fixtures to prove direct and UI denial now, without claiming review UI exists. Reassignment updates an eligible one-off consistently; children cannot claim/reassign work.
- AC-002: Two timezone browser contexts share identical occurrence identity/date but show their own overdue label around local midnight. Use server-controlled instants and valid IANA context, including DST calendar dates. No individual due time is added; submission timeliness preservation is007.
- AC-003: Real PostgreSQL reload/sign-out/server-restart retains definitions/occurrences. Deleting eligible to-do work removes only that work; seeded completed history is retained and protected from deletion. Durable approval/star creation is007 and visible totals008; this task does not create fake earned stars to substitute for those workflows.
- AC-004: Actual two-household child/work identifiers, locked parent/child/outsider requests and CSRF are denied; failures do not show committed success. Version checks reject incompatible concurrent edits/deletion and refresh explicitly. Advance household board revision atomically for accepted board-affecting changes so009 can poll it. Stable Chrome/Firefox keyboard/focus/labeled create/edit/delete/error journeys at1280×720/200% and server/regression suites provide evidence.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Parallel preparation is not readiness: dependency integration, grooming integration onto develop and current PM review remain pending. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

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
- Remaining risks or blockers: Dependency integration and current readiness review; no material scope blocker found
