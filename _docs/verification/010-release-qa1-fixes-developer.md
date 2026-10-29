# Verification:010 QA1 fixes — developer

Verdict: **PASS for scoped developer fixes; independent QA2 pending**. QA1's original FAIL is preserved in [independent record](010-release-qa.md).
Task: [010](../tasks/010-release-verification.md), REQ-026 and mandatory browser gates; all27 ACs unchanged.
Immutable correction: `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3` on `task/010-release-verification`, following QA1 routing tipc732979. Documentation-only handoff follows.
Reviewer: same task developer; focused high-reasoning investigator proved QA002 and executed native diagnostics, not independent release QA.
Environment:2026-10-29, same locked Python/Django/PostgreSQL17:55432, installed Chrome156.0.8078.48/Firefox159.0; unrelated PostgreSQL13:5432 preserved. Synthetic fixtures only. No product/configuration/dependency changes.

## Findings and correction

| Finding | Expected / demonstrated cause | Correction / actual developer result |
| --- | --- | --- |
|F010-QA001|A locked board remains visible with recoverable PIN unlock and no management access. QA1 exact old caption failed when the legitimate synchronized explanation was appended.|Both bundled assertions now scope `#parent-lock-status` to locked prefix and require visible board, visible/enabled Unlock button and absent Manage household settings link. Both complete PIN journeys PASS; existing child/reset/old-PIN denial assertions retained.|
|F010-QA002|Tab must reach an actually focused, labeled control with visible outline. Original diagnostic reached retained `activeElement=note` while actual focus was in Firefox browser chrome, not the page.|Before Tab, snapshot was not ready and form controls were disabled, so native Tab skipped them. Later the stylesheet was fully loaded/readyState complete, but content `hasFocus`,`:focus`,`:focus-visible` remained false across8 frames; chrome trace identified browser tablist focus. Shared helper now awaits authorized synchronization before Tab and atomically requires actual document/element focus,`:focus-visible`,non-none positive-width outline and label. Native review4 cases and12 positive/negative controls PASS; no DOM focus repair or product CSS change.|

Corrected Firefox100 trace: initial connectedfalse/disabled form → authorized connectedtrue/enabled form → real keyboard note focus,`:focus-visible`,solid3px outline,1label. Original and corrected screenshots were inspected: absent original page outline versus clear brown corrected outline. Evidence remains ignored under `.local/verification/010/`: `qa002-original-note.json/png`, `focus-firefox-100-note.json/png`, `focus-corrected-firefox-100-note.json/png`, `focus-ready-corrected-diagnostic.log`. Original QA failures remain under `.local/verification/010-qa/`.

Per-case review cleanup now closes the ORM connection context even on assertion failure, preventing the diagnostic's disposable-DB teardown leak. This changes test resource cleanup only. No focus or label check was removed; checks are stricter than before.

## Exact checks

Commands ran from repository root; suites were sequential under explicit DB/browser ownership. Native driver used `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`.

| Command | Actual result / evidence |
| --- | --- |
|`PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_pins.py --browser chromium --browser firefox -q`|2 PASS18.46s; `.local/verification/010-qa1-fixes/bundled-pins.log`|
|`RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_review_native.py::test_native_submission_return_resubmit_approval -q -s`|1 PASS31.33s across installed Chrome/Firefox100/200, no skips; `.local/verification/010/focus-review-final.log`|
|`PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run python .local/verification/010/focus-helper-negative.py`|12/12 actual native controls PASS:4 labeled solid3px focused controls accepted;4 focused controls with outline:none rejected;4 focused unlabeled controls rejected. `focus-helper-negative.log/json` in010 artifacts|
|`UV_CACHE_DIR=.local/uv-cache uv run ruff check .`; `uv run ruff format --check .` with same cache; `git diff --check`|PASS;157 formatted files. `.local/verification/010-qa1-fixes/ruff.log`, `format.log`|
|Read-only listener/DB/hash checks after test handles exit|8000/8025/1025/4445 closed;testDB0sessions;PG55432/5432 alive;original resumeSHA unchanged. `010-qa1-fixes/cleanup.json`; investigator driver66413 stopped exit0, `010/focus-cleanup.json`|

## Retention and routing

`git diff 3769e5c9dba30388c7aa127af9fb2124f62444d0 dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3 -- accounts households chores board config static templates manage.py pyproject.toml uv.lock` is empty. Only code changes are `tests/e2e/test_pins.py`, `tests/e2e/test_review_native.py` cleanup and `tools/verify_household_browsers.py` focus verifier. Locked dependencies/environment unchanged.

Retain fresh independent QA1's166 server PASS152.82s, unchanged domain/security/config/static/actual SMTP/61sec idle/restart/privacy evidence and26 passing AC rows by exact unchanged product/configuration paths. Do not treat QA1's failed browser checks as passing. Because shared native focus verification changed, independent QA2 must replay **all13 native tests**, including four full keyboard journeys, plus affected bundled PIN cases. Developer deliberately did not repeat unchanged full server/SMTP/idle/restart or broad native suite.

No implementation blocker remains for these fixes; task In review for independent affected QA2 and eventual final orchestrator requirements review. Attempts remain0101/3 until coordinator dispatch; batch2 remains9/10, earlier histories unchanged. User resume.md SHA256 remains `987abed09c813aa9f566613ce5a040e905f0d6751b840f08a7ccaa46d8d5627f` and is excluded. No live owned service/test/browser sessions, merge, push, deployment or external issue write. Coordinator reconciles issue10 review/commit/evidence handoff.
