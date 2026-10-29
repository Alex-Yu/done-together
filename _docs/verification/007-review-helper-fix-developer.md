#007 F001 helper correction — developer evidence

Developer verdict: PASS for the affected correction; independent QA3 pending. Date:2026-10-29.
Implementation including helper fix: `e68c669d145d9edf2c4cd0aec38669c80ce8776a`, task/007-review. Application behavior remains from `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8`. QA1 FAIL and QA2 BLOCKED histories remain intact; attempts2/3 before final QA3 dispatch, batch2 6/10.

## Proven cause and change

The narrow high investigation reproduced the QA2 setup failure on a synthetic page without Django/DB: the actual Sign in heading was present and ready, but geckodriver started without the documented `--allow-system-access` flag made privileged Firefox zoom fail with HTTP500/System access required. The helper caught that zoom error along with transient navigation errors and falsely reported a5-second heading/sign-in timeout. With the flag, the same heading wait passed. Original evidence: ignored `.local/verification/007/f001-zoom-isolation.log`. This establishes the QA2 setup/diagnostic cause; prior QA1 observations remain preserved rather than rewritten.

Only `tools/verify_household_browsers.py` changes executable behavior: navigation polling catches predicate-read races, then applies zoom outside that catch so setup errors propagate immediately. Firefox native zoom always restores content context in `finally`, including a failure while entering chrome context or evaluating zoom. Product routes/models/templates/permissions and committed tests are unchanged. Commands and task007 now emphasize that the driver flag is mandatory.

## Fresh affected verification

- `UV_CACHE_DIR=.local/uv-cache uv run python .local/verification/007/verify_zoom_fix.py` — PASS on a synthetic loopback HTML page; no DB, accounts, credentials or product routes. Without the flag: heading present, corrected wait propagates actual HTTP500/unsupported operation/System access required in0.01s, rather than timing out; content context restored. With flag: native100%=1280×720/DPR1 and200%=640×360/DPR2 PASS. Injected zoom-evaluation RuntimeError propagates, restores content context, and leaves the heading readable. Both owned drivers/server stopped exit0. Sanitized log: `.local/verification/007/f001-zoom-fix.log`.
- Start the exact documented owned driver: `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`.
- `RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest .local/verification/007/test_firefox_repeat.py -k native_submission -q -s` — **1 passed/1 deselected in18.88s**, both installed Firefox159 native100/200 complete wrong-PIN/submit/required-note/return/resubmit/approve flows PASS; clean teardown. This ignored wrapper restricts the committed journey to Firefox and adds only sanitized server method/path/status/redirect logging. Actual sign-in POST302→GET302→boardGET200 in both cases; recoverable PIN/note400 and accepted transitions302. Log `.local/verification/007/f001-helper-firefox.log`.
- `UV_CACHE_DIR=.local/uv-cache uv run ruff check tools/verify_household_browsers.py`, `ruff format --check tools/verify_household_browsers.py`, `git diff --check` — PASS.

Retained evidence: independent [QA1](007-review-qa.md)97 affected PostgreSQL cases and Chrome100/200/LA-Tokyo checks, plus original developer persistence/security/visual evidence. Actual `git diff 8b66f1b..e68c669 -- accounts board chores config households static templates tests` is empty. The helper delta affects Firefox setup/error reporting and cleanup; normal Chrome zoom remains its unchanged no-op. No broad server, Chrome, account mail or real-minute scheduler suites replayed. Retained006 scheduler evidence remains valid.

Task In review for final independent QA3 with the full driver command above; F001 is not yet independently cleared. Driver31219 stopped exit0, suites/profiles/live server finished; PG17:55432 and unrelatedPG13:5432 preserved. No merge/push; user resume edit untouched/excluded.
