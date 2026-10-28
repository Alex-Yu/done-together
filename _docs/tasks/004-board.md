# 004: Shared board, empty states, and settings navigation

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/4
Local task: `_docs/tasks/004-board.md`
Requirement links: [REQ-008](../plan.md), [REQ-009](../plan.md), [REQ-024](../plan.md), [REQ-026](../plan.md)
Dependencies: [003](003-pins.md) Done; architecture selection and applicable grooming complete.

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

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Architecture is undecided: do not scaffold or choose dependencies from this task. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user confirmed scope on 2026-10-28; this task is not yet groomed or Ready.

## Verification plan

Map each AC to its named requirement's observable outcome using deterministic synthetic fixtures. Cover success, invalid input, unauthorized access, boundaries, and relevant failure/concurrency cases. Record reproducible procedures, actual observations, and exact implementation revision. Define architecture-specific commands and environments during grooming before Ready; unavailable checks remain BLOCKED. Final release verification must cover all journeys J-01–J-05 and P-01–P-07 on the integrated delivery revision.

## Questions and assumptions

Product scope confirmed; no remaining product questions. Architecture, concrete commands, test environment, and PM readiness review remain pending. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- Implementation summary: Not started
- Task branch / verified implementation commit: Pending
- Changed files / revision: Specification only; uncommitted
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: Task criteria drafted from confirmed requirements; GitHub issue synchronization verified by readback on 2026-10-28; implementation verification not run
- Verification record: Pending
- Orchestrator requirements re-check / evidence / outcome: Pending
- Remaining risks or blockers: Architecture selection, grooming, and dependencies
