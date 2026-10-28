# Backlog

Authoritative backlog: GitHub issues in [Alex-Yu/done-together](https://github.com/Alex-Yu/done-together/issues), selected after user scope confirmation under [process.md](process.md). Local task documents mirror the mapped GitHub issues; this file is the index/checkpoint.

Backlog mode / origin repository: GitHub — `git@github.com:Alex-Yu/done-together.git`, checked 2026-10-28.
Pending issue synchronization: None after initial delivery grooming; bootstrap issues #11/#12 and existing feature issues #1–#10 updated and exact-body readback verified on 2026-10-28 (source link formatting normalized). Local commits remain unpushed.

## Task index

Delivery handed over on 2026-10-28. PM reviewed bootstrap scope and the feature roadmap against the selected architecture. Environment-setup and skeleton are Done/integrated; 001 accounts is Ready after PM review; 002–010 remain Draft pending dependency integration/current readiness review. Scope was confirmed by the user on 2026-10-28, including P-01–P-07.

| ID / labels | Task | Status | Dependencies | GitHub issue |
| --- | --- | --- | --- | --- |
| `environment-setup` | [Set up the development environment](tasks/environment-setup.md) | Done | None; PM readiness passed | [#11](https://github.com/Alex-Yu/done-together/issues/11) |
| application-skeleton | [Create a runnable application skeleton](tasks/application-skeleton.md) | Done | environment-setup Done/integrated | [#12](https://github.com/Alex-Yu/done-together/issues/12) |
| 001 | [Account registration, verification, sign-in, recovery, and safeguards](tasks/001-accounts.md) | In review | application-skeleton Done/integrated | [#1](https://github.com/Alex-Yu/done-together/issues/1) |
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

- Phase/current routing: Bootstrap Done/integrated; 001 accounts implementation In review, independent QA attempt1 next after workflow documentation handoff.
- Agreed task set: environment-setup, application-skeleton, 001–010; REQ-001–027 and confirmed defaults unchanged.
- Delivery state: develop includes setup delivery `e1d8b42d520abe8acf6bae470568ca0e0d67757e` and skeleton delivery `79711b8348ff400983c5e6d265b90a476c3a6bad`. Current branch `task/001-accounts`; exact account implementation `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`, developer records tip `8c949311770573b746983a43f24fb2c4d2d851b5`; workflow-only changes follow with no application changes.
- Current workflow (user override): retain independent per-task QA; remove the separate orchestrator per-task requirements verification. QA PASS → Done/completion records → integration checks. Failures or implementation changes route to developer and fresh affected QA. Orchestrator requirements review occurs only at final release verification alongside integrated-product QA; historical re-check evidence is preserved.
- Readiness/evidence: Setup and skeleton Done; 001 In review; 002–010 Draft. [Account developer evidence](verification/001-accounts-developer.md) is not a QA verdict. [Commands](commands.md) contains actual validation; full feature release remains incomplete.
- Attempts: setup2/3; skeleton1/3; 0010/3 before QA dispatch; 002–010 each0/3. Counts persist across sessions/batches.
- Active batch2 completions0/10, explicitly reset/renewed by user during001. Historical batch1 completed setup and skeleton (2 tasks); no workflow-doc task counted.
- Environment: project PostgreSQL17.11 loopback55432 running; unrelated PG13:5432 preserved. App/Mailpit/geckodriver stopped; synthetic data only.
- GitHub: setup11 and skeleton12 Done/closed. Issue1 In review, exact implementation/hash readback verified by developer. Draft issues2–10 completion fields synchronized/readback for the current user-requested workflow; no pending synchronization.
- Blockers: None for account QA dispatch; production decisions remain outside local delivery.
- Push authorization: None; all commits local. Issue synchronization separately authorized.
- Next action: QA verifies 001 at exact implementation (attempt1); PASS permits completion/integration directly under updated process; then PM grooms002 after successful integration.

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

## Orchestrator completion checkpoint — environment-setup

- Verified implementation: `1dc5e2406abd49d3cb20e2a20c4f5e191f577274`; QA evidence tip `156e10f6b1a8de15b2814c0b86480fe8cb05b2ef`.
- Re-check: PASS; [evidence](verification/environment-setup-orchestrator.md). All seven setup criteria met; no application requirement claimed complete.
- Current routing: commit Done records on `task/environment-setup`, integrate into `develop`, run locked sync/database integration checks, record delivery hash, reconcile/close issue #11, then PM grooms skeleton.
- Attempts: setup 2/3; all other tasks 0/3. Batch 1 completions 1/10 upon successful integration.
- Push authorization: None; local delivery only.

## Setup integration result

- Fast-forward delivery commit / task final tip: `e1d8b42d520abe8acf6bae470568ca0e0d67757e` on `develop`.
- Post-merge `uv sync --locked`, runtime imports (Django 5.2.18), authenticated PostgreSQL `SELECT 1`, and `git diff --check`: all exit 0. Clean tree before records update.
- Batch completions 1/10; setup attempts 2/3, all others 0/3. Next: PM grooms application-skeleton.
- Issue #11 Done/closed; exact body and CLOSED state readback verified. No push.

## PM Ready handoff — application-skeleton, 2026-10-28

- Current role/task: PM → developer / application-skeleton Ready. Dependency integrated at `e1d8b42d520abe8acf6bae470568ca0e0d67757e`, QA2/orchestrator PASS; integration checks passed.
- Scope/readiness: five ACs preserved; selected architecture and validated environment confirmed. Explicit test-DB guard, safe settings, custom user before migrations, local pinned HTMX provenance/license, full skeleton checks and stable Chrome/Firefox keyboard/200% observations remain required. No account workflow.
- Issue #12 Ready/open reconciled/readback verified; no pending sync. Grooming branch `develop`; full grooming commit `87b54c097f99613a23972b6b08efc194f1088f91`. Subsequent checkpoint-only commit records this hash without changing scope.
- Counters: batch1 completions1/10; setup2/3 attempts; skeleton/001–010 each0/3. No push authorization.
- Next: developer creates task/application-skeleton from committed grooming, implements, then exact commit to independent QA.

## Developer handoff — application-skeleton, 2026-10-28

- Current role/task: Skeleton implementation complete, In review; route independent QA.
- Branch: `task/application-skeleton`, from PM tip e1e23a8a05dad5075cd997298f7e2e76a9c51add including grooming87b54c097f99613a23972b6b08efc194f1088f91.
- Exact implementation commit: `f663bfe2149500d13516c1d82d924c3fb0a87185`; later handoff records do not change code.
- Evidence: [developer record](verification/application-skeleton-developer.md), [validated commands](commands.md), tracked installed-browser helper.
- Checks: migrations/system/drift/lint/format/static/locked sync pass; targeted health4/server11/bundled browsers2 pass; installed Chrome156/Firefox159 native100/200% keyboard/focus/HTMX screenshots inspected.
- Services: PG17 running127.0.0.1:55432; existing PG13:5432 preserved. Webserver/geckodriver stopped after verification.
- Counters before QA dispatch: Setup2/3, skeleton0/3, features001–010 zero. Batch1/10 complete.
- Blockers: None for skeleton; feature001 awaits skeleton QA/re-check/integration/PM readiness.
- Issue12 In review synchronized/readback at handoff. No merge/push; no push authorization.
- Next routing: QA every skeletonAC on exact implementation, then orchestrator re-check/integration if PASS.


## QA handoff — application-skeleton attempt 1, 2026-10-28

- Current role/task: Independent QA PASS → orchestrator requirements re-check; skeleton remains In review.
- Exact verified implementation: `f663bfe2149500d13516c1d82d924c3fb0a87185`; reviewed records-only tip `da17dd05d5f1187b591203c69f1ab02b3aa1a95b`.
- Evidence: [skeleton independent QA PASS](verification/application-skeleton-qa.md). All five AC pass: locked config/custom user/testDB isolation; real DB health success/failure; local HTMX/CSRF; lint/checks/health4/server11/bundled2; independent installed stable Chrome156/Firefox159 native100/200% keyboard/focus/screenshots; clean server/driver stop.
- Attempts: setup2/3; skeleton1/3;001–010 each0/3. Batch1 completions1/10.
- Services: PG17 remains running127.0.0.1:55432; QA loopback webserver/geckodriver stopped exit0 and endpoints refused. No private values logged.
- Synchronization: issue12 QA PASS handoff updated/readback; no closure, merge or push. Push authorization None.
- Next routing: Orchestrator re-check same implementation/evidence; if gate passes, complete/merge/integration-check skeleton, then PM grooms001 accounts.

## Orchestrator skeleton completion checkpoint

- QA attempt1 PASS and orchestrator PASS at implementation `f663bfe2149500d13516c1d82d924c3fb0a87185`; reviewed records tip `00d85a9c8657758201beb65d030ec21140027422`.
- Evidence: [QA](verification/application-skeleton-qa.md), [requirements re-check](verification/application-skeleton-orchestrator.md).
- Next: commit Done records, integrate task/application-skeleton into develop, run integration server/check/drift/lint commands, record delivery hash and close issue12 after readback.
- Attempts setup2/3, skeleton1/3, others0/3. Batch completions2/10 after successful integration. No push.

## Skeleton integration result

- Final task tip/fast-forward delivery `79711b8348ff400983c5e6d265b90a476c3a6bad` on develop.
- Post-merge Django checks/drift, server/config11 tests, Ruff lint/format, git diff check PASS. No implementation change during integration.
- Attempts skeleton1/3, setup2/3; batch2/10. Issue12 Done/closed, exact body and state readback verified; no push.

## PM Ready handoff — 001 accounts, 2026-10-28

- Current role/task: PM → developer / 001 Ready. Skeleton integrated at `79711b8348ff400983c5e6d265b90a476c3a6bad`; QA1/orchestrator PASS implementation `f663bfe2149500d13516c1d82d924c3fb0a87185`, postmerge checks passed.
- Scope/readiness: four ACs preserved; django-allauth/custom user, mandatory verification, one-hour safe links, recovery invalidation, atomic PostgreSQL five-failure/five-minute identity lockouts, supplementary source/request throttles, CSRF/session privacy, accessible recoverable errors and SMTP retry verified by specified backend/browser checks. No material question.
- Sequencing: establish reusable verified-account access guard with synthetic protected endpoint fixture now; actual household data isolation 002/004 and PIN/parent authority 003/007 remain named later requirements, never claimed complete here.
- Authoritative issue1 Ready/open reconciled and body readback verified; no pending synchronization. Grooming branch `develop`; full grooming commit `0be3570381f86976bd0fbdfe214d4cfa06025c75`. Subsequent checkpoint-only commit records this hash without changing task scope.
- Counters: batch1 completions2/10; setup2/3, skeleton1/3, 001–010 each0/3. No push authorization.
- Next: developer creates task/001-accounts from committed grooming, implements account scope, commits exact implementation, hands to independent QA (attempt1).

## User limit reset — 2026-10-28

- User explicitly reset limits and requested goal continuation during task001 implementation. Start batch2 with default ten completions, now0/10; remaining001–010 fit this batch. Batch1 ended with setup and skeleton Done (2 completions).
- Preserve task attempt history: setup2/3, skeleton1/3, accounts0/3 before QA dispatch; all later tasks0/3.
- Current role/task: developer implementing001 on task/001-accounts from PM checkpoint c7a085d3d1604951e49c1b9847ecb4d5dc94693e; uncommitted source/tests are incomplete until exact implementation handoff.
- Last developer results: account integration20 and bundled browser4 passed; installed Chrome/Firefox native100/200 account checks and actual Mailpit account lifecycle passed. Final regression, persistence and commit/handoff pending; no QA verdict for001 yet.
- Next routing: developer finishes and commits, independent QA attempt1, orchestrator requirements re-check and integration, then PM002. No pushes authorized.

## Developer handoff —001 accounts, 2026-10-28

- Current role/task: Account implementation complete/In review; route independent QA. User removed separate per-task orchestrator requirements re-check; QA PASS proceeds to completion/integration, final release review retained.
- Branch: `task/001-accounts`, from PM checkpoint c7a085d3d1604951e49c1b9847ecb4d5dc94693e including grooming0be3570381f86976bd0fbdfe214d4cfa06025c75.
- Exact implementation commit: `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`; later handoff/workflow-only commits contain no source changes.
- Evidence: [developer account record](verification/001-accounts-developer.md), [validated commands](commands.md), tracked stable-browser and real-SMTP helpers.
- Results:32 server/config tests and4 browser tests passed; final narrow DB-failure/unsent-SMTP-link cases1 each passed; migrate/check/drift/lint/format/static/locked sync pass. Native stable Chrome156/Firefox159 keyboard100/200% account checks, actual Mailpit verification/recovery capture, and stored synthetic account post-webserver-restart revisit PASS.
- Services: ProjectPG17 remains127.0.0.1:55432; unrelatedPG13:5432 preserved. App/Mailpit/geckodriver cleanly stopped (exit0; endpoints refuse).
- Privacy correction: private link GET exchanges into nonce-bound server session; token-free native forms retain CSRF and same-origin referrer policy, original private redirects no-referrer; all no-store. Local-only DB credential rotated after verbose failing fixture trace; ignored.env/pgpass parity and SELECT1 verified, no value in source/evidence.
- Active batch2:0/10 completions, explicitly renewed by user during001. Historical batch1 completed setup/skeleton2 tasks. Attempts:setup2/3,skeleton1/3,0010/3 before QA dispatch;002–010 all0/3.
- Issue1 In review exact-body/hash readback verified at handoff; no pushes authorized or performed.
- Next: PM commits/synchronizes user-requested workflow documents on this branch; independent QA001 attempt1 at exact implementation, then completion/integration on PASS. Actual household/PIN rights remain later tasks.

## User workflow change — 2026-10-28

- User requested removal of orchestrator verification for each task, keeping release verification. Independent per-task QA retained; only the extra orchestrator requirements gate is removed. Completion records, integration checks, failure/fix/fresh-QA routing and final release QA remain required. Orchestrator requirements review is final-release-only.
- Updated AGENTS, README graph/prose, process, orchestrator role, reusable prompt, task template and unstarted002–010 completion handoff fields. Historic setup/skeleton verification records and account implementation are unchanged.
- Checks: git diff --check passed; local Markdown targets in15 changed workflow/task documents resolve; current-instruction assertions confirm no obsolete extra per-task gate. GitHub Draft issue2–10 mirror fields updated and exact readback verified.
- Workflow-only commit: `c4c4233d9cc670ae68d06f03efc77d0dad707cf0` on `task/001-accounts`; no application code changes, no feature completion/attempt increment, no push. Subsequent checkpoint-only commit records this hash.


## QA handoff —001 accounts attempt1,2026-10-28

- Current role/task: Independent QA PASS → administrative completion/integration;001 remains In review. User removed per-task orchestrator requirements re-check; final release review still required.
- Exact verified implementation: `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`; reviewed at records/workflow-only tip `b5eb43ea7abe2d1c6539085023840b4565878a9c`; no implementation changes by QA.
- Evidence: [001 independent QA PASS](verification/001-accounts-qa.md). All fourAC pass;32server/4bundled/4additional concurrency-session probes; stable Chrome156/Firefox159 keyboard/native100/200%; actual Mailpit signup/verify/recovery and post-restart persistence; actual log privacy assertions.
- Counters: renewed batch2 completions0/10 before001 integration;001 attempt1/3; setup2/3/skeleton1/3 preserved;002–010 each0/3.
- Services: only dedicated PG17 remains running55432; unrelated PG13PID858 preserved5432. QA app/Mailpit/geckodriver stopped cleanly, their four ports closed. Private values never printed.
- Synchronization: issue1 QA PASS handoff updated/readback; no closure/merge/push. No push authorization.
- Next routing: administratively markDone/commit completion after QA PASS, integrate/check exact delivery state, close issue1 only after successful integration; PM grooms002.

## Accounts completion — current routing

- Independent QA1 PASS all four criteria at implementation `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`; evidence/status tip `8a346c1756c3268c8639021042419cf17373e61b`. See [QA evidence](verification/001-accounts-qa.md).
- Administrative Done/integration follows QA PASS; no per-task orchestrator verification under user workflow override.
- Next: commit completion, fast-forward task/001-accounts to develop, run required integration gates, record delivery and synchronize/close issue1.
- Batch2 completion1/10 on successful integration; accounts1/3 QA attempts, setup2/skeleton1 retained, later tasks0. No push.
