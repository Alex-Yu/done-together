# Verification:003 PINs — attempt1

Overall verdict: PASS
Task / specification: [003](../tasks/003-pins.md), [plan](../plan.md), [commands](../commands.md)
Revision or exact working-tree state: implementation `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c` on `task/003-pins`, reviewed at records-only tip `c3bd384206e33347509d369cbda563873a59f74f`. Exact intervening diff changes task/checkpoint/developer evidence only.
Reviewer / independence: Separate QA subagent; no application fixes.
Environment: macOS/Python3.13.15/Django5.2.18/PostgreSQL17.11, isolated disposable PostgreSQL; bundled Chromium/Firefox and installed stable Chrome156.0.8078.48/Firefox159.0; synthetic fixtures only.
Date: 2026-10-29

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | PIN/request/browser suites; independent credential/format probes; inspect maintained hash/pepper mechanism | Protected add/name/PIN updates, exact fourASCII strings/leading zeros, own selected password first/reset, replaced codes fail | Exact0007/0123 accepted; nonASCII/length/newline/padding/blank reject without partial child. Own selected password required; wrong/other-parent password fails; whitespace preserved. Child add/name/reset and old/new verifier checks pass. PIN/hash not read back; native/restart journeys pass | PASS |
| AC-002 | A-opened/B-selected parent, separate sessions, existing002 management guard, foreignIDs/CSRF, version/inactive/reset race tests | Equal member authority scoped per board session; no child/locked/outsider bypass; bootstrap/reset reachable locked | Both members unlock, selectedB distinct from signed-inA; independent session remains locked. Existing settings/invitation and child actions protected. Version reset revokes both active board sessions; inactive selectedB invalidates authority. Two-connection reset/oldPIN race leaves no grant valid at new version. Verified creation/join and own-password recovery still work | PASS |
| AC-003 | Deterministic exact boundary probes, passiveGET/invalidPOST/child verification and accepted activity; real native61s idle |60s exact expiry; parent-only accepted activity extends, passive/failed/child activity never does; board visible | Independent59.999/60/60.001s tests pass. Read/poll-equivalent GETs, invalid child form and child verifier preserve last activity; accepted explicit parent POST extends; exact new deadline denies. Both actual stable browsers idle61s without heartbeat and show locked controls with child visible | PASS |
| AC-004 | Parent/child counter/deadline/session/concurrency tests; own-password path/login identity and separate source probe | Shared five failures/five minutes, correct blocked/no extension, exact retry/success reset; source limiter supplementary | Backend tests and independent probes pass: correct codes/password denied until exact deadline; permitted success clears; concurrent failures retained; parent/child identities separate. Own parentPIN password path shares login identity restriction. Seeded source60-window blocks even valid unlock429/no grant, then allows after60s | PASS |
| AC-005 | Argon2/HMAC/pepper tests/source; no-echo/CSRF/no-store, actual routine-log assertions and controlled DB failure | Salted maintained hash/outsideDB pepper, no plaintext/hash/private values exposed; recoverable errors | RawPIN cannot verify hash directly; changed pepper invalidates. Password/PIN fields blank on re-render, no hashes in ordinary settings. CSRF rejects mutations. Actual generated passwords/PIN values absent from routine logs, private paths redacted. Controlled parent/child DB errors generic503 without private marker or traceback | PASS |
| AC-006 | Actual household isolation, rollback/retry, stable native100/200 keyboard/labels/focus/validation, restart | Protected persistent accessible settings; no false success/partial state | Scoped foreign parent/child/household requests deny. Independent childPIN-save DB error rolls back partial child and leaves authority timestamp unchanged; retry succeeds. Four native PIN/child journeys and allfour post-restart revisit cases pass; six screenshots inspected. No child deletion or actual chore submission claimed | PASS |

## Required checks

Commands from repository root with documented project-local UV/browser exports and ignored dotenv; shared test DB suites strictly sequential. Prepared probes were reviewed against the final contracts before execution; no moving implementation was tested.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `uv sync --locked` | Exit0 |28 resolved/25 checked; locked dependencies retained |
| `uv run python manage.py migrate` | Exit0 | No pending migrations |
| `uv run python manage.py check`; `uv run python manage.py makemigrations --check --dry-run` | Exit0 |0 issues/no drift |
| `uv run python manage.py collectstatic --noinput` | Exit0 |9 files unchanged |
| `uv run ruff check .`; `uv run ruff format --check .` | Exit0 | All checks pass;106 files formatted |
| `uv run pytest tests/unit tests/integration -q --tb=short` | Exit0 |73 passed in30.99s; current20 PIN cases plus53 earlier cases, including final exact-password-whitespace/pepper test |
| `uv run pytest tests/e2e --browser chromium --browser firefox -q --tb=short` | Exit0 |8 passed in59.78s; actual PIN/account/household/skeleton workflows in both engines |
| `uv run pytest -c pyproject.toml /private/tmp/done-together-qa003-probes.py -q --tb=short` | Exit0 |15 independent adversarial probes passed in8.91s; procedures below |
| `uv run pytest -c pyproject.toml /private/tmp/done-together-qa003-failures.py -q --tb=short` | Exit0 |2 passed in1.99s: source throttle and childPIN-save DB rollback/privacy/retry |
| Documented app/Mailpit/geckodriver foreground commands | Started successfully | Loopback app8000/driver4445/SMTP1025/UI8025 only |
| `uv run python tools/verify_pin_browsers.py` | Exit0 | Installed Chrome156/Firefox159 native100%=1280×720/DPR1;200%=640×360/DPR2; overflow=false. Selected other-parent, child add/name/PIN update/replacement/error/keyboard pass |
| Actual idle interval in both stable browsers | PASS | Both100% sessions held open simultaneously, no parent input/automatic heartbeat for61s; controls lock, Birch native child board content remains visible |
| Fresh screenshot inspection | PASS | `.local/pins-{chrome,firefox}-{100,200}.png` and both `-idle.png`: readable board/labels/status; no horizontal clipping/overlap; normal vertical scrolling at200%; locked forms empty and child preserved |
| Actual log/fixture assertions | Exit0 | Generated fixture0600; generated account passwords and synthetic parent/childPIN values absent from ignored routine server log; private path redaction markers present; values not printed |
| QA webserver SIGINT/restart then `uv run python tools/verify_pin_browsers.py --revisit` | Exit0 | Allfour stored households can unlock with replaced parentPIN and view renamed child settings after restart |
| Final SIGINT and socket probes | All exit0 | QA app/Mailpit/driver stopped;8000/4445/1025/8025 closed. DedicatedPG17 remains55432, unrelatedPG13 preserved |
| `git diff --check` | Exit0 | No whitespace errors |

## Independent adversarial procedures

The15 prepared probes use real PostgreSQL/request/service boundaries, distinct synthetic parent passwords and exact PIN strings. They cover three fractional boundary instances59.999/60/60.001, one passive/invalid/child-no-touch versus accepted parentactivity case, two-session reset revocation, selected-parent inactivity, own-password reset sharing login lockout, seven invalid Unicode/padded/length cases and one actual two-connection reset/unlock race. The race pauses real PIN hash verification, starts a reset on another connection and uses a bounded pause to avoid deadlock when correct locking serializes operations. After both requests finish, the old-session management request must deny and the stored credential version must advance. All assertions pass.

The two further probes seed the real shared source limit at60, assert valid unlock429 creates no grant, advance exactly60s and retry successfully. The child-save failure probe injects synthetic OperationalError after child creation begins, captures the actual request log, checks generic503/no-store/no private marker, no partial child and unchanged authority timestamp, then removes failure injection and retries to create exactlyone child. No real database outage or secret was introduced.

Committed tests independently cover child-only fixture checks without authority/touch, five-parentPIN failures/exact300s retry, five concurrent child failures, child expiry/no-extension, selected-own-password verification, real household/role scoping, existing002 protection, CSRF, pepper/hash and DB-error privacy. Source review confirms user→credential serialization between reset/grant and version binding; actual probes verify these guarantees rather than relying on comments.

## Findings and verdict rationale

None. PASS for all six criteria at `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c`. Actual child submission007 and full board004 remain named later integration owners; the test-only child credential route cannot grant parent authority.

003 attempt1/3; active renewed batch2 completions2/10 before integration, setup2/skeleton1/accounts1/households2 histories retained. Task remains In review for administrative completion/integration; user retained requirements review only at final release. QA changed evidence/status only, no Done/merge/push/deployment/external email.
