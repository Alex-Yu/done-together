# Developer evidence:002 households

Overall verdict:PENDING — independent QA required.
Task/specification:[002](../tasks/002-households.md), [plan](../plan.md), [architecture](../architecture.md), [commands](../commands.md).
Revision:`1b01711d3fd9962825e38ba87297a22c976d0a09` on `task/002-households`; subsequent record-only handoff commit changes no implementation.
Reviewer/independence:Developer self-check, not independent QA.
Environment:macOS x86_64/Python3.13.15/Django5.2.18/PostgreSQL17.11; bundled Chromium156/Firefox157; installed Chrome156.0.8078.48/Firefox159.0; isolated synthetic fixtures.
Date:2026-10-28

## Acceptance evidence

| Criterion | Executed checks | Observed | QA verdict |
| --- | --- | --- | --- |
| AC001 | Targeted requests, four PostgreSQL race scenarios, dual bundled journeys, actual Mailpit/stable browser lifecycle | Intended verified recipient joins once; wrong/anonymous/unverified/tampered/reused/expired deny; seven-day boundary; expired replacement/SMTP rollback+retry; competing token/slot/account creation/joins preserve invariants | PENDING |
| AC002 | Actual two-household scoped GET/POST tests, forged IDs, both member settings and capacity actions | Outsiders cannot read/mutate; both member parents have identical available rights; max2 and one household/account enforced by locks/constraints. PIN integration remains003 | PENDING |
| AC003 | Browser Intl suggestion Europe/Warsaw, recipient America/New_York, invalid/missing choice requests, model/direct change attempts, restart revisit | Valid IANA timezone persists unchanged; no partial invalid creation/no timezone controls; stored household zone agrees across computers/restart | PENDING |
| AC004 | Digest storage, nonce exchange, no-referrer private links/same-origin safe forms, no-store, CSRF, request/security log rendering, response secret assertions | Raw key not stored/rendered, no credential hashes or foreign membership data; private URLs/queries redacted; unauthorized requests denied | PENDING |
| AC005 | Installed Chrome/Firefox native100/200 keyboard/create/invite/join/error helper, inspected screenshots, SMTP failure and post-restart revisit | All four native cases PASS; labels/focus/readable reflow/no horizontal overflow; actual Mailpit invitation captured; consistent failure/retry and persisted state | PENDING |

## Required checks

- Targeted household integration17 passed.
- Full server/config49 passed; full bundled browser6 passed, sequential shared disposable PostgreSQL execution.
- Final rejected-flow recovery correction affected test1 passed/16 deselected.
- Django migrate/check/drift, Ruff lint/format, collectstatic and locked sync exit0; static2 copied/6 unmodified.
- Installed Chrome156/Firefox159 native100/200 create/invite/realSMTP/join/keyboard/error helper PASS, metrics1280×720/DPR1→640×360/DPR2/no overflow. Screenshots inspected.
- Real Mailpit invitation capture/API/UI PASS; UI screenshot inspected. App restart then stored-household revisit in all four cases PASS.
- Clean app/mail/driver shutdown exit0; endpoints refused/HTTP000. DedicatedPG17 remains55432, unrelatedPG13 unchanged.

## Findings and resolved issues

Initial model timezone field shadowed the timezone module in its class body; import alias corrected before migration. Browser reload exposed POST resubmission after sending an invitation; successful send now redirects to GET with accessible status, affected request/browser checks passed. Native helper needed project import path and explicit form-navigation/status waits; corrected without product changes, all stable cases then passed. A rejected pending invite could trap wrong-recipient navigation; clearing failed flows restores access to their own household, affected request check passed.

## Services/artifacts

Only dedicatedPG17 remains running. Synthetic credentials, browser profiles/screenshots and captured mail remain ignored .local; no generated credential values are committed or printed. Stable helper seeds verified fixtures explicitly; real registration/verification→household join is separately tested in both bundled browsers. No external mail/push/merge/deployment.

## Verdict rationale

Five criteria have implementation evidence; independent QA must verify the exact recorded commit. Parent PIN/child/board/scheduling integration remains named subsequent tasks.
