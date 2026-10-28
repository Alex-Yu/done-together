# 006: Recurrence, occurrence generation, future edits, and deletion

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/6
Local task: `_docs/tasks/006-recurrence.md`
Requirement links: [REQ-010](../plan.md), [REQ-011](../plan.md), [REQ-012](../plan.md), [REQ-013](../plan.md), [REQ-014](../plan.md), [REQ-015](../plan.md), [REQ-025](../plan.md)
Dependencies: [005](005-one-off-chores.md) Done and integrated into `develop`; PM readiness review after that dependency.

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

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Where a criterion depends on another task, verify it after that dependency is integrated; do not mark unverified behavior complete.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM reviewed release scope and architecture during initial grooming; this task remains Draft until its dependency is Done/integrated and its current readiness review is recorded.

## Verification plan

Implement the documented reconcile_recurrence --once and --loop --interval 60 commands using the same domain service as the later approval flow. Test creation today/next scheduled day and P-07 recovery latest-eligible-date behavior with no browsers, DST/calendar boundaries, unfinished/awaiting work across days, duplicate/overlapping schedulers, future-only edits and deletion preserving snapshots. PostgreSQL independent transactions exercise uniqueness and definition-first lock ordering. Exercise recurrence after a synthetic atomic completion at the service boundary; task 007 wires and verifies the actual approval request and star award together.

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
- Completion / integration evidence / outcome: Pending
- Remaining risks or blockers: Dependency integration and current readiness review; no material scope blocker found
