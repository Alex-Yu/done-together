# 003: Child profiles, parent/child PIN management, and protected shared access

Status: In review
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/3
Local task: `_docs/tasks/003-pins.md`
Requirement links: [REQ-004](../plan.md), [REQ-005](../plan.md), [REQ-006](../plan.md), [REQ-007](../plan.md), [REQ-027](../plan.md)
Dependencies: [002](002-households.md) Done/integrated at `f98ba7ba2a46b875bb3a2c0c643d8a3bbe5a1cad`; independent QA2 PASS implementation `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`; current PM readiness passed.

## Goal

Children have submission identities and either parent can securely unlock management.

## Acceptance criteria

- [ ] AC-001: REQ-004: Protected settings add children/reset child PINs; own password authorizes own parent PIN reset; replaced PINs fail. Four-digit PINs preserve leading zeroes.
- [ ] AC-002: REQ-005: Either valid parent PIN unlocks management; child/incorrect PINs and locked requests cannot perform parent actions.
- [ ] AC-003: REQ-006: After 60 seconds, management requires a PIN again. Board viewing and child activity do not extend parent access.
- [ ] AC-004: REQ-007: Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits.
- [ ] AC-005: REQ-027: Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions.
- [ ] AC-006: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

First/own parent PIN setup/reset verifies the selected member’s own account password and remains reachable when locked. Existing household management/invitations from002 acquire parent-unlock protection here; verified-account initial household creation/join remain bootstrap actions. Child submission authority is integrated in007; full board columns in004.

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. Dependency002 and parallel grooming8feda09b8b827736f832fd8dff6a48ece0e7075d are integrated onto `develop`; current PM review confirms all six criteria, exclusions, constraints and verification plan complete. This task is Ready. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

Use the integrated [QA preparation matrix](../verification/plans/003-006-identity-board-assignment.md) alongside the six-criterion plan below. Preparation is not a QA verdict; independent QA verifies the exact implementation after handoff.

- AC-001: Browser and direct-request tests add/edit a child's display name and set/reset child PIN in protected settings. Use exact strings `0007`/`0123`, reject non-four-digit/non-ASCII-digit/blank input without partial data, and prove replaced PINs fail using the credential verifier. Selected member's own account password authorizes first/own parent PIN setup/reset; wrong password, another parent's password and outsider identity fail. Verify password lockout safeguards on this path. No PIN can be read back.
- AC-002: The board-opening account may differ from selected unlocking parent; either member's valid PIN grants equal authority for that board session only. Apply the server-side parent guard to existing task002 household management/invitation settings as well as children/PIN settings. Anonymous/unverified/outsider/child/incorrect PIN and locked direct requests cannot manage. Verified-account initial household creation/join remain bootstrap actions; password-authorized own PIN setup/reset must stay reachable when locked. Test separate browser sessions and forged parent/child/household IDs; no Django admin bypass.
- AC-003: Test just before and at60 seconds using deterministic server instants and a real-browser idle check. Every protected request enforces expiry; accepted explicit parent activity extends it, failed activity/viewing/polling/child activity does not. Visible read-only household board surface stays present on lock (full columns arrive004). Client timer gives matching feedback, while direct requests after expiry still deny. Actual child-submission interaction is integrated in007; use a non-authorizing child credential-check fixture now, never a child session granting management.
- AC-004: Reuse atomic PostgreSQL identity limiter and supplementary request throttles. Across independent sessions/transactions, five consecutive failures for each parent/child PIN identity trigger exactly five minutes; correct PIN while blocked denies, blocked attempts do not extend deadline, permitted success clears failures. PIN checks require household board access. Test concurrent failures and expiry retry; actual submission endpoint inherits this in007.
- AC-005/006: Inspect salted maintained hashes plus outside-database pepper use, no plaintext/hash/PIN in ordinary responses/logs, no-store sensitive pages and CSRF-protected mutations. Test actual two-household isolation, persistent settings after sign-out/restart and no false success on DB/request failure. Stable Chrome/Firefox at1280×720 and200% zoom cover keyboard/focus/labeled inputs, lock/unlock, child/PIN management and recoverable errors.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Dependency/grooming integration and current PM readiness are complete. Existing task002 settings/invitation management must now require selected-parent unlock; verified-account create/join and password-authorized own-PIN recovery remain reachable while locked. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM readiness: Ready on 2026-10-28 after002 and parallel grooming integration; six ACs unchanged, no consequential question. Full readiness grooming commit recorded in backlog checkpoint.

- Implementation summary: Salted/peppered exact PIN credentials, selected-own-password setup/reset, scoped child add/name/PIN updates, session-bound DB parent authority/60sec activity guard, version/active-parent revocation and explicit-only client timer/activity. Existing002 management protected; verified bootstrap retained.
- Task branch / verified implementation commit: `task/003-pins`; exact implementation hash recorded after commit; independent QA pending.
- Changed files / revision: Household credential/child/authority models and migration, PIN services/views/routes/templates/JS, existing management guard integration, tests/native helpers and architecture/commands/evidence.
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: PIN19/full backend72/household21/bundled browser8 PASS; final whitespace/pepper1 PASS. Standard gates PASS; native100/200 flows, both actual61sec idle locks and post-restart stored PIN/child revisit PASS.
- Verification record: [developer evidence](../verification/003-pins-developer.md); independent QA pending.
- Completion / integration evidence / outcome: Pending
- Remaining risks or blockers: No implementation blocker; independent QA required. Actual child submission007/full board004 remain later. No child deletion controls. OnlyPG17 left running; no pushes authorized.
