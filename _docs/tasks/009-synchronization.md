# 009: Synchronization, concurrent-action handling, and offline recovery

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/9
Local task: `_docs/tasks/009-synchronization.md`
Requirement links: [REQ-021](../plan.md), [REQ-022](../plan.md), [REQ-023](../plan.md)
Dependencies: [008](008-stars.md) Done and integrated into `develop`; PM readiness review after that dependency.

## Goal

Connected computers converge automatically and disconnected boards stay read-only.

## Acceptance criteria

- [ ] AC-001: REQ-021: Two-computer checks cover children, chores, submissions, reviews, and totals without manual refresh; confirmed target is five seconds (P-06).
- [ ] AC-002: REQ-022: Disconnect preserves visible board and disables actions; reconnect refreshes data automatically before actions resume.
- [ ] AC-003: REQ-023: Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed.
- [ ] AC-004: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Where a criterion depends on another task, verify it after that dependency is integrated; do not mark unverified behavior complete.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM reviewed release scope and architecture during initial grooming; this task remains Draft until its dependency is Done/integrated and its current readiness review is recorded.

## Verification plan

Use two independent browser contexts and measured accepted-mutation-to-visible-result latency ≤5 seconds for child/chore/submission/review/total changes. Test two-second version polling, consistent snapshots, no refresh when unchanged, preservation of focused input/open forms/unsaved text, midnight/week recalculation and polling not extending unlock. Simulate disconnection, failed polls, lost mutation responses, server recovery and stale concurrent edits/deletions: preserve the open board, show offline status, disable writes, refresh authorized snapshot before reenabling; confirmed authorization failure/sign-out clears private content. No persistent cache/service worker or offline reload promise.

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
