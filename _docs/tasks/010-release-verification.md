# 010: Integrated release verification and browser/accessibility checks

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/10
Local task: `_docs/tasks/010-release-verification.md`
Requirement links: [REQ-001](../plan.md), [REQ-002](../plan.md), [REQ-003](../plan.md), [REQ-004](../plan.md), [REQ-005](../plan.md), [REQ-006](../plan.md), [REQ-007](../plan.md), [REQ-008](../plan.md), [REQ-009](../plan.md), [REQ-010](../plan.md), [REQ-011](../plan.md), [REQ-012](../plan.md), [REQ-013](../plan.md), [REQ-014](../plan.md), [REQ-015](../plan.md), [REQ-016](../plan.md), [REQ-017](../plan.md), [REQ-018](../plan.md), [REQ-019](../plan.md), [REQ-020](../plan.md), [REQ-021](../plan.md), [REQ-022](../plan.md), [REQ-023](../plan.md), [REQ-024](../plan.md), [REQ-025](../plan.md), [REQ-026](../plan.md), [REQ-027](../plan.md)
Dependencies: [009](009-synchronization.md) Done; architecture selection and applicable grooming complete.

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
