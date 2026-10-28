# 003: Child profiles, parent/child PIN management, and protected shared access

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/3
Local task: `_docs/tasks/003-pins.md`
Requirement links: [REQ-004](../plan.md), [REQ-005](../plan.md), [REQ-006](../plan.md), [REQ-007](../plan.md), [REQ-027](../plan.md)
Dependencies: [002](002-households.md) Done and integrated into `develop`; PM readiness review after that dependency.

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

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM reviewed release scope and architecture during initial grooming; this task remains Draft until its dependency is Done/integrated and its current readiness review is recorded.

## Verification plan

Use server-side board-session unlocks with selected member identity, even when another parent opened the board. Test leading-zero four-digit PINs, invalid format, PIN replacement, wrong own password, selecting the other parent, outsider/child/direct-request denial and CSRF. Verify 60-second expiry at the boundary; only accepted explicit parent activity extends it, while viewing/polling/child requests do not. PostgreSQL integration checks five failures/five minutes across independent sessions and no deadline extension. Inspect hashes/pepper separation and sanitized responses/logs.

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
