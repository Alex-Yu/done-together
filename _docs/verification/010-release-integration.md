# Final local release integration —010

Verdict: **PASS**. Date:2026-10-29. Coordinator integration after independent QA2 and final requirements review PASS.

Integrated delivery: `374c2ad42d1ac4b40bb111fc31bf3ed4cf1b66d2` on `develop`, fast-forwarded from `task/010-release-verification`. Reviewed/verified implementation: `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`. Independent QA2 evidence tip `a1c0752baa0ccdb92554e67ffd8ce587844781f7`; [QA2 record](010-release-qa-attempt-2.md), [final requirements review](010-release-requirements.md). Completion and later record commits change documentation only.

## Exact-state and gate audit

- `git diff --name-only dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3 374c2ad42d1ac4b40bb111fc31bf3ed4cf1b66d2` contains only `_docs/` paths. Implementation, tests, helpers, configuration and locked dependencies are identical to the independently verified/reviewed code. No conflict or implementation edit occurred during fast-forward.
- All27 task010 acceptance criteria, REQ-001–027, P-01–P-07 and J-01–J-05 have QA2 PASS and final requirements review PASS. QA1 FAIL remains historical; both findings cleared by fresh affected QA2. Six unchanged non-PIN bundled cases plus two fresh PIN cases cover eight unique bundled cases; full166 server and actual SMTP/real61sec idle/restart/privacy/schema evidence retained only with documented revision/environment proof. All13 native tests and12 focus controls are fresh at final code.
- Independent QA2 measured36 events across nine classes/four native observer engine/zoom contexts at0.9949–1.9487seconds accepted-server-clock→other-profile DOM, all<=5seconds. Profiles are independent on this one Mac; no two-physical-computer claim.

## Executed integration checks

Repository root; `UV_CACHE_DIR=.local/uv-cache`. Only one disposable PostgreSQL suite ran. Sanitized ignored artifacts: `.local/verification/010-integration/results.json` and `check-0.log` through `check-6.log`.

| Command | Actual result |
| --- | --- |
|`uv run python manage.py migrate`|Exit0; migrations current|
|`uv run python manage.py check`|Exit0; no system issues|
|`uv run python manage.py makemigrations --check --dry-run`|Exit0; no drift|
|`uv run pytest tests/integration/test_households.py tests/integration/test_sync.py tests/integration/test_release.py -q`|28 PASS19.68s, exit0|
|`uv run ruff check .`|Exit0|
|`uv run ruff format --check .`|Exit0;160 files already formatted|
|`git diff --check`|Exit0|

This is the applicable affected integration pass on the exact merged code. Unchanged full final-release suites are not redundantly replayed; independent QA/review records establish their coverage and retention.

## Completion, preservation and boundaries

Bootstrap and001–010 Done/integrated. Active batch2 now10/10 after010's successful integration; historical batch1 bootstrap2. Attempts preserved: setup2/3,skeleton1/3,0011/3,0022/3,0031/3,0041/3,0051/3,0061/3,0073/3,0081/3,0091/3,0102/3. No new task/batch or reset.

Read-only post-integration state audit PASS (`final-state.json`): owned8000/8025/1025/4445 listeners closed; disposable test database0sessions; PostgreSQL17:55432 and unrelated13:5432 preserved. Original uncommitted `_docs/resume.md` SHA256 remains `987abed09c813aa9f566613ce5a040e905f0d6751b840f08a7ccaa46d8d5627f`, excluded from all delivery commits. No other uncommitted work is introduced.

[Validated startup commands](../commands.md#verified-local-release-2026-10-29) document separate loopback Mailpit, web and independent scheduler foreground processes. Verification services are stopped. Same-host synchronization, local SMTP, synthetic fixtures and explicit viewport/clock evidence limits match approved scope. Production hosting/email/operations remain outside delivery. No push, deployment or external email delivery performed.

Issue10 Done/integrated completion body and CLOSED state exact readback verified after successful integration. All12 mapped delivery issues11/12/1–10 independently read CLOSED; no pending issue synchronization. Ignored artifacts `issue10-done-readback.json` and `issues-final.json` record actual results. Final records commit changes documentation only; source remains unpushed.
