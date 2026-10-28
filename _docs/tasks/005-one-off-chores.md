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

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Where a criterion depends on another task, verify it after that dependency is integrated; do not mark unverified behavior complete.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM reviewed release scope and architecture during initial grooming; this task remains Draft until its dependency is Done/integrated and its current readiness review is recorded.

## Verification plan

PostgreSQL/request tests and browser flows create/edit/delete one-off chores and reload/sign out/restart to prove persistence. Cover P-03: edits only in to-do, never edit awaiting/completed, deletion allowed for unfinished work while retaining completions/stars; seed states where needed before task 007. Reject blank titles, missing/foreign child, invalid date, unauthorized or stale version requests atomically. Two browser timezone contexts use the same due-date identity and show differing local overdue labels around midnight. Full submission timeliness is task 007.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Commands remain UNVERIFIED until their owning tasks execute them; dependency completion and current PM readiness review remain pending. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM scope review: 2026-10-28; requirements retained, selected architecture applied; Draft until dependency integration and current readiness review.

- Implementation summary: Not started
- Task branch / verified implementation commit: Pending
- Changed files / revision: Initial delivery grooming on `develop`; full grooming commit recorded in backlog checkpoint
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: Scope/architecture reviewed against confirmed requirements on 2026-10-28; issue reconciliation recorded in backlog checkpoint; implementation verification not run
- Verification record: Pending
- Orchestrator requirements re-check / evidence / outcome: Pending
- Remaining risks or blockers: Dependency integration and current readiness review; no material scope blocker found
