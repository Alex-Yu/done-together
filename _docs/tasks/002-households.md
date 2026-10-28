# 002: Household creation, timezone setup, and second-parent invitation

Status: Ready
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/2
Local task: `_docs/tasks/002-households.md`
Requirement links: [REQ-002](../plan.md), [REQ-003](../plan.md), [REQ-011](../plan.md), [REQ-027](../plan.md)
Dependencies: [001](001-accounts.md) Done/integrated at `3afacd6e58d61f727f5aa2760a7ab0bbff445043`; independent QA1 PASS at `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`; current PM readiness passed.

## Goal

Parents can create a private household and invite the second parent.

## Acceptance criteria

- [ ] AC-001: REQ-002: Intended verified recipient joins once; wrong-address, reused, and expired invitations fail; an expired invitation can be replaced.
- [ ] AC-002: REQ-003: Either member parent can manage the household; outsiders cannot read or change it through UI or direct requests.
- [ ] AC-003: REQ-011/P-02: Creation suggests the creating browser timezone, validates and stores the household IANA timezone, and provides no timezone-change controls. Occurrence identity/scheduling and browser-local overdue interpretation remain linked to tasks 005–007 and release AC-011.
- [ ] AC-004: REQ-027: Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions.
- [ ] AC-005: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning, and scope excluded by the confirmed product plan. Parent/child PIN setup and protected parent controls belong to [003](003-pins.md); child columns/board belong to [004](004-board.md); chore scheduling/local overdue behavior belongs to 005–007. This task verifies actual household membership/data isolation, not those later workflows. Until task003 integrates parent unlock, household creation/join/invitation use verified-account membership authority; task003 must protect existing household management/settings with PIN authority while preserving verified-account bootstrap creation/join.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM current readiness passed after account integration. Reuse `verified_parent_required` and the integrated allauth verified identity. Enforce P-01 (one household per parent, at most two parents), immutable P-02 timezone, recipient-bound seven-day single-use invitations and atomic membership/token consumption in PostgreSQL. Either member has equal rights; do not add owner-only management, parent removal or timezone-change controls.

## Verification plan

- AC-001: Browser/request journeys create a household from a verified account, invite a synthetic second parent, register/verify or sign in as the intended recipient and join. Test seven-day just-before/at-expiry boundaries, malformed/tampered/reused links, wrong-address and unverified/anonymous denial, replacement after expiry, and local SMTP failure followed by successful retry without false success. Exercise real loopback Mailpit invitation capture in addition to in-memory automated tests. PostgreSQL independent transactions test concurrent acceptance of one token, competing invitations for the last parent slot, and competing joins/creation for one account: no double consumption, third member or second household.
- AC-002: Both member parents can perform the available household management actions, with membership-scoped read/mutation queries. Create two actual synthetic households and test outsiders, unverified users, forged household/invitation IDs and direct requests: no cross-household data or changes, recoverable explicit conflicts on incompatible state. Verify one household/account and two parents/household at request and concurrent transaction boundaries. Parent PIN protection is integrated by task003; do not claim it here.
- AC-003: Browser creation suggests `Intl`/IANA browser timezone; valid selection persists unchanged across reload/sign-out/restart and other computers. Invalid/missing timezone creates no partial household; direct attempts cannot modify the stored timezone. Later005–007 verify occurrence dates/local overdue labels; no chore data required now.
- AC-004: Inspect invitation storage, private-link exchange/consumption, response cache/referrer policy and sanitized request logs without exposing real tokens. Reuse account privacy/CSRF/session conventions, test CSRF rejection and unauthorized direct requests. Household responses must not expose account credential hashes, PIN material or another household membership/activity.
- AC-005: Stable Chrome/Firefox keyboard, focus, labeled inputs, status/error text and 200% zoom at the agreed viewport cover create/invite/join/error journeys. Verify persistent household/membership/invitation state across reload/sign-out/server restart; email/validation/race failures leave a consistent recoverable state and never appear successful. No child/PIN workflow is introduced or claimed complete before003.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Account prerequisites are verified/integrated; household-specific commands remain UNVERIFIED until implementation. Five ACs are mapped to checks and named later integration owners; current readiness passed. Verified-account bootstrap authority is a staged implementation assumption until003 protects management settings, consistent with J-01. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM readiness: Ready on 2026-10-28 after account integration; five ACs preserved, selected architecture and dependency confirmed, no consequential question. Full grooming commit recorded in backlog checkpoint.

- Implementation summary: Not started
- Task branch / verified implementation commit: Pending
- Changed files / revision: Initial delivery grooming on `develop`; full grooming commit recorded in backlog checkpoint
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results: Scope/architecture reviewed against confirmed requirements on 2026-10-28; issue reconciliation recorded in backlog checkpoint; implementation verification not run
- Verification record: Pending
- Completion / integration evidence / outcome: Pending
- Remaining risks or blockers: None at readiness; specific access failures route through orchestrator; no pushes authorized
