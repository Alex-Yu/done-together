# Developer evidence:001 accounts

Overall verdict:PENDING — independent QA required.
Task/specification:[001](../tasks/001-accounts.md), [plan](../plan.md), [architecture](../architecture.md), [commands](../commands.md).
Revision:Implementation hash recorded after commit in task/backlog.
Reviewer/independence:Developer self-check, not independent QA.
Environment:macOS x86_64/Python3.13.15/Django5.2.18/allauth65.21.0/PostgreSQL17.11; bundled Chromium156/Firefox157; installed Chrome156.0.8078.48/Firefox159.0; synthetic fixtures only.
Date:2026-10-28

## Acceptance evidence

| Criterion | Executed checks | Observed | QA verdict |
| --- | --- | --- | --- |
| AC001 | PostgreSQL account requests/boundaries; dual bundled browser full journeys; actual Mailpit/stable Chrome lifecycle | Signup→verify→login/logout/reload; one-hour3599/3600/3601 rejection boundaries; tamper/replay/password invalidation; generic known/unknown recovery; SMTP failure/resend without duplicate; real capture verified | PENDING |
| AC002 | Five failures across clients, exact expiry/correct password while blocked/no extension; five concurrent sessions; independent Python subprocess; separate source window test | No lost failures, shared DB restriction5min; correct credentials rejected while blocked; exact expiry success clears state; source60/min separately enforced and expires | PENDING |
| AC003 | Argon2 stored credential assertion; CSRF/direct guard; password non-echo; private URL/header and rendered request/security-log tests; exception filtering | No plaintext password response; private keys/query strings/flow IDs redacted; no-store; no-referrer private redirects/same-origin safe forms; base secure/HttpOnly cookies with documented loopback exception | PENDING |
| AC004 | Test-only verified access guard; real stable browser keyboard/nativezoom; SMTP/DB recoverable failures; actual stored account restart/revisit | Anonymous/unverified direct fixture denied, verified allowed; real labels/focus/validation readable at200%; no false success; account survives signout/reload/restart. Actual household/PIN rights remain tasks002–004/007/010 | PENDING |

## Required checks

- Django migrate/check/migration drift/Ruff lint+format/locked sync all exit0.
- Final full server/config regression32 passed (21 accounts+11 bootstrap).
- Final bundled browser account+skeleton regression4 passed (two in each engine).
- Final narrow failure-template and unsent-confirmation safeguards individually reverified:1 passed/20 deselected each. No empty selection.
- collectstatic copied7 files, including allauth/static changes and retained local HTMX.
- Installed Chrome/Firefox helper passed real100/200% browser zoom, keyboard/labeled fields/visible outline/generic validation/password non-echo/no horizontal overflow; screenshots visually inspected.
- Actual SMTP verification/recovery Mailpit capture + installed Chrome lifecycle PASS; Mailpit UI screenshot inspected. Post-webserver-restart stored synthetic account `--revisit` PASS.
- Ignored local credential rotation parity/authenticated SELECT1 PASS; no local credential file tracked; changed-document links/diff checks recorded at handoff.

## Findings and resolved implementation issues

Real native browser POSTs exposed blanket no-referrer→Origin:null/CSRF403. Fixed by private-key→nonce-bound server session redirect and same-origin token-free forms, retaining no-referrer on private URL responses and all CSRF protections. Older-tab nonce mismatch is tested; GET never verifies.

Exact accessible labels include colons and capitalized New Password; browser test locators corrected after inspecting rendered forms. Overlapping test suites accidentally shared a disposable DB and caused teardown errors; discarded those results and reran strictly sequentially. A failing framework trace included local connection parameters; project-only password rotated immediately, ignored configuration parity/SELECT1 checked, short traceback default adopted. No values retained in evidence/source.

## Services/artifacts

Only dedicated PG17 remains running55432; unrelated PG13:5432 preserved. App/Mailpit/geckodriver stopped after checks. Private screenshots/generated synthetic credentials remain ignored .local. No external mail, push, merge or deployment.

## Verdict rationale

Four criteria have implementation evidence; independent QA must reverify the recorded commit. Later household/PIN behavior is explicitly unclaimed and assigned to subsequent tasks.
