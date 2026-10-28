# 004: Shared board, empty states, and settings navigation

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/4
Local task: `_docs/tasks/004-board.md`
Requirement links: [REQ-008](../plan.md), [REQ-009](../plan.md), [REQ-024](../plan.md), [REQ-026](../plan.md)
Dependencies: [003](003-pins.md) Done and integrated into `develop`; PM readiness review after that dependency.

## Goal

Families can consult child columns and parents can navigate protected settings.

## Acceptance criteria

- [ ] AC-001: REQ-008: Mixed-state assignments appear under the correct child; states are understandable without color alone; empty states guide setup.
- [ ] AC-002: REQ-009: Provide directly visible active/completed states with no collapsed completion section; final approval-based data and weekly rollover are integrated in task 008.
- [ ] AC-003: REQ-024: Chores/reviews are managed on the board; accounts/children/PINs in settings; no separate dashboard, sounds, or reminder notifications are required.
- [ ] AC-004: REQ-026: Core journeys work with keyboard and visible focus, labeled inputs, and text status equivalents; agreed browser/viewport/zoom checks pass.
- [ ] AC-005: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Where a criterion depends on another task, verify it after that dependency is integrated; do not mark unverified behavior complete.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM reviewed release scope and architecture during initial grooming; this task remains Draft until its dependency is Done/integrated and its current readiness review is recorded.

## Verification plan

Use seeded synthetic read-model states until chore workflows arrive. Browser checks cover one column/child, textual state/overdue labels, visible active and completed entries without a collapsed section, empty setup guidance, board/settings navigation, membership and locked-control denial. Check stable Chrome/Firefox, 1280×720, keyboard focus, labeled controls and 200% zoom; record exact versions. Workflow mutations and approval-based week totals are integrated by tasks 005–008.

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
