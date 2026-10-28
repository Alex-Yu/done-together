# 003: Child profiles, parent/child PIN management, and protected shared access

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/3
Local task: `_docs/tasks/003-pins.md`
Requirement links: [REQ-004](../plan.md), [REQ-005](../plan.md), [REQ-006](../plan.md), [REQ-007](../plan.md), [REQ-027](../plan.md)
Dependencies: [002](002-households.md) Done; architecture selection and applicable grooming complete.

## Goal

Children have submission identities and either parent can securely unlock management.

## Acceptance criteria

- [ ] AC-001: REQ-004: Protected settings add children/reset child PINs; own password authorizes own parent PIN reset; replaced PINs fail. Four-digit PINs preserve leading zeroes.
- [ ] AC-002: REQ-005: Either valid parent PIN unlocks management; child/incorrect PINs and locked requests cannot perform parent actions.
- [ ] AC-003: REQ-006: After 60 seconds, management requires a PIN again. Board viewing and child activity do not extend parent access.
- [ ] AC-004: REQ-007: Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits.
- [ ] AC-005: REQ-027: Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions.
- [ ] AC-006: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

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
