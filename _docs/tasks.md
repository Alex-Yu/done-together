# Backlog

Authoritative backlog: GitHub issues in [Alex-Yu/done-together](https://github.com/Alex-Yu/done-together/issues), selected after user scope confirmation under [process.md](process.md). Local task documents mirror the mapped GitHub issues; this file is the index/checkpoint.

Backlog mode / origin repository: GitHub — `git@github.com:Alex-Yu/done-together.git`, checked 2026-10-28.
Pending issue synchronization: None after initial delivery grooming; bootstrap issues #11/#12 and existing feature issues #1–#10 updated and exact-body readback verified on 2026-10-28 (source link formatting normalized). Local commits remain unpushed.

## Task index

Delivery handed over on 2026-10-28. PM reviewed bootstrap scope and the feature roadmap against the selected architecture. Environment setup, skeleton,001 accounts,002 households and003 PIN/shared access are Done/integrated;004–010 remain Draft pending current readiness/dependency review. Scope was confirmed by the user on 2026-10-28, including P-01–P-07.

| ID / labels | Task | Status | Dependencies | GitHub issue |
| --- | --- | --- | --- | --- |
| `environment-setup` | [Set up the development environment](tasks/environment-setup.md) | Done | None; PM readiness passed | [#11](https://github.com/Alex-Yu/done-together/issues/11) |
| application-skeleton | [Create a runnable application skeleton](tasks/application-skeleton.md) | Done | environment-setup Done/integrated | [#12](https://github.com/Alex-Yu/done-together/issues/12) |
| 001 | [Account registration, verification, sign-in, recovery, and safeguards](tasks/001-accounts.md) | Done | application-skeleton Done/integrated | [#1](https://github.com/Alex-Yu/done-together/issues/1) |
| 002 | [Household creation, timezone setup, and second-parent invitation](tasks/002-households.md) | Done | 001 Done/integrated | [#2](https://github.com/Alex-Yu/done-together/issues/2) |
| 003 | [Child profiles, parent/child PIN management, and protected shared access](tasks/003-pins.md) | Done | 002 Done/integrated | [#3](https://github.com/Alex-Yu/done-together/issues/3) |
| 004 | [Shared board, empty states, and settings navigation](tasks/004-board.md) | Ready | 003 Done/integrated | [#4](https://github.com/Alex-Yu/done-together/issues/4) |
| 005 | [One-off chore assignment and maintenance](tasks/005-one-off-chores.md) | Draft | 004 | [#5](https://github.com/Alex-Yu/done-together/issues/5) |
| 006 | [Recurrence, occurrence generation, future edits, and deletion](tasks/006-recurrence.md) | Draft | 005 | [#6](https://github.com/Alex-Yu/done-together/issues/6) |
| 007 | [Child submission, parent review, returns, and overdue rules](tasks/007-review.md) | Draft | 006 | [#7](https://github.com/Alex-Yu/done-together/issues/7) |
| 008 | [Weekly/all-time stars and completion visibility](tasks/008-stars.md) | Draft | 007 | [#8](https://github.com/Alex-Yu/done-together/issues/8) |
| 009 | [Synchronization, concurrent-action handling, and offline recovery](tasks/009-synchronization.md) | Draft | 008 | [#9](https://github.com/Alex-Yu/done-together/issues/9) |
| 010 | [Integrated release verification and browser/accessibility checks](tasks/010-release-verification.md) | Draft | 009 | [#10](https://github.com/Alex-Yu/done-together/issues/10) |

Bootstrap criteria preserve environment-before-skeleton separation. PM reconciled all feature tasks to the selected architecture, retained stable acceptance IDs, and made later integration ownership explicit where features depend on later workflows. No requirement is claimed complete by grooming.

## Checkpoint — 2026-10-29

- Phase/current routing: Environment, skeleton,001 accounts,002 households and003 PIN/shared access Done/integrated; 004 board Ready; developer handoff next.
- Agreed scope: bootstrap plus001–010; REQ-001–027 and confirmed defaults unchanged. Full release incomplete.
- Delivery: develop at `8218a22e1b015e89be45aad814f5188150fafe4b`, task003 final tip/fast-forward delivery. Verified implementation `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`; independent QA1 PASS all six criteria. No implementation change during merge.
- Integration: migrate/check/drift,73 server/config tests, Ruff lint/format and diff check PASS. [PIN QA evidence](verification/003-pins-qa.md) includes8bundled,15adversarial,2failure/privacy probes, stable native100/200/real61s idle and restart checks.
- Preparation:004 Ready after current PM review;005–010 Draft grooming and QA plans integrated, dependencies still gate readiness.
- Workflow override: independent per-task QA→completion/integration; no per-task orchestrator verification. Final release requires integrated QA and orchestrator requirements review.
- Attempts: setup2/3;skeleton1/3;0011/3;0022/3;0031/3;004–010 each0/3. Preserve histories.
- Active batch2 completions3/10 after user reset; historical batch1 bootstrap2. Remaining004–010 fit renewed batch.
- Environment: PG17.11 loopback55432 retained; unrelated PG13:5432 preserved; app/Mailpit/geckodriver stopped. Synthetic data only.
- GitHub:11/12/1/2 closed; issue3 Done/closed; exact body and state readback verified;issue4 Ready/open exactbody readback verified;005–010 Draft/open.
- Blockers: None for004 implementation. No pushes authorized. Next: developer task/004-board from committed develop grooming→implementation→independent QA attempt1; no pending issue synchronization.

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

## Accounts integration result

- Delivery/final task tip `3afacd6e58d61f727f5aa2760a7ab0bbff445043` on develop; all required integration checks PASS (32 server/config tests), no code delta from QA-verified implementation.
- Batch2 1/10,001 attempts1/3; bootstrap histories retained. Issue1 Done/closed, exact body and state readback verified; PM002 next. No push.

## PM Ready handoff —002 households, 2026-10-28

- Dependency:001 integrated at `3afacd6e58d61f727f5aa2760a7ab0bbff445043`, independent QA1 PASS at `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`; postmerge checks passed.
- Five ACs retained: verified account creation/join, recipient-bound seven-day single-use invitations, atomic P-01 membership limits, equal rights/actual two-household isolation, immutable browser-suggested timezone, recoverable SMTP and private/accessible persistent workflows.
- Staged authority: verified account/membership protects available household workflows now;003 integrates PIN protection into existing management/settings. Bootstrap creation/join stays account-authorized; no later PIN/child/chore requirement claimed complete.
- Issue2 Ready/open synchronized and exactbody readback verified; grooming branch `develop`, full grooming commit `44aff04469c91a50f16fbf89a129d963d662ad04`; subsequent checkpoint-only commit records this hash.
- Counters: active batch2 completions1/10; setup2/3,skeleton1/3,0011/3,002–010 each0/3. No push authorization; workflow-only grooming does not count as completion.
- Next: Developer task/002-households from committed grooming, implementation→independent QA attempt1→completion/integration on PASS; no per-task orchestrator verification.

## Developer handoff —002 households, 2026-10-28

- Current role/task: Household implementation complete/In review; independent QA next. QA PASS proceeds to completion/integration; separate orchestrator per-task re-check remains removed by user, final release review retained.
- Branch: `task/002-households` from24b5ca3df6d882a85a38ff42bccb1731a6fb2805 including PM grooming44aff04469c91a50f16fbf89a129d963d662ad04.
- Exact implementation commit: `1b01711d3fd9962825e38ba87297a22c976d0a09`; later handoff records contain no source changes.
- Results/evidence: [developer household record](verification/002-households-developer.md), [commands](commands.md). Household17/server49/browser6 passed; final affected wrong-recipient recovery1 passed/16 deselected. Standard gates pass; native stable100/200 realSMTP/create/invite/join/error checks and post-app-restart stored-state revisit all PASS.
- Services: App/Mailpit/geckodriver stopped exit0/endpoints refuse; projectPG17 running127.0.0.1:55432; unrelatedPG13 preserved. Private synthetic fixtures/screenshots ignored.
- Preparation already integrated separately onto develop96e7018af88d67b24d0ff63b924f8ebec4f1e906: PM8feda09 future Draft grooming and QA29bdf2e plans. Root task002 remains based on24b5ca3; do not rebase/merge before exact-code QA. Normal non-fast-forward task integration may be needed.
- Counters: Active batch2 completions1/10 (001 Done); historical setup2/3,skeleton1/3,0011/3;0020/3 before QA dispatch;003–010 all0/3.
- Issue2 In review/exact body/hash readback verified. Initial combined command was rejected by automatic approval review over destination/payload authorization; local records were completed first, read-only origin/repo/issue checks and private-value scans confirmed the authorized task-only payload, then a single direct exact issue edit succeeded with review. No pending synchronization. No source push authorization; no pushes/merge performed by developer.
- Next: QA002 at exact implementation, then completion/integration on PASS, PM fresh003 readiness. Parent PIN/child/board/scheduling remain subsequent tasks.


## QA in progress —002 households attempt1,2026-10-28

- Current role/task: Independent QA002 running; task In review, no verdict yet.
- Exact implementation: `1b01711d3fd9962825e38ba87297a22c976d0a09`; reviewed records-only tip `114b8f23086fd9784f296bcf0aa06cac3e34f66c`.
- Counters:002 attempt1/3 dispatched; active renewed batch2 completions1/10; setup2/3/skeleton1/3/accounts1/3 retained;003–010 each0/3. Per-task orchestrator re-check removed by user; final release review remains.
- Progress: locked sync/lint/format/migrate/system/drift/static and49server tests passed; bundled browser regression running. No completion verdict; remaining privacy/failure, installed-browser/SMTP/persistence checks pending.
- Next: complete all fiveAC independently, record exact observations/verdict, synchronize issue2 and evidence-only commit. Technical findings route developer for fixes, never alter implementation during QA.


## QA handoff —002 households attempt1,2026-10-28

- Current role/task: Independent QA FAIL → developer fix;002 In progress on existing task/002-households.
- Exact verified implementation: `1b01711d3fd9962825e38ba87297a22c976d0a09`; records-only reviewed tip `114b8f23086fd9784f296bcf0aa06cac3e34f66c`; no app fixes by QA.
- Evidence: [002 QA attempt1](verification/002-households-qa.md). F001 AC004/005 FAIL: household DB errors after initial source limiter bypass account-only exception recovery and expose synthetic private detail in technical500/logs under local DEBUG. AC001–003 PASS;49server/6bundled and installed stable native100/200% actualSMTP/join/error/screenshots plus restart persistence pass. Independent narrow probe1FAIL.
- Counters:0021/3; active renewed batch2 completions1/10; setup2/3/skeleton1/3/accounts1/3 retained;003–010 each0/3. User final-only orchestrator requirements review override remains.
- Services: QA app/driver/Mailpit stopped exit0 and fourports closed; projectPG17 remains55432, unrelatedPG13 preserved.
- Synchronization: issue2 In progress/findings/evidence updated and exact readback; no closure/merge/push. No push authorization.
- Next: developer generic household DB-error/privacy correction and regression on same branch, new implementation commit then QA attempt2. Preserve prior positive evidence for unchanged code where valid.

## Developer correction handoff —002 F001,2026-10-28

- Current role/task: F001 source correction complete/In review; fresh affected QA next on same task/002-households.
- Exact fix implementation commit: `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`. One-line middleware recovery-prefix extension plus four regression cases; prior normal-path implementation unchanged.
- Evidence: [F001 developer correction](verification/002-households-fix-developer.md), original [QA attempt1 FAIL](verification/002-households-qa.md). Affected4 and original independent QA probe1 pass; fresh server53 plus checks/drift/lint/format/diff pass. Prior6-browser/native100/200/SMTP/restart positive evidence retained, no unchanged reruns.
- Counters unchanged until QA dispatch:0021/3; batch2 completions1/10; setup2/skeleton1/accounts1 historical attempts,003–010 zero. Final-only orchestrator requirements review remains.
- No owned app/mail/driver service started; projectPG17 remains55432 and unrelatedPG13 preserved.
- Develop remains docs-preparation divergence96e7018af88d67b24d0ff63b924f8ebec4f1e906; no merge/rebase/push.
- Issue2 In review/exact fix-hash/task body synchronized and readback verified; no pending synchronization.
- Next: QA2 on exact fix; completion/integration on PASS then PM003 readiness.


## QA in progress —002 households attempt2,2026-10-28

- Current role/task: Independent QA002 fix verification; task In review, no fresh verdict yet.
- Exact fix implementation: `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`; reviewed records-only tip `49cd31869dc82b85b5361302caa92a2c79d86ee4`.
- Counters:002 attempt2/3 dispatched; active renewed batch2 completions1/10; setup2/3/skeleton1/3/accounts1/3 retained;003–010 each0/3. User final-only orchestrator requirements review remains.
- Next: inspect exact delta, independently repeat original F001/four affected failure paths/privacy/rollback/retry; retain unaffected prior runtime evidence explicitly; commit fresh evidence/status and direct issue2 readback.


## QA handoff —002 households attempt2,2026-10-28

- Current role/task: Independent QA PASS → administrative completion/integration;002 remains In review. Final-only orchestrator requirements review override preserved.
- Exact verified implementation: `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`; reviewed records-only tip `49cd31869dc82b85b5361302caa92a2c79d86ee4`.
- Evidence: [002 QA attempt2 PASS](verification/002-households-qa-attempt-2.md); attempt1 FAIL retained. F001 resolved: affected4/originalQAprobe1/fullserver53/checks/drift/lint/format pass, generic503/private response+log protection/rollback+retry verified. Exact delta supports retained unchanged normal browser/native/SMTP/restart evidence.
- Counters:0022/3; active renewed batch2 completions1/10 before integration; setup2/3/skeleton1/3/accounts1/3 retained;003–0100/3.
- Services: no new owned services for scoped fix; dedicatedPG17 remains55432. No secret values printed.
- Synchronization: issue2 PASS handoff updated/readback; no closure/merge/push. No push authorization.
- Next: administratively complete002, integrate with docs-only develop divergence and run applicable integration gates; then PM current readiness for003.

## Household completion — current routing

- Independent QA attempt2 PASS at implementation `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`; evidence/status tip `53d4e47f5e998e6b2e36d6837f50538fbacb5daf`. [Evidence](verification/002-households-qa-attempt-2.md); attempt1 FAIL retained, F001 resolved.
- Administrative Done/integration follows QA PASS. Develop already includes docs-only PM/QA preparation at `96e7018af88d67b24d0ff63b924f8ebec4f1e906`; merge preserves both histories without changing implementation.
- Next: integration checks, delivery hash and issue2 completion synchronization, then PM marks003 Ready after dependency integration.
- Active batch2 completion2/10 on successful integration;002 attempts2/3,0011/3,setup2/skeleton1,003–010 each0. No push.

## Household integration result

- Delivery `f98ba7ba2a46b875bb3a2c0c643d8a3bbe5a1cad`, task tip `39297ba6903bfe1c7e96c9b85fb8d7dd8892f877`. Normal merge with parallel future-task grooming/QA plans; diff from task branch contains only those preparation documents, no implementation change.
- Post-merge migrate/check/drift,53 server/config tests, Ruff lint/format and diff check PASS. Batch2 2/10,002 attempts2/3; issue2 Done/closed, exact body and state readback verified. PM003 next; no push.

## PM Ready handoff —003 PIN/shared access, 2026-10-28

- Dependency002 Done/integrated `f98ba7ba2a46b875bb3a2c0c643d8a3bbe5a1cad`, QA2 PASS `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`; postmerge53 server/check/migrate/drift/Ruff PASS.
- Six ACs unchanged; parallel grooming8feda09 and QA plan29bdf2e integrated, current readiness complete. Selected parent's own password for first/reset PIN; exact four digits/leading zeros; either-parent unlock; PostgreSQL shared identity5/5; server60-second parent-only activity and protected existing002 management. Verified-account creation/join and own-password recovery remain bootstrap paths. Full board004/submission007 remain later owners.
- Issue3 Ready/open body readback verified. Grooming on develop; full readiness commit `0eb69675a07941132674a4e549bbf81e4da1e6c7`; following checkpoint-only commit records this hash. No implementation/QA claim from readiness.
- Counters unchanged: batch2 completions2/10; setup2/3,skeleton1/3,0011/3,0022/3,003–010 each0/3. No pushes.
- Next: developer branch task/003-pins includes readiness commit; exact implementation to independent QA attempt1, then completion/integration on PASS.

## Developer started003 —2026-10-28

- Current role/task:003 In progress on task/003-pins from Ready grooming0eb69675a07941132674a4e549bbf81e4da1e6c7/checkpointdb1096aa86bef0fcb517f93ca447785a7d237aba.
- Scope: Salted/peppered PINs, selected-parent password recovery, scoped child management, DB board-session authority with60sec accepted-parent-only activity; existing002 settings/invites become PIN guarded, create/join remain verified bootstrap.
- Active batch2 completions2/10;003 attempts0/3 before QA. Source incomplete/uncommitted; no QA verdict or push.

## Continuation checkpoint —2026-10-29

- Actual root state inspected: task/003-pins at readiness checkpoint `db1096aa86bef0fcb517f93ca447785a7d237aba` with uncommitted PIN source/tests; no implementation commit or task003 QA handoff yet.
- Developer usage-limit interruption routed back to same developer with completed evidence preserved; final local credential checks/persistence/shutdown/records pending. No completion or failed QA attempt inferred from interruption.
- Corrected stale task-index rows:001/002 Done,003 In progress. Active batch2 remains2/10;003 attempts0/3, previous histories retained.

## Developer handoff —003 PINs,2026-10-29

- Current role/task:003 implementation complete/In review; exact-code independent QA next. No per-task orchestrator re-check; final release review retained.
- Branch:task/003-pins fromdb1096aa86bef0fcb517f93ca447785a7d237aba including Ready grooming0eb69675a07941132674a4e549bbf81e4da1e6c7. Exact implementation hash:`d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`.
- Evidence:[developer PIN record](verification/003-pins-developer.md), [commands](commands.md). PIN19/full backend72/household21/browser8 PASS; final exact-password/pepper1 PASS. Standard gates pass; installed native100/200 and both actual61sec idle locks/visible child board PASS; stored state restart revisit PASS.
- Scope: Child add/read/name-or-PIN update, no deletion. Actual submission007 and full columns004 remain later. Existing002 management now guarded; bootstrap create/join/own password recovery preserved.
- Services: owned app/Mailpit/geckodriver stopped exit0/endpoints refuse; dedicatedPG17 running55432, unrelatedPG13 preserved. Private fixture artifacts ignored.
- Counters: batch2 completions2/10;0030/3 before QA dispatch; historical setup2/skeleton1/0011/0022;004–010 zero.
- Issue3 In review/exact implementation hash/task body synchronized and readback verified; no pending synchronization. No merge/rebase/push.
- Next: independent QA003 at exact commit, then completion/integration on PASS and PM004 fresh readiness.


## QA in progress —003 PINs attempt1,2026-10-29

- Current role/task: Independent QA003 running; task In review, no verdict yet.
- Exact implementation: `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`; reviewed records-only tip `c3bd384206e33347509d369cbda563873a59f74f`.
- Counters:003 attempt1/3 dispatched; active renewed batch2 completions2/10; setup2/skeleton1/accounts1/households2 histories retained;004–010 each0/3. Final-only orchestrator requirements review remains.
- Next: exact-commit sixAC verification including independent adversarial authority/reset/time-boundary probes, required sequential PostgreSQL/browser/native checks and privacy; record all findings and direct issue3 readback, evidence-only commit.


## QA handoff —003 PINs attempt1,2026-10-29

- Current role/task: Independent QA PASS → administrative completion/integration;003 remains In review. Final-only orchestrator requirements review preserved.
- Exact verified implementation: `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`; reviewed records-only tip `c3bd384206e33347509d369cbda563873a59f74f`.
- Evidence: [003 independent QA PASS](verification/003-pins-qa.md). All sixAC pass;73backend/8bundled/15independent adversarial/2source-DBfailure probes; stableChrome156/Firefox159 native100/200, both actual61s idle locks with visible childboard, six fresh screenshots and allfour postrestart revisits.
- Counters:0031/3; active renewed batch2 completions2/10 before integration; setup2/skeleton1/accounts1/households2 histories retained;004–0100/3.
- Services: QA app/driver/Mailpit stopped exit0 and temporary fourportsclosed; PG17 running55432, PG13 preserved. No private values printed.
- Synchronization: issue3 PASS handoff updated/exact readback; no closure/merge/push. No push authorization.
- Next: administratively complete/integrate/check003, then PM readiness for004; real child submission007/full board004 remain later owners.

## PIN completion —2026-10-29

- Independent QA attempt1 PASS all six criteria at implementation `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`; evidence/status tip `2457faf3664a65459cce664ae6fc39690a210360`. [QA evidence](verification/003-pins-qa.md).
- Administrative completion/integration follows QA PASS; no separate per-task orchestrator verification. Next merge, required integration checks, delivery hash and issue3 synchronization/closure; PM004 readiness after integration.
- Active batch2 completion3/10 after successful integration;003 attempts1/3; setup2/skeleton1/accounts1/households2 retained,004–010 each0. No push.

## PIN integration result —2026-10-29

- Task final tip/fast-forward delivery `8218a22e1b015e89be45aad814f5188150fafe4b`; no code changes during integration.
- Post-merge migrate/check/drift,73server tests,Ruff lint/format,diff check PASS. Active batch2 3/10;003 attempt1/3. Issue3 Done/closed, exact body and state readback verified; PM004 next. No push.

## PM Ready handoff —004 board, 2026-10-29

- Dependency003 Done/integrated `8218a22e1b015e89be45aad814f5188150fafe4b`, QA1 PASS `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`; postmerge73 backend/check/migrate/drift/Ruff PASS.
- Five ACs unchanged; integrated Draft grooming/QA matrix reviewed. Real child columns/empty states/protected navigation now; synthetic internal mixed-state fixtures only for005–008 pending workflows. Preserve003 timeout and read-only board visibility; no production fake chores/totals or dashboard.
- Issue4 Ready/open exactbody readback verified. Grooming on develop; full readiness commit `6ccc548e5c63a6139a8994f4bae9a4a8dc2b6bbd`; following checkpoint-only commit records this hash. No implementation/QA claim from readiness.
- Counters unchanged: batch2 completions3/10; setup2/3,skeleton1/3,0011/3,0022/3,0031/3,004–010 each0/3. No pushes.
- Next: developer task/004-board includes readiness commit; exact implementation to independent QA attempt1→completion/integration on PASS.
