# Verification:005 one-off chores — developer

Overall verdict: PASS (developer; independent QA pending)
Task: [005](../tasks/005-one-off-chores.md)
Revision: `2424cdf4fd056a392977ac4414e51df594be4039` on `task/005-one-off-chores`
Reviewer: task005 developer, not independent QA. Date:2026-10-29.
Environment: macOS, Python3.13/Django5.2 locked dependencies, PostgreSQL17 loopback55432; installed Chrome156.0.8078.48 and Firefox159.0. Synthetic disposable test database/in-memory mail only.

| AC | Expected and observed evidence | Verdict |
| --- | --- | --- |
| 001 | Create definition+occurrence; edit/reassign updates both; eligible deletion removes both. Six invalid-input cases leave neither partial record. Stale edit/delete409 refresh scoped board; awaiting/completed GET/POST denial retains snapshots. Native engines create/edit/delete and recover from server-required-title error. | PASS |
| 002 | Same persisted occurrence ID/due calendar date2026-03-08 at controlled2026-03-09T00:30Z: America/Los_Angeles shows no overdue, Europe/Warsaw shows overdue. Browser clock installed by test only; valid IANA zones include US DST transition. Production compares browser-local calendar without individual due times. | PASS |
| 003 | PostgreSQL sign-out/new login/reload restores edited work; actual runserver start→stop→new process preserves same occurrence/definition and signed-in session. Seeded awaiting/completed snapshots deny deletion; no approval/star workflow is fabricated. Actual earned awards/visible completion-week projection remain007–008. | PASS |
| 004 | Real foreign household/child/work IDs, locked request with child PIN, outsider, expired authority and CSRF fail. Recoverable simulated database error503 never announces success. Competing edit/delete yields exactly one accepted write; stale versions fail; accepted create/edit/delete advance revision exactly3. Four native cases verify Tab focus outlines/labeled fields, keyboard submit/error/edit/delete,1280×720 at100% and640×360 CSS viewport at native200%, no horizontal overflow. Visual inspection corrected child labels/template fragment before final passing rerun. | PASS |

Commands/results, sequential disposable database:

- `UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -q`: **37 passed in19.65s** (12 new005 cases,5 board,20 PIN). Includes actual two-process restart and concurrent service transactions.
- `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; `RUN_NATIVE_CHORES=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_chores_native.py -q -s`: **1 passed in30.53s**, four native engine/zoom cases plus two timezone contexts. Explicit viewport and child-name checks pass. Native OS select/date values use test DOM assignment after keyboard focus/label assertions; navigation, text entry, submit, edit/error/delete use native keyboard. This is targeted feature evidence, not a claim of the full release keyboard-only journey.
- `UV_CACHE_DIR=.local/uv-cache uv run ruff check .`, `uv run ruff format --check .` (**123 files**), `uv run python manage.py migrate --noinput` (chores0001 applied), `uv run python manage.py check`, `uv run python manage.py makemigrations --check --dry-run`, `git diff --check`: **PASS**, no drift.
- Screenshots ignored under `.local/verification/005/{chrome,firefox}-{100,200}-{board,error}.png`; Chrome100 board and both200 error images visually reviewed after fixes: readable names/labels, wrapping and vertical scrolling, no stray fragment/overflow.

Findings: None outstanding. Initial harness keyword/connection/selector/native-popup issues were corrected; visual review found and fixed default model-choice labels and template insertion before final runs. Earlier broad native run passed4 cases but failed a timezone harness selector and left one disposable testDB connection; final run closes those connections and passes without teardown warning. No empty selection is counted as evidence.

Reuse: account/mail and real61-second idle journeys remain valid at003/004 evidence; underlying account/PIN authority/security files unchanged. Board synthetic mixed-state evidence at004 implementation `067addc7eda122736893d17d5ca4aff7ce1a2885` is retained for unchanged presentation; fresh5 board/20 PIN regressions cover integration. Complete integrated/stable-browser journeys remain010.

Lifecycle: In review only; QA attempt005 remains0 until coordinator dispatch. Batch2 remains4/10; all earlier counters preserved. Owned driver/browser/server processes stopped; PG17 retained and unrelatedPG13 untouched. No push. Unrelated `_docs/resume.md` edit preserved and excluded from commits.

Administrative blocker: automatic approval review rejected issue5 In review/evidence update as external disclosure without explicit authorization despite supplied delivery/AGENTS process context. Local handoff remains reviewable; coordinator notified, remote Ready/open retained. No implementation/verification blocker.
