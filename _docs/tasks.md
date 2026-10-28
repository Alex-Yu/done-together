# Backlog

Authoritative backlog: GitHub issues in [Alex-Yu/done-together](https://github.com/Alex-Yu/done-together/issues), selected after user scope confirmation under [process.md](process.md). Local task documents mirror the mapped GitHub issues; this file is the index/checkpoint.

Backlog mode / origin repository: GitHub — `git@github.com:Alex-Yu/done-together.git`, checked 2026-10-28.
Pending issue synchronization: Bootstrap issue publication/reconciliation. Tasks 001–010 are mapped to GitHub issues #1–#10; issue content/status and local mirrors verified by readback on 2026-10-28. Authentication works through GitHub CLI. Bootstrap tasks have now been refined locally for the selected architecture; issue publication/reconciliation is pending authorized delivery/backlog synchronization. No GitHub writes or readback occurred during this architecture-recording turn.

## Task index

Architecture was selected on 2026-10-28. All feature tasks remain Draft until dependency completion, PM grooming, and issue reconciliation. Scope was confirmed by the user on 2026-10-28, including P-01–P-07.

| ID / labels | Task | Status | Dependencies | GitHub issue |
| --- | --- | --- | --- | --- |
| `environment-setup` | [Set up the development environment](tasks/environment-setup.md) | Draft | Selected architecture; PM readiness review | Pending publication |
| application-skeleton | [Create a runnable application skeleton](tasks/application-skeleton.md) | Draft | environment-setup | Pending publication |
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

Preserve the `environment-setup` label and the skeleton dependency when those tasks are refined after architecture selection. Their local documents now contain concrete architecture-specific criteria; publish/reconcile them only within authorized backlog coordination before implementation. Feature requirement links, acceptance criteria, exclusions, and verification plans are in each task file.

## Checkpoint — 2026-10-28

- Phase: Architecture recorded after user stack selection; delivery has not been handed to an orchestrator.
- Agreed release: [plan.md](plan.md), REQ-001–REQ-027, D-01–D-07, P-01–P-07; product behavior unchanged.
- Current work: [architecture.md](architecture.md), ADR-001–003, [commands.md](commands.md) and local bootstrap tasks refined. Feature issues #1–#10 were synchronized in the prior specification phase; no remote issue state was rechecked in this turn.
- Implementation state: Documentation only, prepared for the user-requested architecture commit. No installs, scaffolding, application execution, task delivery branches, merges or pushes.
- Architecture / commands: Django + PostgreSQL + HTMX selected. Intended setup/run/verification commands explicitly UNVERIFIED. Runtime/patch compatibility and local services must be validated by bootstrap tasks.
- Per-task developer-to-QA attempts: Zero for every task, including bootstrap tasks.
- Delivery batch completions: Zero; no delivery batch started.
- Verification: `git diff --check` passed; local Markdown links checked across all nine changed/new documents with zero broken links; bootstrap acceptance IDs checked for uniqueness (7 setup, 5 skeleton), both tasks remain Draft, and explicit command UNVERIFIED status confirmed. No environment/application checks claimed.
- Push authorization: None.
- Pending synchronization: Publish/reconcile environment-setup and application-skeleton issues during authorized backlog coordination; read mapped issue updates before grooming features. No external write attempted in this documentation-only turn.
- Remaining decisions: Hosting, external email provider, budget, backups/recovery, distribution and production operations. These gate affected operational work, not isolated local bootstrap.
- Next action: User delivery handover under README step 4; then PM reads the role guide, reconciles authoritative issues, reviews bootstrap readiness and routes environment-setup to the developer. Do not start scaffolding before that handover and setup completion.

Source publication: The user authorized a local architecture documentation commit; no push is authorized or performed. Bootstrap issue publication is pending; existing feature issue source links may not reflect these local documents until an authorized push. Issue synchronization does not authorize source publication.
