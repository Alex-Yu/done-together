# Verification:006 recurrence — independent QA

Overall verdict: PASS
Task: [006](../tasks/006-recurrence.md)
Implementation: `47268781b08fedb63330fcaaf27a98a3ee260c77` on `task/006-recurrence` (immutable). Checked at records-only tip `4d449919b888af00e978b493674fd8141cf7bc92`; QA changed no product code. The pre-existing uncommitted `_docs/resume.md` was preserved and excluded.
Reviewer: Fresh independent QA agent, `gpt-6-luna` medium; not the implementer. Date: 2026-10-29.
Environment: macOS, managed Python3.13, Django5.2.18, PostgreSQL17.11 on loopback55432, synthetic disposable test fixtures, installed Chrome156.0.8078.48 and Firefox159.0.

## Acceptance evidence

| Criterion | Independent evidence | Verdict |
| --- | --- | --- |
| AC-001 | PostgreSQL recurrence suite verified daily/selected-weekday creation, creation-date P-07, invalid/foreign-child atomic rejection, latest-only recovery with no pre-creation/backlog date; real browser-free `--once`/60-second loop, interrupt and restart paths passed. | PASS |
| AC-002 | Four household Warsaw DST-midnight cases passed. Reused 005's browser-zone comparison (same occurrence identity/date, differing overdue label in LA/Warsaw) after confirming `static/js/local-dates.js` is unchanged from 005 implementation `2424cdf4fd056a392977ac4414e51df594be4039`. | PASS |
| AC-003 | PostgreSQL cases held daily work in to-do and awaiting-approval over multiple dates; at-most-one-unfinished and no-backlog recovery passed, including database uniqueness invariants. | PASS |
| AC-004 | Completion hook passed scheduled-Wednesday and unscheduled-Tuesday late-completion paths: Monday snapshot retained; Wednesday/next scheduled work appears once; no duplicate for today's completed work. Scheduler/completion races passed. | PASS |
| AC-005 | Title/child/schedule edits preserved current and completed snapshots; the next occurrence used updated values. Edit/completion races passed. | PASS |
| AC-006 | Deletion in to-do and awaiting-approval removed unfinished work, stopped generation, and retained completed occurrence snapshots after definition deletion. The actual approval/star workflow is owned by 007/008 and is explicitly scheduled for award-retention recheck there. | PASS |
| AC-007 | Sign-out/in and board reload retained recurrence data; a fresh scheduler process observed persistent state; deleted definitions left completed history intact. Actual earned-award integration is rechecked with 007/008. | PASS |
| AC-008 | Household/foreign-child scope, locked parent guard, missing CSRF, version conflicts, and database failure returning recoverable 503 without false success passed. Six independent-transaction race cases passed. Native Chrome/Firefox keyboard, weekday selection, validation, edit/delete and focus/label checks passed at100%/200%. | PASS |

## Required checks

- `PATH="$PWD/.local/postgresql/bin:$PWD/.local/bin:$PATH" UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_recurrence.py -q` — **29 passed in88.58s**; includes actual browser-free 60-second scheduler loop/restart and temporary connection-failure recovery.
- `PATH="$PWD/.local/postgresql/bin:$PWD/.local/bin:$PATH" UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_recurrence.py::test_real_scheduler_connection_failure_then_restart tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -q` — **38 passed in22.25s**.
- `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; then `PATH="$PWD/.local/postgresql/bin:$PWD/.local/bin:$PATH" UV_CACHE_DIR=.local/uv-cache PLAYWRIGHT_BROWSERS_PATH=.local/playwright RUN_NATIVE_RECURRENCE=1 uv run pytest tests/e2e/test_recurrence_native.py -q -s` — **1 passed in27.71s**, Chrome156/Firefox159 at native100% and200%. All eight error/delete screenshots inspected; text remained readable with vertical scrolling and no horizontal overflow. Artifacts: ignored `.local/verification/006/`.
- `uv run python manage.py makemigrations --check --dry-run`, `check`, and `migrate --check`; `uv run ruff check .`, `ruff format --check .`; `git diff --check` — all exit0; no migration drift, no system issues, all131 Python files formatted.

The first recurrence command was blocked by sandbox loopback policy before tests ran; the same command with approved local DB access passed. The first native attempt omitted the documented geckodriver startup and stopped before Firefox assertions; after starting the repository-owned driver, the full four-case retry passed. These setup retries exposed no product failure. Suites sharing the disposable database ran sequentially. QA stopped its owned geckodriver; project PostgreSQL17 remains on55432, unrelated PostgreSQL13 on5432 is untouched.

## Findings and remaining integration ownership

No task006 product findings. Actual protected approval HTTP, award creation and real approval/earned-star retention are not implemented in006; preserve and rerun them when007/008 integrate. Totals/weekly visibility remain008 and synchronization009. Full release journeys remain010.

## Verdict rationale

All eight criteria passed against the immutable implementation commit, with later-task integration boundaries recorded above. Attempt006 is1/3; batch2 remains5/10 until integration. No source changes, merge or push were made.
