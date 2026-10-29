# 009: Synchronization, concurrent-action handling, and offline recovery

Status: In review
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/9
Local task: `_docs/tasks/009-synchronization.md`
Requirement links: [REQ-021](../plan.md), [REQ-022](../plan.md), [REQ-023](../plan.md)
Dependencies: [008](008-stars.md) Done/integrated `6a3b2d5dd2c529c9af40f351f299c03d18569dbf`; independent QA1 and affected integration gates PASS.

## Goal

Connected computers converge automatically and disconnected boards stay read-only.

## Acceptance criteria

- [ ] AC-001: REQ-021: Two independent browser sessions/profiles on this Mac cover child/profile, chore create/edit/delete, submissions, returns/approvals, and resulting totals without manual refresh; each accepted mutation is visible within five seconds (P-06). User accepted this same-host setup on 2026-10-29 for the two-computer evidence gate. Evidence must identify one-host sessions and make no claim of two-physical-computer testing.
- [ ] AC-002: REQ-022: Disconnect preserves visible board and disables actions; reconnect refreshes data automatically before actions resume.
- [ ] AC-003: REQ-023: Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed.
- [ ] AC-004: Affected changes enforce household isolation, protected parent/child permissions, persistent data, accessible keyboard interaction, and recoverable validation/failure states under REQ-003/023/025/026/027; no credential exposure or false success.

## Out of scope

Technology selection, unrelated release features, public launch, deployment, paid service provisioning and excluded product scope. Later workflow ownership and synthetic-fixture boundaries are explicit in the verification plan; do not claim later integrated behavior complete based on fixtures.

## Constraints

Follow the confirmed first-release scope and P-01–P-07 in [plan.md](../plan.md). Use the selected Django 5.2/Python 3.13/PostgreSQL 17/HTMX approach in [architecture.md](../architecture.md), ADR-001–003 and the locked setup dependencies. No SQLite substitute, frontend build stack, external email provider or deployment is authorized. Follow [process.md](../process.md) and [testing-guidelines.md](../testing-guidelines.md). The user handed over delivery on 2026-10-28. PM refined scope/verification in parallel on an isolated grooming branch; acceptance IDs and release behavior are unchanged. Ready on2026-10-29: coordinator reused PM scope review `8feda09b8b827736f832fd8dff6a48ece0e7075d` plus narrow user-approved verification clarification `d0be1b30912e489cd54f61fc2c1f720b34ff7f76`; dependency008 and both grooming records integrated. Four ACs/product contracts unchanged. Independent task QA leads to completion/integration; orchestrator requirements review is final-release-only.

## Verification plan

- AC-001: Measure server-accepted change to appearance in a second independent browser session, ≤5 seconds under normal connectivity for every required mutation class: child/profile, chore create/edit/delete, child submission, parent return/approval, and resulting totals. Use two independent sessions/profiles on this Mac; this satisfies the evidence gate. Record timestamps, per-event latency and host/session setup honestly, identifying both sessions as one-host evidence and making no claim of testing across two physical computers. Record actual latency per class, not merely a configured two-second interval. Board revision updates atomically; unchanged revisions avoid content replacement and changed reads form consistent scoped snapshots. Midnight/local overdue and household-week rollover update on idle connected boards without requiring a mutation.
- AC-002: Simulate offline network, failed polls/server requests and reconnection. Preserve the currently open last-synchronized board, display disconnection and disable all mutations; no offline queues. Reconnection fetches a fresh authorized snapshot before enabling writes, including when browser online hints arrive before server readiness. Lost response after a committed mutation reconciles server outcome safely; failed mutation never appears committed. Confirm sign-out/authorization failure clears private view. No persistent browser private cache/service worker or offline reload guarantee.
- AC-003: Stale edit/review/deletion races across browsers produce valid outcome or explicit conflict with refreshed data; no duplicate work/award and no silently lost incompatible edit. Preserve focused control, open forms, unsaved input and selection while polling/refreshing; deferred refresh must not erase edits or allow stale writes. Poll/view/child traffic never extends parent unlock; server protection still expires at60 seconds.
- AC-004: Cross-household snapshot/version/direct requests deny; fragments contain no hashes/tokens. Failure/offline status is textual/accessibly announced, keyboard focus retained and disabled state understandable in stable Chrome/Firefox at1280×720/200%. Repeat persistence/transaction races and required server/browser regressions. Two independent sessions exercise privacy/session independence; identify their same-host setup in evidence. The user accepted this setup for the two-computer synchronization evidence gate; do not represent it as cross-physical-computer testing.

For each named AC, record expected and actual observations at the exact implementation commit using [verification template](../templates/verification.md). Run targeted PostgreSQL integration/browser checks and required regression commands in [commands.md](../commands.md); developer records exact selectors before handoff, and empty selections do not pass. Use synthetic data and isolated test settings/in-memory mail. Missing environment or evidence is BLOCKED.

## Questions and assumptions

Product scope and architecture are confirmed; no consequential product question identified. Existing setup/skeleton/account commands are verified; new feature commands remain UNVERIFIED until their owning task executes them. Dependency008 and grooming integrated; readiness reuses valid product PM review plus approved same-host evidence clarification. No material question found; minor sequencing assumptions are explicit in verification plan. GitHub issues are authoritative. Existing issues were inspected before initial creation; match by local task ID/path at each synchronization to avoid duplicates.

## Handoff

- PM parallel scope review: 2026-10-28; acceptance IDs/behavior retained, concrete per-criterion checks and later integration ownership recorded. Draft until dependency/grooming integration and current readiness review; isolated grooming commit supplied to orchestrator for develop integration.

- Implementation summary: Household-serialized revision/snapshot polling updates board regions and calendar boundaries while preserving forms; failed/offline requests retain last board with writes disabled until authorized resync. Explicit stale child edits and unknown committed-response handling protect against lost edits/retries.
- Task branch / verified implementation commit: `task/009-synchronization` / `497a573349f791833bdcee3683b3b1c23ed11ad0` (immutable implementation; independent QA pending)
- Changed files / revision: `board/sync.py`, child revision/locking and snapshot route, synchronization/parent/local-date JS, board templates, targeted server/native tests. No schema/dependency change.
- Final branch tip / delivery commit / integration results: Records-only tip follows; independent QA and integration pending.
- Push status / authorized remote and branch targets: No pushes authorized
- Checks and results:109 affected server tests PASS (4 new synchronization cases);3 native tests PASS plus one required narrow Firefox200 form spotcheck PASS.36 same-host mutation events0.9051–2.0266s. System/drift/static/Ruff/diff PASS.
- Verification record: [009 developer](../verification/009-synchronization-developer.md)
- Completion / integration evidence / outcome: Independent QA next; not Done/merged.009 QA0/3 until dispatch; batch2 remains8/10.
- Remaining risks or blockers: None for implementation. Evidence explicitly uses independent profiles on one Mac, not two physical computers. Initial Firefox form zoom-reset gap closed by narrow actual200 repeat; blank Chrome200 offline capture excluded as visual evidence. See verification record for exact retained scopes.

- Coordinator readiness2026-10-29:008 integrated,45 affected integration tests/static/migration PASS; original PM grooming8feda09 plus narrow clarificationd0be1b3 integrated at `046a9cdb18278ee35cafd00685912d9a0f9be16b`. User accepted two independent browser sessions; all<=5second per-event/class measurements, offline/reconnect/focus/privacy requirements unchanged. Fresh developer next;0090/3.
