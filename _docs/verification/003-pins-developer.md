# Developer evidence:003 PINs and parent authority

Overall verdict:PENDING — independent QA required.
Task/specification:[003](../tasks/003-pins.md), [plan](../plan.md), [architecture](../architecture.md), [commands](../commands.md).
Revision:`d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c` on task/003-pins; subsequent handoff-only records change no implementation.
Reviewer/independence:Developer self-check, not independent QA.
Environment:macOS/Python3.13.15/Django5.2.18/PostgreSQL17.11; bundled Chromium/Firefox; installed Chrome156.0.8078.48/Firefox159.0; synthetic isolated fixtures only.
Date:2026-10-29 (work began2026-10-28).

## Acceptance evidence

| Criterion | Executed checks | Observed | QA verdict |
| --- | --- | --- | --- |
| AC001 | Selected-parent own password first/reset, leading-zero child addition/name/PIN updates, old/new verifier, malformed ASCII/Unicode requests | Own selected account password only; raw PIN strings preserved; replaced codes fail; no partial child, no deletion controls. Exact whitespace/pepper final case passes | PENDING |
| AC002 | A-opened/B-selected grants and isolated sessions; existing002 settings/invites guarded; foreign IDs, child code, CSRF, reset version/inactive selected parent | Both members can unlock same board session; no global grant; locked/outsider/child requests deny. Bootstrap creation/join and password recovery stay reachable. Old versions/inactive identities revoke | PENDING |
| AC003 | Deterministic59/60 and89/90 boundaries, passive views/failed actions/child fixture checks; two installed browsers actually idle61sec | Exact server expiry; only accepted explicit parent activity extends; both real browsers lock while child board remains visible. Client does not heartbeat automatically | PENDING |
| AC004 | Parent/child shared identity fifth failure/exact299/300 retry; independent sessions/concurrent failures; own PIN password path shares account limit | Correct code denied while restricted; no deadline extension/lost failures; permitted success clears; identity scopes separate | PENDING |
| AC005 | Argon2/HMAC/pepper separation, password/PIN non-echo, no-store/CSRF, generic controlled DB failure | No plaintext/hash material in ordinary pages; salted maintained hashing and independent pepper; account password whitespace retained | PENDING |
| AC006 | Actual two-household scoped IDs; stable keyboard/native100/200 add/name/PIN/lock/error flows, inspected screenshots, restart revisit | Persistent protected settings, recoverable errors, readable/focused controls/no horizontal overflow. No child deletion or chore submission claimed | PENDING |

## Executed checks

- Targeted PIN19 passed; full backend72 passed in33.78s; household regression21 passed.
- Bundled browser8 passed in49.16s, including account/household/PIN/skeleton journeys.
- Final narrow exact-password-whitespace/external-pepper case1 passed/19 deselected after its one-field correction; current collection20 PIN cases. Prior broader suites not repeated unchanged.
- Migrate/system/migration drift/lint/format/static/locked sync pass; static3 copied/6 unchanged.
- Deterministic paused old-PIN verification versus reset test confirms serialization/version binding; selected-parent inactivity immediately invalidates an A-opened/B-unlocked grant.
- Installed Chrome/Firefox native100/200 full selected-other-parent and child add/name/PIN update/replace/error flows PASS. Both100% cases actually idled61seconds and locked with child board visible; no simulated clock.
- Firefox helper clear-before-fill correction narrowly checked exact edited name at100/200; no repeated real-idle check.
- Post-server-restart stored PIN/child revisit PASS all four native cases; screenshots inspected.
- Owned app/mail/driver stop exit0 and endpoints refuse/HTTP000; PG17 remains55432, PG13 preserved.

## Resolved findings during implementation

Prepared QA review identified reset/grant version race and selected-parent inactive status. Grant now serializes user→credential with reset and rechecks active selected identity; deterministic regressions pass. Earlier household fixtures/journeys were adapted to explicit real PIN unlock, not a bypass. Exact password field preserves whitespace. Native WebDriver fill now clears prefilled names before replacement; narrow checks passed.

## Scope and evidence limits

Child credential-check URL is test-only and cannot grant/touch parent authority. Product child submission007/full columns004 are unimplemented. Child operations are add/read/name-or-PIN update only; no deletion UI/endpoint. Generated fixture passwords/screenshots/profiles are ignored/private; no external mail/push/merge/deployment. Independent QA must verify the exact committed state.
