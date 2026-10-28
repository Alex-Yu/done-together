# Backlog

Authoritative backlog: GitHub issues in [Alex-Yu/done-together](https://github.com/Alex-Yu/done-together/issues), selected after user scope confirmation under [process.md](process.md). Local task documents mirror the mapped GitHub issues; this file is the index/checkpoint.

Backlog mode / origin repository: GitHub — `git@github.com:Alex-Yu/done-together.git`, checked 2026-10-28.
Pending issue synchronization: None after initial delivery grooming; bootstrap issues #11/#12 and existing feature issues #1–#10 updated and exact-body readback verified on 2026-10-28 (source link formatting normalized). Local commits remain unpushed.

## Task index

Delivery handed over on 2026-10-28. PM reviewed bootstrap scope and the feature roadmap against the selected architecture. Only environment-setup is Ready; dependent tasks remain Draft until their dependency integrates and current readiness is reviewed. Scope was confirmed by the user on 2026-10-28, including P-01–P-07.

| ID / labels | Task | Status | Dependencies | GitHub issue |
| --- | --- | --- | --- | --- |
| `environment-setup` | [Set up the development environment](tasks/environment-setup.md) | In review | None; PM readiness passed | [#11](https://github.com/Alex-Yu/done-together/issues/11) |
| application-skeleton | [Create a runnable application skeleton](tasks/application-skeleton.md) | Draft | environment-setup | [#12](https://github.com/Alex-Yu/done-together/issues/12) |
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

Bootstrap criteria preserve environment-before-skeleton separation. PM reconciled all feature tasks to the selected architecture, retained stable acceptance IDs, and made later integration ownership explicit where features depend on later workflows. No requirement is claimed complete by grooming.

## Checkpoint — 2026-10-28

- Phase: Delegated delivery started; PM grooming complete; route Ready environment-setup to developer.
- Agreed task set: environment-setup, application-skeleton, 001–010 (12 tasks); [plan.md](plan.md) REQ-001–027, D-01–07, P-01–07 unchanged.
- Delivery branch / starting state: `develop` created from `main` at `b8ea110`; no implementation exists yet. PM grooming commit: `66245f5fcde8bce1e189b7ff86885a3d232b8d7d` on `develop`; contains all 12 task mirrors and synchronized scope. Subsequent checkpoint-only commit records this hash without changing task scope.
- Current role/task: PM handoff → developer / [environment-setup](tasks/environment-setup.md); create `task/environment-setup` from committed grooming on develop.
- Readiness: environment-setup Ready; skeleton scope refined but Draft until setup Done/integrated; features Draft pending integrated dependencies/current PM review.
- Architecture / commands: Django + PostgreSQL + HTMX; commands remain UNVERIFIED until executed. Preserve unrelated PostgreSQL 13 on 5432; developer uses isolated project-owned PostgreSQL 17 on loopback 55432 and project-local tooling/cache where needed.
- Per-task developer-to-QA attempts: environment-setup 2/3; application-skeleton 0/3; 001 0/3; 002 0/3; 003 0/3; 004 0/3; 005 0/3; 006 0/3; 007 0/3; 008 0/3; 009 0/3; 010 0/3. Attempts persist across sessions/batches.
- Delivery batch: 1; completions 0/10. Default limit stops after ten completed tasks (through 008 if sequential); 009/010 require explicit batch renewal before continuation. Do not claim full release then.
- Verification evidence: PM scope/architecture review and exact issue-body readback only; no environment/application checks or QA verdict claimed. Developer and independent QA must verify every setup criterion before completion.
- GitHub: origin `git@github.com:Alex-Yu/done-together.git` confirmed. Issues #1–#12 read/reconciled; #11 environment-setup with preserved label, #12 skeleton newly created; all open. No pending synchronization.
- Push authorization: None; do not push local develop/task branches. Issue updates are authorized separately.
- Remaining decisions: Production hosting/provider/budget/operations remain out of local release scope; no consequential local product question identified. Tool/access failures route to developer, then request only specific missing access if necessary.
- Next routing action: Developer implements one Ready setup task from full grooming commit; commit and submit exact revision to QA (consumes attempt 1); orchestrator re-check follows QA PASS before Done/merge.

Source publication: Issue bodies contain complete specifications; local source is unpushed. Issue links to develop source may not resolve until separately authorized source publication.

## Developer handoff — environment-setup, 2026-10-28

- Current role/task: Developer implementation complete; route `environment-setup` to independent QA.
- Task branch: `task/environment-setup`, created from PM checkpoint18e9ab25fb08609d6709ce8af5e866486bee4fe3 and includes grooming66245f5fcde8bce1e189b7ff86885a3d232b8d7d.
- Exact implementation commit: `f31e725ed4356ee142370cf8323e36f9ea43d8d5`. QA must verify this full hash; subsequent handoff commits are records only.
- Evidence: [developer setup record](verification/environment-setup-developer.md), [validated setup commands](commands.md). No application source/tests exist.
- Environment: isolated project PG17.11 running on127.0.0.1:55432; unrelated PG13:5432 preserved; Mailpit stopped after successful capture/shutdown.
- Per-task developer-to-QA attempts: Setup0 before QA dispatch; all other tasks0. Batch completions0/10.
- Blockers: None for setup; skeleton/features remain dependency-blocked Draft.
- Push authorization/status: None; local commits only.
- Next routing: Independent QA against recorded setup implementation, then orchestrator re-check/integration if PASS.


## QA handoff — environment-setup attempt 1, 2026-10-28

- Current role/task: QA FAIL → developer fix on existing `task/environment-setup`; setup remains In progress.
- Exact verified implementation: `f31e725ed4356ee142370cf8323e36f9ea43d8d5`; reviewed at status-only tip `789b4d2c2abdea184b33b9ab42480eaa75b97013`. No implementation changes made by QA.
- Evidence: [independent QA attempt1](verification/environment-setup-qa.md). AC001–006 pass; AC007 fails because commands.md line189 still uses Homebrew stop for the project-local pg_ctl cluster. Developer fixes command consistency and adds offline-safe Mailpit version probe, then commits for fresh QA.
- Attempts: environment-setup1/3; application-skeleton and001–010 each0/3. Batch1 completions0/10.
- Services: project PG17 restarted/left running on127.0.0.1:55432; unrelated PG13PID858 unchanged on5432; QA Mailpit stopped cleanly. Secrets never printed.
- Synchronization: issue11 updated/readback during QA handoff; no issue closure, merge or push. Push authorization remains None.
- Next routing: Developer documentation correction on same branch; QA affected re-verification at new full commit, then orchestrator re-check only after PASS.

## Developer fix handoff — environment-setup, 2026-10-28

- Current role/task: Developer correction complete; In review for fresh affected QA.
- Branch / exact implementation commit: `task/environment-setup` / `1dc5e2406abd49d3cb20e2a20c4f5e191f577274`. This changes only three commands.md lines from QA attempt1 implementation; subsequent handoff commits are records only.
- Findings addressed: F001 Homebrew stop row replaced with dedicated project `pg_ctl -D .local/pgdata stop -m fast` and preservation warning; version probe now `mailpit version --no-release-check`.
- Checks: Offline-safe Mailpit probe exit0 (v1.32.0); `git diff --check` exit0; scoped diff confirms docs-only changes. QA1 AC001–006 evidence remains linked; no new runtime behavior.
- Counters: environment-setup1/3 attempts until next QA dispatch; all others0; batch completions0/10.
- Services: PG17 remains127.0.0.1:55432, unrelated PG13 preserved, Mailpit stopped.
- Issue11 synchronization: In review with exact fix hash, readback checked at handoff. No pushes/merge authorized or performed.
- Next action: QA verifies new implementation revision for F001/AC007 plus affected checks, then orchestrator re-check on PASS.


## QA handoff — environment-setup attempt 2, 2026-10-28

- Current role/task: Independent QA PASS → orchestrator requirements re-check; task remains In review.
- Exact verified implementation: `1dc5e2406abd49d3cb20e2a20c4f5e191f577274`; reviewed at records-only tip `e7808387b218a50ec281d283485868c7dfff988e`. No implementation changes by QA.
- Evidence: [independent QA attempt2 PASS](verification/environment-setup-qa-attempt-2.md); attempt1 FAIL retained. AC001–007 pass using fresh affected documentation/command checks and explicitly retained runtime evidence for unchanged files/environment.
- Attempts: environment-setup2/3; application-skeleton and001–010 each0/3. Batch1 completions0/10.
- Services: project PG17 stop/start verified and left running on127.0.0.1:55432; unrelated PG13PID858 unchanged; Mailpit stopped.
- Synchronization: issue11 QA PASS handoff updated/readback; no closure, merge or push. Push authorization None.
- Next routing: Orchestrator re-check exact implementation/evidence, record completion only if gate passes, merge/integration checks, then PM grooms dependent skeleton.
