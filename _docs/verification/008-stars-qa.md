# Independent QA: task 008

Overall verdict: **PASS**. Date: 2026-10-29. Reviewer: independent task-only QA; no application or test changes.

Verified immutable implementation: `4f965a3c706f821fbc6a25ac601a1ffbd30e41d0` on `task/008-stars`; QA attempt-start checkpoint: `c404747fceb17b3af30f832e81b8858660fde40a`. Environment: macOS, Python 3.13 via uv, PostgreSQL 17 on loopback 55432, installed Chrome 156.0.8078.48 and Firefox 159.0. Synthetic fixtures only. PostgreSQL 13 on 5432 remained running and untouched.

| AC | Independent procedure and observed result | Verdict |
|---|---|---|
| AC-001 | Targeted `test_approval_week_rollover_old_active_and_totals` exercised real approvals, active overdue work, direct current-week completions, older hidden-but-stored completion, reread at rollover, and both LA/Tokyo viewers. Native Chrome/Firefox showed current completion without expansion and text totals. | PASS |
| AC-002 | `test_submit_return_zero_and_retry_one_visible_award` observed zero stars after submission and return, then one after approval/retry; `test_concurrent_actual_approvals_one_visible_star` released two transactions together and observed one approval/card/star. | PASS |
| AC-003 | Rollover test verified Sunday work approved at household Monday belongs to the new week and all-time/history persist. `test_warsaw_dst_calendar_week_exact_boundaries` independently verified 167/169-hour household weeks, before/start/last/next instants, and both viewer zones. | PASS |
| AC-004 | `test_deleted_recurrence_projected_history_survives_fresh_processes` created a real approval, deleted its recurrence, read retained history/totals from two fresh processes, then signed out/revisited. Native journeys also reloaded and retained all-time totals. | PASS |
| AC-005 | `test_actual_foreign_history_totals_and_direct_reads_are_scoped` confirmed foreign IDs/content/credential hash were absent from local totals/body and direct foreign reads denied. Affected permission/error regressions passed. Installed-browser keyboard traversal reached a labeled PIN control with visible focus; textual states/totals remained visible and no horizontal overflow appeared at 100%/200%. | PASS |

## Checks

- `UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_stars.py tests/integration/test_review.py tests/integration/test_board.py tests/integration/test_pins.py tests/integration/test_chores.py tests/integration/test_recurrence.py -k 'not real_no_browser_once_loop_sixty_restart' -q`: **105 passed, 1 deselected in 69.55s**. The deselected case is the unrelated long real scheduler restart loop.
- `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; then `RUN_NATIVE_STARS=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_stars_native.py -q -s`: **1 passed in 23.32s**, four actual installed-engine/zoom cases. Chrome 156 and Firefox 159 each passed at 100% and 200%.
- Inspected `.local/verification/008/chrome-100.png` and `firefox-200.png`: active overdue and current completed cards are readable; visible totals and keyboard focus are clear at both viewport scales. All four screenshots are ignored artifacts.
- Driver exited 0 after Ctrl-C; loopback port 4445 refused connection afterward. PostgreSQL 17/13 listeners verified on 55432/5432. Changes since implementation are documentation only; `_docs/resume.md` remains preserved and excluded.

## Findings and limitations

None. The real no-browser recurrence restart loop was intentionally excluded as unrelated to this task and already has owning-task evidence; scheduler behavior is also covered by task 009/010 gates. No merge, push, deployment, or completion-state change was made.

## Verdict rationale

All five acceptance criteria have independent executable evidence at the immutable implementation. Exact-boundary, DST, race, retention, cross-household scoping, native browser, keyboard and zoom cases passed. Full integrated regression remains task 010.
