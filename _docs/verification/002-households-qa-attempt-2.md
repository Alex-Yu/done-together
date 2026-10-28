# Verification:002 households — attempt2

Overall verdict: PASS
Task / specification: [002](../tasks/002-households.md), [commands](../commands.md)
Revision or exact working-tree state: fix implementation `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a` on `task/002-households`, reviewed at records-only tip `49cd31869dc82b85b5361302caa92a2c79d86ee4`.
Reviewer / independence: Separate QA subagent; no implementation fixes.
Environment: Same macOS/Python3.13.15/Django5.2.18/PostgreSQL17.11 checkout/toolchain as [attempt1](002-households-qa.md). No new app/mail/browser-driver services started for this scoped fix.
Date: 2026-10-28

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | Fresh full server regression plus exact delta inspection; retain prior native/SMTP/invitation browser observations | Recipient/expiry/consumption/replacement/race behavior remains correct |53 server tests pass, including all prior17 household cases plus4 failure cases. Seven-day boundaries/wrong/anonymous/unverified/reused flows, SMTP rollback/retry and all membership races remain passing. Prior6 bundled and4 stable/native actualSMTP journeys apply to unchanged domain/UI/helper code | PASS |
| AC-002 | Fresh scoped isolation/equal-right/constraint/race checks in full suite; compare domain source | Equal scoped rights and membership limits retained | Actual two-household/forged-ID/parent capacity tests pass; household models/services/views untouched by fix. No new authorization path | PASS |
| AC-003 | Fresh invalid/missing/immutable timezone tests; retain unchanged timezone-context/restart evidence | IANA suggestion/immutability/persistence preserved | Server tests pass; timezone form/JS/domain and browser helpers byte-identical to attempt1. Previously inspected creatorWarsaw/recipientNew_York and stable/restart observations remain applicable | PASS |
| AC-004 | Reproduce original F001 and four DEBUGTrue failure cases, actual rendered-log/header assertions; retain normal-flow token checks | No private details/tracebacks; generic no-store failure, safe token/session privacy | Original unchanged QA probe1PASS. New create/settings-render/invite/join failure cases4PASS:503, no private marker in response/log, no traceback, no-store/same-origin, join nonce redacted. Previous digest/CSRF/referrer/normal routine-log/browser checks remain applicable | PASS |
| AC-005 | Four affected failure/rollback/retry cases plus full server regression; retain unchanged stable/accessibility/persistence evidence | Recoverable failure, unchanged state and successful retry; no regression in accessible persistent journeys | Every injected failure returns generic retry guidance, domain counts/consumption unchanged; same input/current invitation retries successfully after recovery.53 server tests pass. Prior stable100/200% screenshots/actualMailpit/restart checks retained for unchanged normal paths | PASS |

## Required checks

Working directory: repository root. Used documented project-local UV/browser exports, isolated disposable PostgreSQL test database and short tracebacks; suites executed sequentially. No secret/connection values printed.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| Exact original implementation→fix diff | PASS | Application delta only `accounts/middleware.py`: DatabaseError recovery now covers both `/accounts/` and `/households/`. Four parametrized regressions added; remaining changes are docs/evidence/status. Fix→review tip is records only |
| `git diff --exit-code 1b01711d3fd9962825e38ba87297a22c976d0a09..8269f5a6f5bd6fb71468a93e1a2c405f0aea519a -- households templates static tools uv.lock pyproject.toml .env.example .gitignore` | Exit0 | Domain/UI/static/helper/dependencies/config unchanged; explicit evidence-retention basis |
| `uv run pytest tests/integration/test_households.py -k domain_database_failures -q --tb=short` | Exit0 |4 passed/17 deselected in1.87s; create service/settings render/invitation transaction/join service failures underDEBUGTrue |
| `uv run pytest -c pyproject.toml .local/qa_households_extra.py -q --tb=short` | Exit0 | Original unchanged independent F001 reproduction now1 passed in1.26s |
| `uv run pytest tests/unit tests/integration -q --tb=short` | Exit0 |53 passed in11.80s; prior features and new recovery paths |
| `uv run python manage.py check` | Exit0 |0 issues |
| `uv run python manage.py makemigrations --check --dry-run` | Exit0 | No changes detected |
| `uv run ruff check .`; `uv run ruff format --check .` | Exit0 | All checks pass;94 files already formatted |
| `git diff --check` | Exit0 | No whitespace errors |

The affected tests inject synthetic OperationalError after middleware/authorization without disrupting the real database. They capture the actual django.request handler output, assert no private marker/traceback and no-store/referrer headers, compare household/membership/invitation/consumption counts before/after, then remove failure injection and retry successfully. Invitation-transaction injection proves rollback of intermediate invitation state; join retry uses the existing session/current invitation.

## Retained evidence and findings

[Attempt1](002-households-qa.md) remains intact as historical FAIL. Its executed positive49-server/6-bundled-browser, four installed Chrome156/Firefox159 native100/200 create/invite/actualSMTP/join/error journeys, nine visually inspected screenshots, actual captured-key log assertions and four post-server-restart revisit observations are retained. These normal paths, domain models/services/views, templates/JS/helpers, packages and local service configuration are unchanged; only generic failure handling changed and was independently retested with account/household regression. Unchanged browser flows were not needlessly repeated.

F001 resolved: household DatabaseError now receives the same safe, database-independent unavailable template as account failures. No remaining finding/blocker. Task003 must still add parent PIN protection to household management; this staged feature is not claimed by002.

## Verdict rationale

PASS for all five criteria at `8269f5a6f5bd6fb71468a93e1a2c405f0aea519a`, with fresh affected evidence and explicit unchanged evidence retention.002 attempts2/3; renewed batch2 completions1/10 before integration; setup2/skeleton1/accounts1 histories preserved. Task remains In review for administrative completion/integration; user retained requirements review only at final release. QA changed evidence/status only, no app fixes/Done/merge/push. Only dedicatedPG17 remains running; no new temporary services.
