# Task004 developer verification

Revision: task/004-board implementation commit immediately following this record; exact hash in task handoff. Date2026-10-29. Developer result: PASS, pending independent QA. PostgreSQL17, installed Chrome156.0.8078.48/Firefox159.0.

| AC | Expected / observed evidence | Result |
| --- | --- | --- |
| 001 | Real scoped child columns and setup/empty-work guidance. Internal provider fixture renders to-do, overdue, awaiting approval and completed text under Aster; Birch stays empty. No HTTP fixture selection or production fake chores. | PASS |
| 002 | Old active work and supplied current-week completion remain directly rendered without details/collapse; both native engines inspect4 cards. Actual approval/week filtering/totals remain008. | PASS |
| 003 | Verified household member `/` enters board; settings remains parent-protected with child/PIN controls. Native unlock→settings→board revisits stored children. No dashboard/inert chore controls. Chore/review mutations remain005–007. | PASS |
| 004 | Stable Chrome/Firefox,1280×720 native100%,640×360 CSS viewport/DPR2 native200%; labels, keyboard Tab/Enter, focus outlines, long names and text states; no horizontal overflow. Four screenshots visually inspected. | PASS |
| 005 | Actual second household/anonymous/unverified reads denied, locked child mutation denied, real child unchanged. Passive GET preserves authority timestamp; expired authority locks settings while child remains visible. DEBUG database faults at projection and new entry return generic503 without private response/log detail; retry succeeds. Invalid PIN render retains columns. Existing20 PIN regressions passed. | PASS |

Commands/results (sequential disposable testDB):

- `uv run pytest tests/integration/test_board.py tests/integration/test_pins.py -q`: initial23 passed/1 failed because test expected403 for existing locked settings GET redirect. Corrected expectation; board-only4 passed. Existing20 PIN tests passed unchanged.
- Added new entry failure/anonymous/unverified boundary: `uv run pytest tests/integration/test_board.py -k entry_failure -q`:1 passed/4 deselected after matching existing explicit403 denial contract. Five unique board tests now passed.
- Start `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; `RUN_NATIVE_BOARD=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_board_native.py -q -s`:1 passed, four native engine/zoom cases. Initial execution preceded adding explicit opt-in skip guard; test body unchanged. Driver stopped with Ctrl-C, all browser contexts/test server closed. PG17 retained; unrelated PG13 preserved.
- `uv run ruff check .`, `uv run ruff format --check .` (111 files), `uv run python manage.py check`, `uv run python manage.py makemigrations --check --dry-run`, `git diff --check`:PASS/no migration changes.

Screenshots: ignored `.local/board-{chrome,firefox}-{100,200}.png`; readable wrapped headings/cards, normal vertical scrolling. Native test is tracked and patches read-model provider inside pytest live server only; it never seeds production work. Production provider returns empty work until005–008 integration. No completed-history query/approval/week rollover is claimed.

Verification scope follows user request for affected checks: unchanged accounts/mail and actual61-second timeout native journeys reuse task003/002 evidence; full integrated regression and complete stable journeys remain010 final release. No new dependencies, services or schema changes. No production restart needed for read-only projection; existing persisted Child rows were revisited through new requests/native settings return; prior003 process restart evidence retained.
