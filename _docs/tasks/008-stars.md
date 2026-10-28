# 008: Weekly/all-time stars and completion visibility

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/8
Local task: `_docs/tasks/008-stars.md`
Requirement links: [REQ-009](../plan.md), [REQ-019](../plan.md), [REQ-020](../plan.md), [REQ-025](../plan.md)
Dependencies: [007](007-review.md) Done and integrated into `develop`; PM readiness review after that dependency.

## Goal

Families see accurate approval-based totals and current-week completions.

## Acceptance criteria

- [ ] AC-001: REQ-009: Older overdue work remains visible; current-week completions are directly accessible; older completions leave the column but remain stored.
- [ ] AC-002: REQ-019: Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none.
- [ ] AC-003: REQ-020: Monday approval counts in the new week even for Sunday work; weekly rollover preserves history and all-time totals.
- [ ] AC-004: REQ-025: Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded.
- [ ] AC-005: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. This task remains Draft until its dependency is Done/integrated, this grooming is integrated onto `develop`, and current PM readiness is recorded. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

- AC-001: Board displays all active work (including older overdue) and all current-household-week approvals directly, no collapsed completions. Older completions leave view but remain stored. Exercise Monday rollover without mutations and reread after refresh;009 verifies periodic refresh on connected idle boards.
- AC-002: Weekly/all-time totals derive from unique persisted approval records, one star per occurrence irrespective of effort; submission/return contributes zero. Competing approvals/retries preserve one award and consistent visible totals. No variable values or redemption.
- AC-003: Use deterministic UTC instants spanning Monday00:00 in household IANA timezone, Sunday work approved Monday, differing viewer timezones and DST weeks. Approval time controls weekly membership, not due/submission time or viewer-local date. Weekly rollover preserves all-time/history and direct visibility rules.
- AC-004/005: Reload/sign-out/server-restart preserve totals/history; recurring definition deletion retains actual approved snapshots/stars and one-off completed deletion remains forbidden. Household-scoped totals/direct routes expose no foreign records or credentials; parent/child authority and expired unlock regressions still pass. Stable Chrome/Firefox at1280×720/200% verify keyboard/focus/text totals and no hidden current-week completions. No separate history screen; no completion retention expiry introduced.

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
