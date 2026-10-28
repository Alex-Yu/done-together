# 007: Child submission, parent review, returns, and overdue rules

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/7
Local task: `_docs/tasks/007-review.md`
Requirement links: [REQ-016](../plan.md), [REQ-017](../plan.md), [REQ-018](../plan.md), [REQ-019](../plan.md), [REQ-023](../plan.md)
Dependencies: [006](006-recurrence.md) Done and integrated into `develop`; PM readiness review after that dependency.

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

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Where a criterion depends on another task, verify it after that dependency is integrated; do not mark unverified behavior complete.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM reviewed release scope and architecture during initial grooming; this task remains Draft until its dependency is Done/integrated and its current readiness review is recorded.

## Verification plan

PostgreSQL and browser tests exercise child-only submission, wrong/other-child PIN, duplicate submission, return notes including whitespace rejection, resubmission, expired unlock, and CSRF/outsider denial. Verify P-04 from validated browser timezone plus server receipt instant, invalid timezone, on-time/late pending classification and late return. Competing independent transactions exercise approval/approval, approval/return and deletion races with explicit stale conflicts. One atomic approval record/star is durable; same-day/late/unscheduled recurrence reconciliation uses task 006 services.

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
