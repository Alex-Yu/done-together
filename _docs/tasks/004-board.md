# 004: Shared board, empty states, and settings navigation

Status: Done
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/4
Local task: `_docs/tasks/004-board.md`
Requirement links: [REQ-008](../plan.md), [REQ-009](../plan.md), [REQ-024](../plan.md), [REQ-026](../plan.md)
Dependencies: [003](003-pins.md) Done/integrated at `8218a22e1b015e89be45aad814f5188150fafe4b`; independent QA1 PASS implementation `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`; PM current readiness passed on 2026-10-29.

## Goal

Families can consult child columns and parents can navigate protected settings.

## Acceptance criteria

- [x] AC-001: REQ-008: Mixed-state assignments appear under the correct child; states are understandable without color alone; empty states guide setup.
- [x] AC-002: REQ-009: Provide directly visible active/completed states with no collapsed completion section; final approval-based data and weekly rollover are integrated in task 008.
- [x] AC-003: REQ-024: Chores/reviews are managed on the board; accounts/children/PINs in settings; no separate dashboard, sounds, or reminder notifications are required.
- [x] AC-004: REQ-026: Core journeys work with keyboard and visible focus, labeled inputs, and text status equivalents; agreed browser/viewport/zoom checks pass.
- [x] AC-005: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Mixed-state presentation uses test-only synthetic read-model fixtures until005/006 provide persisted work;007 wires review UI,008 actual approval totals,009 automatic cross-board refresh. Preserve requirement ownership without fake production household data.

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. Dependency003, parallel grooming8feda09 and QA preparation are integrated onto `develop`. Current PM review confirms all five criteria, exclusions, constraints and verification plan complete; this task is Ready. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

Use the integrated [QA preparation matrix](../verification/plans/003-006-identity-board-assignment.md) alongside the plan below. Real child columns, empty states and protected navigation are production behavior now; mixed chore states are internal test fixtures only until005–008. Preserve003 server timeout and locked board visibility; no production fake chores, fake totals, inert product controls or separate dashboard are required.

- AC-001: Use a synthetic read-model fixture to display multiple children with to-do, overdue, awaiting and completed entries under the correct column; statuses include text independent of color. Empty household/child/work states guide allowed setup. Production reads remain real household scoped; synthetic state injection is test-only. Full persisted chore definitions/occurrences arrive005/006; submission/review state changes arrive007.
- AC-002: Browser checks confirm active work and current-week completion entries are directly visible without a collapsed completed section. Seed older overdue and completed dates to exercise the presentation contract; approval-derived week filtering and totals are verified in008. Do not claim actual approval/rollover workflows complete now.
- AC-003: Board is the shared entry surface and settings contains account/child/PIN management. Both parents can select/unlock their own identity using003; controls expire while board stays visible. Reserve chore/review controls on the board for005–007 without inventing a separate dashboard or operational reminders.
- AC-004/005: Stable Chrome/Firefox at1280×720 and native200% zoom, keyboard-only/focus/labels/status text, long synthetic names and recoverable errors. Use two actual households to test authorized board reads/settings navigation and denied outsider/locked management direct requests; no sensitive credential material. Recheck existing account/household/PIN suites and data persistence. Test locked board after inactivity; automated bundled Firefox does not replace installed stable Firefox evidence.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Dependency/grooming integration and current PM readiness are complete. Test-only mixed-state fixtures verify presentation boundaries now; actual chore/review/approval-derived week behavior remains005–008 and final010. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM readiness: Ready on 2026-10-29 after003 integration; five ACs unchanged, integrated scope/QA preparation reviewed, no consequential question. Full readiness commit recorded in backlog checkpoint.

- Implementation summary: Real scoped child columns, setup/empty guidance, semantic text-state card projection and shared board entry; settings keeps parent guard. No production fake work.
- Task branch / verified implementation commit: `task/004-board`; `067addc7eda122736893d17d5ca4aff7ce1a2885`
- Changed files / revision: Board read model/views/templates/CSS, scoped tests/native check and documentation; no schema/dependency change
- Final branch tip / delivery commit / integration results: Final task tip/fast-forward delivery `bd608632e14d9a98aea957f82c433d8f03dc1ebc`; no implementation changes during integration
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: Five unique board tests,20 affected PIN regressions and four installed Chrome/Firefox100/200% native cases PASS; check/drift/lint/format/diff PASS. Prior unchanged mail/61-second evidence reused; full integrated regression at010.
- Verification record: [Developer AC table](../verification/004-board-developer.md); [independent QA PASS](../verification/004-board-qa.md)
- Completion / integration evidence / outcome: Independent QA1 PASS all five criteria; integrated. Migrate/check/drift,25 affected board/PIN tests,Ruff lint/format114 files,diff check PASS; retained native QA evidence unchanged
- Remaining risks or blockers: No QA findings; persisted work/review/approval week visibility/totals remain005–008; no source pushes authorized
