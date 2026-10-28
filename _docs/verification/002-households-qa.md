# Verification:002 households — attempt1

Overall verdict: FAIL
Task / specification: [002](../tasks/002-households.md), [plan](../plan.md), [architecture](../architecture.md), [commands](../commands.md)
Revision or exact working-tree state: implementation `1b01711d3fd9962825e38ba87297a22c976d0a09` on `task/002-households`, reviewed at records-only tip `114b8f23086fd9784f296bcf0aa06cac3e34f66c`. Exact intervening diff changes task/checkpoint/developer evidence only; no implementation change.
Reviewer / independence: Separate QA subagent; no application fixes or criteria changes.
Environment: macOS x86_64/Python3.13.15/Django5.2.18/PostgreSQL17.11; bundled Chromium/Firefox; installed stable Chrome156.0.8078.48/Firefox159.0. Isolated PostgreSQL tests and synthetic local Mailpit fixtures only.
Date: 2026-10-28

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | Independently run household/request races and both bundled registration→invitation→join journeys; actual SMTP/stable helper | Intended verified recipient once; seven-day/replay/wrong-recipient/expired denial, replacement/retry and atomic membership limits | Targeted17 household cases included in49 passing server cases; all four token/last-slot/join-vs-join/create-vs-join race modes pass. Seven-day just-before/exact/after expiry, invalid/unverified/wrong/reused flows, expired replacement and SMTP rollback/retry pass. Actual new invitation capture/join succeeds in four native browser/zoom cases | PASS |
| AC-002 | Inspect services/constraints and executed actual two-household/forged-ID/equal-right tests | Scoped membership read/mutation, equal parents, one household/account and at mosttwo parents | Outsider/foreign/nonexistent IDs deny403 without private recipient/member data. Both parents see/manage same household and both receive capacity conflict. OneToOne user and unique constrained slots1/2 plus real transaction races preserve limits. Parent PIN integration remains003 | PASS |
| AC-003 | Browser timezone contexts, invalid/missing input/direct edit tests; native/restart revisit | Browser IANA suggestion; stored immutable timezone shared across computers/restarts, no partial invalid creation | CreatorWarsaw suggestion, recipientNew_York seesEurope/Warsaw in bundled journey. Invalid/empty zone rejects400/no partial work; second creation409; direct settings input/model save cannot change stored zone. No timezone-change UI. Native and post-restart four-case revisit pass | PASS |
| AC-004 | Digest/session/CSRF/referrer/no-store/response/log checks plus independent household DB-exception probe | Protected private links/credentials and recoverable failures without private internal detail | Normal flows pass: onlySHA256 token stored, nonce/session join, no-referrer private URL, same-origin forms, no-store/CSRF/nontransferable flow, redacted routine keys. However F001 emits injected private DB-error detail in technical response/logs for household route under documented local DEBUGTrue | FAIL |
| AC-005 | Stable keyboard/native100/200% creation/invite/join/error checks; SMTP state failures/races; restart; independent DB failure | Accessible persistent isolated state and recoverable failures with no false success/private exposure | Browser/accessibility, SMTP rollback/retry, race/persistence checks pass and screenshots inspected. F001 returns unhandled technical500 rather than generic recoverable household failure; fix required | FAIL |

## Required checks

Commands from repository root with documented project-local UV/browser exports and ignored dotenv. Suites ran sequentially against the shared disposable PostgreSQL database. No real credentials, private tokens or connection representations printed.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `uv sync --locked` | Exit0 |28 resolved/25 checked; locked dependencies retained |
| `uv run ruff check .`; `uv run ruff format --check .` | Exit0 | All checks pass;92 files already formatted |
| `uv run python manage.py migrate` | Exit0 | No pending migrations |
| `uv run python manage.py check`; `uv run python manage.py makemigrations --check --dry-run` | Exit0 |0 issues/no changes detected |
| `uv run python manage.py collectstatic --noinput` | Exit0 |8 static files unchanged |
| `uv run pytest tests/unit tests/integration -q --tb=short` | Exit0 |49 passed in10.29s, including all17 household cases and account/bootstrap regression |
| `uv run pytest tests/e2e --browser chromium --browser firefox -q --tb=short` | Exit0 |6 passed in33.86s; real registration/verification/invitation/join in both engines, independent timezone contexts |
| `uv run pytest -c pyproject.toml .local/qa_households_extra.py -q --tb=short` | Exit1 |1 failed in1.16s: independent controlled household DB-exception probe, F001. Boolean response-privacy assertion prevents dumping response/connection data |
| Documented loopback app/Mailpit/geckodriver starts | Successful | App8000/driver4445/SMTP1025/UI8025 bind127.0.0.1 only |
| `uv run python tools/verify_household_browsers.py` | Exit0 | StableChrome156.0.8078.48/Firefox159.0, native100%=1280×720/DPR1;200%=640×360/DPR2; no horizontal overflow; keyboard/labeled focus,create/invite/actualSMTP/join/full-household/reused-link errors |
| Fresh screenshot review | PASS | Eight `.local/household-{chrome,firefox}-{100,200}{,-invalid}.png`: readable headings/timezone/member text/errors, normal vertical scroll at200%, no overlapping/horizontally clipped content |
| Actual Mailpit API/UI and live-log privacy assertions | Exit0 | Four new synthetic invitation messages; original raw private paths/key segments and generated passwords absent from ignored routine log; redacted markers present. Fixture0600. Fresh `.local/household-mailpit-qa-capture.png` visually inspected; no link values displayed |
| QA webserver SIGINT/restart then `uv run python tools/verify_household_browsers.py --revisit` | Exit0 | All four stored household memberships/timezones survive signout/reload/server restart |
| QA-owned app/driver/Mailpit SIGINT and socket probes | All exit0 | Final8000/4445/1025/8025 closed; projectPG17 running55432; unrelatedPG13 unchanged |
| `git diff --check` | Exit0 | No whitespace errors |

## Findings

### F001 — unhandled household database error exposes private error detail

Affected source: `accounts/middleware.py:43` restricts DatabaseError recovery to `/accounts/`, while the same middleware now otherwise covers `/households/`. Any household view/service DB exception after the source-limit check bypasses its generic recoverable failure response.

Reproduction, confined to disposable tests and synthetic marker:

1. Use a verified synthetic parent and `Client(raise_request_exception=False)`; force-login that parent.
2. Monkeypatch `households.views.create_household` to raise `django.db.OperationalError` with a synthetic private-detail marker. This simulates a view/service query failure after the successful source limiter and verified guard; do not stop or corrupt the real database.
3. With documented local `DEBUG=True`, POST `/households/create/` and valid `timezone=Europe/Warsaw`.
4. Inspect the response using a boolean marker-containment assertion without printing response content or connection values.

Expected: generic recoverable503/retry guidance, no private exception detail in ordinary response or routine logs, consistent/no falsely successful operation. Actual: technical500 exposes the synthetic private marker in rendered debug response; django.request emits its exception/stack to the routine handler. The independent probe fails `assert not exposed` (booleanTrue); no real secret was used or printed. Required committed suites still pass because they do not exercise this household-specific post-limiter DB exception path.

Fix routing: developer should extend generic DB-failure handling to affected household endpoints and add regression evidence for failures after initial middleware/authorization checks, including safe rendering without DB-dependent context. Do not relax privacy/recovery criteria or change QA code to obtain PASS. Reverify affected failure/privacy paths at the committed fix and retain unchanged positive evidence explicitly where appropriate.

## Verdict rationale

FAIL because AC004/005 have a confirmed unhandled private-error/recovery path. AC001–003 and all other executed positive checks pass. Return002 to In progress for developer fix on the same branch; fresh QA required. Attempt0021/3 consumed; active batch2 completions1/10, setup2/3/skeleton1/3/accounts1/3 histories retained. Per-task orchestrator requirements re-check was removed by the user; final release review remains. QA changed evidence/status only; no merge, push, external mail or deployment.
