# 001: Account registration, verification, sign-in, recovery, and safeguards

Status: Done
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/1
Local task: `_docs/tasks/001-accounts.md`
Requirement links: [REQ-001](../plan.md), [REQ-007](../plan.md), [REQ-027](../plan.md)
Dependencies: [application-skeleton](application-skeleton.md) Done/integrated at `79711b8348ff400983c5e6d265b90a476c3a6bad`; independent QA1 and orchestrator PASS at `f663bfe2149500d13516c1d82d924c3fb0a87185`; current PM readiness passed.

## Goal

Parents can access and recover verified accounts with protected credentials.

## Acceptance criteria

- [x] AC-001: REQ-001: Verified parents can sign in; unverified accounts cannot access household data; password recovery invalidates the old password; invalid/expired links deny access.
- [x] AC-002: REQ-007: Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits.
- [x] AC-003: REQ-027: Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions.
- [x] AC-004: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Household models/invitations belong to [002](002-households.md), PINs/parent unlock to [003](003-pins.md), and board data to [004](004-board.md). Establish and execute the verified-account access guard now using a synthetic protected endpoint/test fixture without adding household data or product screens. Verify actual household isolation and PIN integration in those named tasks and final release verification; this task does not claim their completion.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. Current PM readiness review passed after skeleton integration; implement from committed `develop` using the existing custom user and locked django-allauth. Keep identity-wide failure counters atomic in PostgreSQL across sessions/processes; supplementary source/request throttles must not replace the approved five-failure/five-minute identity rule. Use private access links, safe token logging, server-validated sessions, CSRF and secure cookie settings (loopback HTTP exception documented in local settings only).

## Verification plan

- AC-001: Exercise register → captured verification email → verify → sign in → sign out, resend/recovery, and password replacement in browser and PostgreSQL/request tests. Mandatory verification must deny unverified/anonymous access through the reusable guard, including direct requests. Test links just before and at one-hour expiry, malformed/tampered/used links, replay after consumption, and recovery links after a password change. A reset makes the old password unusable; duplicate registration and unknown-address recovery use generic recoverable responses. Test local SMTP failure and successful retry without false success or loss of access. Capture synthetic account email in Mailpit separately from in-memory automated tests.
- AC-002: Independent sessions/processes targeting the same account share five consecutive wrong-password attempts and a five-minute restriction. Check the fifth failure, correct password while restricted, exact expiry retry, no deadline extension from restricted attempts, and permitted success clearing failures. PostgreSQL concurrent transactions must not lose failures. Exercise supplementary source/request throttles and confirm generic errors do not disclose account existence. Shared limiter PIN use remains task 003.
- AC-003: Inspect stored credential hashing, ordinary responses, email-link handling, headers and logs without printing actual secrets/tokens. Password fields never read back; private verification/recovery tokens must be redacted from routine request logs/referrers. Test CSRF rejection on account mutations and access denial through direct requests, secure session/cookie settings, and sign-out. PIN-specific storage/exposure is task 003.
- AC-004: Execute keyboard/labeled-input/focus and recoverable validation/error flows in stable Chrome/Firefox at the agreed viewport/zoom, and retain installed-browser smoke/regression commands. Verify account persistence across sign-out/reload/server restart and that failed account actions leave consistent state. Scope household isolation tests to the account guard fixture now; actual two-household data/parent/child permissions are verified in tasks 002–004/007 and final release task 010. No unimplemented later behavior may be marked complete.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Skeleton commands and prerequisites passed independent verification/integration; account-specific commands remain UNVERIFIED until implementation. All four criteria have concrete checks and later integration ownership; PM readiness passed. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM readiness: Ready on 2026-10-28 after skeleton integration; four ACs preserved and mapped to concrete account checks and named later integration owners. Full grooming commit recorded in backlog checkpoint.

- Implementation summary: allauth verified email/password registration/sign-in/recovery, nonce-bound private link handling, atomic PostgreSQL identity/source limits, reusable verified guard, protected logs/headers, recoverable mail/DB errors and accessible account pages. Household/PIN features remain later tasks.
- Task branch / verified implementation commit: `task/001-accounts` / `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`; independent QA attempt1 PASS all fourAC.
- Changed files / revision: accounts models/migration/services/adapter/views/access/privacy; settings/URLs/templates/styles; request/browser tests and tracked stable/SMTP helpers; architecture/commands/evidence. Lock unchanged.
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: Required gates pass;32 server tests,4 browser tests; affected final failure/SMTP cases1 each pass. Stable Chrome/Firefox keyboard/native100/200% checks, actual Mailpit capture and post-restart account revisit PASS.
- Verification record: [developer account evidence](../verification/001-accounts-developer.md); [independent QA PASS](../verification/001-accounts-qa.md).
- Completion/integration record: Independent QA PASS; administrative completion/integration pending. Per-task orchestrator requirements re-check removed by user; final release review remains required.
- Remaining risks or blockers: No QA blocker; independent32server/4bundled/4additional probes and stable keyboard/nativezoom/actual Mailpit/post-restart/privacy checks PASS. Actual household/PIN integration remains subsequent tasks. QA app/mail/driver stopped; PG17 running. No pushes authorized.
