# Backlog

Authoritative backlog: GitHub issues in [Alex-Yu/done-together](https://github.com/Alex-Yu/done-together/issues), selected after user scope confirmation under [process.md](process.md). Local task documents mirror the mapped GitHub issues; this file is the index/checkpoint.

Backlog mode / origin repository: GitHub — `git@github.com:Alex-Yu/done-together.git`, checked 2026-10-28.
Pending issue synchronization: None. Tasks 001–010 are mapped to GitHub issues #1–#10; issue content/status and local mirrors verified by readback on 2026-10-28. Authentication works through GitHub CLI. Bootstrap templates remain unpublished until architecture refinement.

## Task index

All feature tasks remain Draft until architecture selection, dependency completion, PM grooming, and issue reconciliation. Scope was confirmed by the user on 2026-10-28, including P-01–P-07.

| ID / labels | Task | Status | Dependencies | GitHub issue |
| --- | --- | --- | --- | --- |
| `environment-setup` | [Set up the development environment](tasks/environment-setup.md) | Draft | Architecture reviewed | Not published: unresolved template details |
| application-skeleton | [Create a runnable application skeleton](tasks/application-skeleton.md) | Draft | environment-setup | Not published: unresolved template details |
| 001 | [Account registration, verification, sign-in, recovery, and safeguards](tasks/001-accounts.md) | Draft | application-skeleton | [#1](https://github.com/Alex-Yu/done-together/issues/1) |
| 002 | [Household creation, timezone setup, and second-parent invitation](tasks/002-households.md) | Draft | 001 | [#2](https://github.com/Alex-Yu/done-together/issues/2) |
| 003 | [Child profiles, parent/child PIN management, and protected shared access](tasks/003-pins.md) | Draft | 002 | [#3](https://github.com/Alex-Yu/done-together/issues/3) |
| 004 | [Shared board, empty states, and settings navigation](tasks/004-board.md) | Draft | 003 | [#4](https://github.com/Alex-Yu/done-together/issues/4) |
| 005 | [One-off chore assignment and maintenance](tasks/005-one-off-chores.md) | Draft | 004 | [#5](https://github.com/Alex-Yu/done-together/issues/5) |
| 006 | [Recurrence, occurrence generation, future edits, and deletion](tasks/006-recurrence.md) | Draft | 005 | [#6](https://github.com/Alex-Yu/done-together/issues/6) |
| 007 | [Child submission, parent review, returns, and overdue rules](tasks/007-review.md) | Draft | 006 | [#7](https://github.com/Alex-Yu/done-together/issues/7) |
| 008 | [Weekly/all-time stars and completion visibility](tasks/008-stars.md) | Draft | 007 | [#8](https://github.com/Alex-Yu/done-together/issues/8) |
| 009 | [Synchronization, concurrent-action handling, and offline recovery](tasks/009-synchronization.md) | Draft | 008 | [#9](https://github.com/Alex-Yu/done-together/issues/9) |
| 010 | [Integrated release verification and browser/accessibility checks](tasks/010-release-verification.md) | Draft | 009 | [#10](https://github.com/Alex-Yu/done-together/issues/10) |

Preserve the `environment-setup` label and the skeleton dependency when those tasks are refined after architecture selection. Do not create issues for their current unresolved template content. Feature requirement links, acceptance criteria, exclusions, and verification plans are in each task file.

## Checkpoint — 2026-10-28

- Phase: Product specification and Draft backlog preparation; delivery has not been handed to an orchestrator.
- Agreed release: [plan.md](plan.md), REQ-001–REQ-027, D-01–D-07, P-01–P-07.
- Current work: Draft tasks 001–010 synchronized with open GitHub issues #1–#10.
- Implementation state: No application code; documentation changes are uncommitted; pre-existing untracked `initial-plan.md` preserved.
- Architecture / commands: Undecided / unconfigured; no Ready implementation tasks.
- Per-task developer-to-QA attempts: Zero for every task, including bootstrap tasks.
- Delivery batch completions: Zero; no delivery batch started.
- Verification: Specification consistency, diff checks, and GitHub issue content/status readback; no application checks claimed.
- Push authorization: None. No commits, merges, pushes, or deployment performed.
- Blocker: None for issue synchronization. Architecture remains undecided; implementation tasks remain Draft.
- Next action: Compare architecture approaches with the user, record their selection, and refine bootstrap tasks before delivery handover. Read mapped issue updates before future grooming or handoffs.

Source publication: Product specifications and local task files remain uncommitted/unpushed. Issues contain complete task bodies; source links may show the older template or remain unavailable until an authorized push. Issue synchronization does not authorize source publication.
