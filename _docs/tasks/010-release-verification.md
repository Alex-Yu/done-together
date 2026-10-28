# 010: Integrated release verification and browser/accessibility checks

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/10
Local task: `_docs/tasks/010-release-verification.md`
Requirement links: [REQ-001](../plan.md), [REQ-002](../plan.md), [REQ-003](../plan.md), [REQ-004](../plan.md), [REQ-005](../plan.md), [REQ-006](../plan.md), [REQ-007](../plan.md), [REQ-008](../plan.md), [REQ-009](../plan.md), [REQ-010](../plan.md), [REQ-011](../plan.md), [REQ-012](../plan.md), [REQ-013](../plan.md), [REQ-014](../plan.md), [REQ-015](../plan.md), [REQ-016](../plan.md), [REQ-017](../plan.md), [REQ-018](../plan.md), [REQ-019](../plan.md), [REQ-020](../plan.md), [REQ-021](../plan.md), [REQ-022](../plan.md), [REQ-023](../plan.md), [REQ-024](../plan.md), [REQ-025](../plan.md), [REQ-026](../plan.md), [REQ-027](../plan.md)
Dependencies: [009](009-synchronization.md) Done and integrated into `develop`; PM readiness review after that dependency.

## Goal

Verify all agreed release requirements on the integrated delivery revision.

## Acceptance criteria

- [ ] AC-001: REQ-001: Verified parents can sign in; unverified accounts cannot access household data; password recovery invalidates the old password; invalid/expired links deny access.
- [ ] AC-002: REQ-002: Intended verified recipient joins once; wrong-address, reused, and expired invitations fail; an expired invitation can be replaced.
- [ ] AC-003: REQ-003: Either member parent can manage the household; outsiders cannot read or change it through UI or direct requests.
- [ ] AC-004: REQ-004: Protected settings add children/reset child PINs; own password authorizes own parent PIN reset; replaced PINs fail. Four-digit PINs preserve leading zeroes.
- [ ] AC-005: REQ-005: Either valid parent PIN unlocks management; child/incorrect PINs and locked requests cannot perform parent actions.
- [ ] AC-006: REQ-006: After 60 seconds, management requires a PIN again. Board viewing and child activity do not extend parent access.
- [ ] AC-007: REQ-007: Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits.
- [ ] AC-008: REQ-008: Mixed-state assignments appear under the correct child; states are understandable without color alone; empty states guide setup.
- [ ] AC-009: REQ-009: Older overdue work remains visible; current-week completions are directly accessible; older completions leave the column but remain stored.
- [ ] AC-010: REQ-010: Parent can create each type; missing/invalid title, child, or date/schedule cannot create partial work. Children cannot claim or reassign work.
- [ ] AC-011: REQ-011: Different-timezone computers agree on occurrence identity and dates but may show different overdue labels at the same instant.
- [ ] AC-012: REQ-012: Leaving daily work unfinished over several days, including awaiting approval, produces one outstanding item and no backlog after approval.
- [ ] AC-013: REQ-013: Approving overdue Monday work on scheduled Wednesday completes Monday and creates Wednesday once; an unscheduled approval day waits for the next scheduled day.
- [ ] AC-014: REQ-014: Editing title, assignment, or schedule leaves current occurrence details and completed history unchanged; subsequent occurrences use the edit.
- [ ] AC-015: REQ-015: Deleting a definition removes to-do/awaiting-approval work and stops recurrence; prior approvals/history/star totals persist.
- [ ] AC-016: REQ-016: Correct PIN moves eligible work to awaiting approval; incorrect/another child's PIN or duplicate requests cannot create unauthorized transitions.
- [ ] AC-017: REQ-017: Approval completes work; empty return note is rejected; valid return shows the note and restores to-do; child can retry.
- [ ] AC-018: REQ-018: Submission before deadline remains non-overdue after it while awaiting approval; return after deadline restores overdue. Apply P-04 timeliness classification.
- [ ] AC-019: REQ-019: Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none.
- [ ] AC-020: REQ-020: Monday approval counts in the new week even for Sunday work; weekly rollover preserves history and all-time totals.
- [ ] AC-021: REQ-021: Two-computer checks cover children, chores, submissions, reviews, and totals without manual refresh; confirmed target is five seconds (P-06).
- [ ] AC-022: REQ-022: Disconnect preserves visible board and disables actions; reconnect refreshes data automatically before actions resume.
- [ ] AC-023: REQ-023: Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed.
- [ ] AC-024: REQ-024: Chores/reviews are managed on the board; accounts/children/PINs in settings; no separate dashboard, sounds, or reminder notifications are required.
- [ ] AC-025: REQ-025: Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded.
- [ ] AC-026: REQ-026: Core journeys work with keyboard and visible focus, labeled inputs, and text status equivalents; agreed browser/viewport/zoom checks pass.
- [ ] AC-027: REQ-027: Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. This task remains Draft until its dependency is Done/integrated, this grooming is integrated onto `develop`, and current PM readiness is recorded. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

QA verifies the exact integrated delivery revision against every AC-001–027, not only prior task verdicts. Record a requirement→journey→test/manual evidence matrix, actual commands/results, stable browser versions and unverified limitations. Use synthetic households and separate test PostgreSQL/in-memory mail; local Mailpit account/invitation capture is explicit and no external provider/deployment is authorized.

- AC-001–007/027, J-01/J-05: Fresh registration/verification/recovery/invitation through captured email; one-hour/seven-day expiry/single use/wrong recipient, one-household/two-parent concurrent limits, actual household isolation, selected-parent password reset, either-parent unlock, five-failure/five-minute identity limits across contexts, 60-second parent-only inactivity and CSRF/private-log checks.
- AC-008–018/024, J-02/J-03/J-04: Keyboard board/settings setup and each real one-off/daily/weekday workflow; exact P-03 edit/delete restrictions, returned notes/resubmission, browser-local timeliness across zones, late/unscheduled recurrence, no-browser scheduler recovery/overlap, future-only edits/deletion retaining earned records. No synthetic service-only fixture substitutes for final integrated HTTP/browser behavior.
- AC-019/020/025, J-03/J-04: Competing approvals award one durable star; approval-time household Monday boundaries/DST rollover, visible current-week completions/all active work and all-time persistence after reload/sign-out/server/scheduler restart and recurrence deletion.
- AC-021–023/026, J-05: Measured ≤5-second two-context synchronization across change classes, preserve unsaved focus/forms, failed/lost responses, stale conflicts, offline preserved view with disabled writes and fresh authorized reconnect; installed stable Chrome/Firefox at1280×720 and native200% zoom, keyboard/focus/labels/status equivalents. Bundled Playwright Firefox does not certify installed stable Firefox.
- Execute validated commands.md Django checks, drift, Ruff lint/format, full PostgreSQL server/concurrency suite, both bundled browser suites, static collection and scheduler once/loop checks. Document startup/readiness/clean shutdown and services left running; unavailable required check is BLOCKED.
- Orchestrator requirements review occurs at this release stage only and records outcome/evidence at the same final code revision. Final delivery needs independent integrated QA PASS plus this release review PASS. Defects become scoped tasks/fixes with fresh QA and repeat affected release evidence; do not weaken requirements. This task is release verification, not deployment or a second implementation of features.

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
- Orchestrator final release requirements review / evidence / outcome: Pending
- Remaining risks or blockers: Dependency integration and current readiness review; no material scope blocker found
