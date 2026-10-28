# Verification:001 accounts — attempt1

Overall verdict: PASS
Task / specification: [001 accounts](../tasks/001-accounts.md), REQ001/007/027 and scoped cross-cutting REQ003/023/025/026 checks; [commands](../commands.md)
Revision or exact working-tree state: implementation `5f471f53c8b17128b9bd63c69af8fefa2028c6ab` on `task/001-accounts`, independently reviewed at `b5eb43ea7abe2d1c6539085023840b4565878a9c`. Exact intervening diff contains handoff records and user-requested workflow documentation only, no application/runtime change.
Reviewer / independence: Separate QA subagent; no implementation fixes.
Environment: macOS x86_64; Python3.13.15/Django5.2.18/allauth65.21.0/PostgreSQL17.11; bundled Chromium/Firefox; installed stable Chrome156.0.8078.48 and Firefox159.0. Real PostgreSQL isolated test DB, synthetic data/in-memory automated email; separate loopback Mailpit capture.
Date: 2026-10-28

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | Independently run account/server/browser suites, real SMTP lifecycle and additional session/concurrency probes; inspect allauth hooks | Verified accounts sign in; unverified guard denied; exact one-hour private links, replay/tamper denial and old-password invalidation; recoverable mail failures | Registration→captured email→explicit verification POST→sign-in/reload/sign-out→recovery→old password denied/new password accepted passes in both bundled engines and installed Chrome/actual Mailpit.3599s accepted,3600/3601 denied for both link types. Malformed/consumed/password-change tokens fail. Known/unknown recovery generic; SMTP failure503/no false success and resend retry without duplicate pass. Independent concurrent confirmation/reset and session binding probes pass | PASS |
| AC-002 | PostgreSQL multi-client failure tests, five-thread concurrent attempts, separate subprocess, exact deadline/source-window checks | Five consecutive failures restrict identity for five minutes across sessions/processes; no lost failures/deadline extension; source limit separate | Fifth failure creates shared deadline, correct password denied during restriction;299s attempt does not extend; exact300s retry succeeds and clears state. Permitted success resets preceding failures. Five independent concurrent clients and second process share counter correctly. Separate60POST/60s source limit returns429/Retry-After and expires without identity substitution | PASS |
| AC-003 | Hash/response/CSRF/header/logger tests; inspect hooks/settings; actual SMTP token/log assertions; native browser forms and independent session probe | Protected credentials, private links/logs, no echo, CSRF and verified-only guard | Argon2 credential; passwords not echoed. Base Secure/HttpOnly cookie settings/local HTTP exception inspected. Original verification/reset responses no-referrer/no-store; token-free forms same-origin/no-store and native POSTs succeed with CSRF. Anonymous/unverified protected fixture denied. Request/security-log tests redact paths/query keys; actual captured keys/email/generated password absent from routine logs; no secret values printed | PASS |
| AC-004 | Stable browser keyboard/real100/200% zoom and screenshot review; guard fixture; failure cases; actual account revisit after server restart | Accessible labeled/focused controls, recoverable errors/consistent persistence, scoped isolation | Chrome156/Firefox159 keyboard email→password→button and generic validation pass; re-render password empty, visible focus/no horizontal overflow. Five fresh screenshots inspected. Sign-out/reload/restart retained synthetic account and replacement password. Concurrent duplicate signup leaves one unverified account with recoverable response. Test-only verified guard checks pass; actual household/PIN isolation remains named later tasks | PASS |

## Required checks

Working directory: `/Users/alexy/Studies/sdd-apps/done-together`. Used documented project-local UV/browser exports and ignored dotenv configuration. All test suites ran sequentially against one disposable PostgreSQL database; live synthetic capture used the separate application database. No verbose connection trace or credential value was printed.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `uv sync --locked` | Exit0 |28 resolved/25 checked; no dependency lock change |
| `uv run python manage.py migrate` | Exit0 | account/accounts/auth/contenttypes/sessions applied; replay no pending migrations |
| `uv run python manage.py check` | Exit0 |0 issues |
| `uv run python manage.py makemigrations --check --dry-run` | Exit0 | No changes detected |
| `uv run ruff check .`; `uv run ruff format --check .` | Both exit0 | All checks passed;79 files already formatted |
| `uv run python manage.py collectstatic --noinput` | Exit0 |7 static files unchanged |
| `uv run pytest tests/unit tests/integration -q --tb=short` | Exit0 |32 passed in6.35s, including21 account cases and11 bootstrap cases |
| `uv run pytest tests/e2e --browser chromium --browser firefox -q --tb=short` | Exit0 |4 passed in19.31s; account lifecycle and retained skeleton in each engine |
| `uv run pytest -c pyproject.toml .local/qa_accounts_extra.py -q --tb=short` | Exit0 |4 independent additional QA probes passed in1.83s; detailed procedures below; ignored QA artifact, no implementation edit |
| Documented loopback webserver, geckodriver and Mailpit foreground commands | Started successfully | App8000, driver4445, SMTP1025/UI8025 bind127.0.0.1 only |
| `uv run python tools/verify_account_browsers.py` | Exit0 | Stable Chrome156.0.8078.48/Firefox159.0:100%=1280×720,DPR1;200%=640×360,DPR2; overflow=false; labeled keyboard/focus/generic validation/password non-echo |
| `uv run python tools/verify_account_mail.py` | Exit0 | Actual synthetic Mailpit verification/recovery captures, explicit verification and installed Chrome lifecycle pass |
| SIGINT/restart webserver, then `uv run python tools/verify_account_mail.py --revisit` | Exit0 | Stored synthetic account signs in and survives reload after process restart |
| Actual capture/log privacy assertions | Exit0 | Read generated fixture locally; assert0600. Obtain its two captured access-link paths privately via Mailpit API; assert original paths/key segments, generated password and email absent from ignored routine server log, with redacted markers present. Output booleans only |
| Fresh screenshot inspection | PASS | `.local/account-{chrome,firefox}-{100,200}.png`: readable labels, visible focus, empty password, clear generic error, no overlap/horizontal clipping; normal vertical scrolling at200%. `.local/account-mailpit-capture.png`: both email types for the newly generated synthetic recipient |
| SIGINT QA-owned app/driver/Mailpit and closed-port assertions | All exit0 | Final ports8000/4445/1025/8025 reject connections; PostgreSQL17 remains running55432; unrelated PG13PID858 unchanged5432 |
| `git diff --check` | Exit0 | No whitespace errors |

## Independent boundary/concurrency procedures

The four extra QA probes used `pytest.mark.django_db(transaction=True)` for competing requests, independent Client/DB connections, distinct synthetic source addresses and a two-worker Barrier; close_old_connections before/finally prevented shared transaction state. No monkeypatched authentication/link implementation was used.

1. Create one unverified synthetic parent/address and sent confirmation. Two clients independently GET the original link to obtain their own session flow; release simultaneous POSTs. Exactly one302 and one404; address verified once.
2. Create one verified parent and reset token. Two independent clients exchange the same token, then simultaneously POST two distinct valid replacement passwords. Exactly one302 and one200; refreshed user accepts exactly one replacement and rejects the original password. The row-lock recheck prevents stale concurrent reset overwrite.
3. Obtain a verification session flow with a CSRF-enforcing client; assert GET does not verify. A separate session's POST to that flow returns400; same-session POST without CSRF returns403. Load the form for its CSRF cookie, move the sent time to one hour old and POST with correct CSRF:404, still unverified. This verifies validity is rechecked at submission after exchange.
4. Simultaneously submit duplicate signup for one synthetic email through two independent clients. Responses are recoverable200/302/503 rather than an unhandled500; exactly one User and one unverified EmailAddress remain. No duplicate/partial verified identity or false authenticated success.

Committed account tests independently execute exact expiry/replay/tamper, cross-process/five-thread lockouts, known/unknown SMTP failures, unsent confirmation rejection/resend, source deadline, password/hash/no-echo, CSRF/guard, actual logger handlers and old-tab nonce invalidation. The extra probes supplement those checks without changing acceptance criteria.

## Findings

None affecting acceptance criteria. Account delivery/DB failures provide generic recoverable responses. Browser-internal Firefox driver diagnostics remain in ignored driver logs; application console/script checks pass. No household/PIN behavior is claimed by this task; named integration owners remain002–004/007 and010.

## Verdict rationale

PASS for all four task criteria at implementation `5f471f53c8b17128b9bd63c69af8fefa2028c6ab`. Attempt0011/3; setup2/3 and skeleton1/3 histories preserved; renewed batch2 completions0/10 before integration. Task remains In review for administrative completion/integration under the user's updated workflow; final release requirements review remains required. QA changed evidence/status only and performed no merge, push, deployment or external mail delivery.
