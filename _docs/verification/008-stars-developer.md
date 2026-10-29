# Verification:008 developer

Overall verdict: PASS (developer checks; independent QA pending)
Task / specification: [008](../tasks/008-stars.md), [prepared W01–W06](plans/007-010-review-sync-release.md)
Revision: `4f965a3c706f821fbc6a25ac601a1ffbd30e41d0` on `task/008-stars`; subsequent commit contains records only.
Reviewer / independence: task developer; independent QA next.
Environment: existing locked Python3.13/Django5.2/PostgreSQL17 loopback55432, macOS; installed Chrome156.0.8078.48/Firefox159.0. Synthetic isolated data only. Unrelated PostgreSQL13:5432 preserved.
Date:2026-10-29

## Acceptance evidence

| Criterion | Procedure / expected | Observed evidence | Verdict |
| --- | --- | --- | --- |
| AC-001 | W01: real approvals before/current household week plus older active work; reread at next Monday | `test_approval_week_rollover_old_active_and_totals` ×2 viewer zones: active retained, current completion directly visible, old hidden/stored, fresh rollover read hides completion with all-time2. Four native cases show actual active/completed cards without expansion. | PASS |
| AC-002 | W02: submit/return/resubmit/approve/retry and simultaneous transactions | `test_submit_return_zero_and_retry_one_visible_award`, `test_concurrent_actual_approvals_one_visible_star`:0 before approval,1 afterward, one card/award under concurrency. Existing007 HTTP races, lost-response rollback and retry regressions pass. | PASS |
| AC-003 | W03/W04: Sunday due approved exact Monday; just-before/at/last/next boundary; DST weeks and viewer zones | `test_approval_week_rollover_old_active_and_totals` ×2 and `test_warsaw_dst_calendar_week_exact_boundaries` ×2: approval-time inclusion, exact end exclusion/new-week inclusion; UTC intervals167/169h; viewer LA/Tokyo does not affect inclusion. No mutation needed for reread. | PASS |
| AC-004 | W05: actual recurrence approval/delete, fresh processes, sign-out/revisit and browser reload | `test_deleted_recurrence_projected_history_survives_fresh_processes`: two independent Python/Django processes query persisted totals1/1 and retained snapshot after deletion; signed-out/reopened session restores same board.007 persistence/P03 tests also pass. Four native reloads preserve totals. | PASS |
| AC-005 | W06: actual foreign completion/history; forged reads, permissions/expiry/error regressions; native keyboard/text/zoom | `test_actual_foreign_history_totals_and_direct_reads_are_scoped` passes: foreign totals0 in own board, private content/hash absent, direct foreign reads403; foreign board independently totals1. Board503 privacy/retry, PIN/authority, review/CSRF/rollback cases pass. Chrome/Firefox100/200: labeled PIN reached by Tab, visible outline, textual totals/states, no horizontal overflow. Four screenshots visually inspected. | PASS |

## Required checks

Commands use `UV_CACHE_DIR=.local/uv-cache uv run` and PostgreSQL suites run sequentially.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `pytest tests/integration/test_stars.py tests/integration/test_review.py tests/integration/test_board.py tests/integration/test_pins.py tests/integration/test_chores.py tests/integration/test_recurrence.py -k 'not real_no_browser_once_loop_sixty_restart' -q` |104 passed,1 deselected in66.61s | `.local/verification/008/server.log`; includes7 new stars tests +97 affected regressions. Added foreign scoping case after suite collection is separately verified below. |
| `pytest tests/integration/test_stars.py -k actual_foreign_history -q` |1 passed,7 deselected in1.83s | `.local/verification/008/isolation.log`;8 unique new tests,105 unique server cases overall. |
| `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`, then `RUN_NATIVE_STARS=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_stars_native.py -q -s` |1 test/four native engine/zoom cases passed in22.73s | `.local/verification/008/native.log`, `{chrome,firefox}-{100,200}.png`. Actual approval records via existing domain services/HTTP child submission, not a patched provider. Native zoom100:1280×720;200:640×360 CSS pixels. Readable text, ordinary vertical scroll; no horizontal clipping. |
| `python manage.py check`; `python manage.py makemigrations --check --dry-run`; `python manage.py collectstatic --noinput` | PASS: no issues/no changes;3 copied8 unmodified | No schema/dependency change. |
| `ruff check .`; `ruff format --check .`; `git diff --check` | PASS;144 files formatted | Final changed tests included. |

## Findings and retained evidence

Initial new rollover test assumed fixture household UTC; fixture is Warsaw. Corrected test boundary to the household's actual calendar Monday, then all affected checks passed. No product defect or scope change.

Existing007 application revision `8b66f1b426de24e4bd9f48affb4e8f0b5e6d3db8`, helper revision `e68c669d145d9edf2c4cd0aec38669c80ce8776a`, integrated `5502e1d1eb057ab79f8865615440b91ed148da54`: authority/transition/limiter/recurrence/local-date code unchanged; targeted97 affected server cases freshly passed. Retain unchanged actual submission-browser/timeliness and elapsed parent-idle/account-mail evidence linked from [007 QA3](007-review-qa-attempt-3.md) and [006 developer](006-recurrence-developer.md). No repeated elapsed minute scheduler/account email journeys. Full integrated regression remains010.

Owned native browser/test-server sessions closed, driver stopped exit0. PG17 and unrelatedPG13 retained. No credentials or raw private fixtures committed. User `_docs/resume.md` preserved/excluded. No merge/push/deployment.

## Verdict rationale

All five criteria have developer evidence at the immutable implementation. Independent QA is required; task is In review.009 owns periodic idle refresh at time boundaries and synchronization/offline behavior;008 verifies actual board rereads without mutations.
