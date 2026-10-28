# 008: Weekly/all-time stars and completion visibility

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/8
Local task: `_docs/tasks/008-stars.md`
Requirement links: [REQ-009](../plan.md), [REQ-019](../plan.md), [REQ-020](../plan.md), [REQ-025](../plan.md)
Dependencies: [007](007-review.md) Done; architecture selection and applicable grooming complete.

## Goal

Families see accurate approval-based totals and current-week completions.

## Acceptance criteria

- [ ] AC-001: REQ-009: Older overdue work remains visible; current-week completions are directly accessible; older completions leave the column but remain stored.
- [ ] AC-002: REQ-019: Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none.
- [ ] AC-003: REQ-020: Monday approval counts in the new week even for Sunday work; weekly rollover preserves history and all-time totals.
- [ ] AC-004: REQ-025: Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded.
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
