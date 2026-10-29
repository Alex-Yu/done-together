# Independent QA: task 009 synchronization — attempt 1

Overall verdict: **PASS**. Date: 2026-10-29. Reviewer: fresh independent QA; no implementation changes.
Implementation: `497a573349f791833bdcee3683b3b1c23ed11ad0`, branch `task/009-synchronization`. Checkpoint before execution: `697fb19fa5f6a3af8475c9a952f9f3d0111a44b1` (records only). Environment: macOS, locked Python 3.13/Django 5.2, PostgreSQL 17 on loopback 55432; installed Chrome 156.0.8078.48 and Firefox 159.0. Synthetic isolated data. Both native profiles ran on this one Mac; this is user-approved same-host evidence, not two-physical-computer testing.

## Acceptance evidence

| Criterion | Procedure / expected | Observed | Verdict |
|---|---|---|---|
| AC-001 | PostgreSQL affected suite plus native sessions; every required accepted mutation observed in another profile within 5s without refresh; consistent content/revision, unchanged DOM and drafts preserved; idle boundaries refresh | `109 passed, 1 deselected` in 65.45s. Native synchronization test passed in Chrome/Firefox 100% and 200%; 36 measured events cover child/profile, chore create/edit/delete, submission, return/resubmission, approval and totals, 0.9051–2.0266s. Browser test reported same-host independence, focus/input preservation, and idle Monday/local-date refresh. Detailed measurements: ignored `.local/verification/009/latencies.json`. | PASS |
| AC-002 | Native offline/failed poll and attempted action preserve last board and disable writes; online hint does not resume before fresh authorized snapshot; lost committed response reconciles without retry; access revocation clears private board | Native four-engine/zoom combinations passed unreachable transport, reconnect, form-submit guards, and auth-clear. Chrome actual browser offline and transient HTTP 500 retained the board and recovered after authorized fetch. Lost-response case confirmed one approval, disabled retry, no false-success text, then reconciled the committed result. | PASS |
| AC-003 | Exercise stale edits/reviews/deletion and concurrent persistence, with explicit conflict or valid result; no incompatible overwrite, duplicate award, or authority extension | Native Chrome/Firefox at 100%/200% retained open draft/caret through remote edit, showed stale conflict/current board, and preserved board at parent expiry. The 109-case affected server suite passed race, stale-version, rollback, persistence and authorization checks. Lost-response replay remained exactly one approval. | PASS |
| AC-004 | Verify household/role/CSRF/privacy boundaries, persistence, accessible keyboard/status/recovery behavior in stable Chrome/Firefox at 1280×720 and 200% | Server suite passed foreign/anonymous/unverified snapshot denial, scoped content, no credential hash/token exposure and affected mutation guards. Native tests passed keyboard PIN access, visible focus, textual status, no horizontal overflow, offline/conflict/reconnect in both engines/zooms. Independently inspected Firefox 200% conflict and uncertain-result screenshots; draft/conflict message and recovery status are legible. Existing account/privacy evidence remains revision-applicable; see [007 QA attempt 3](007-review-qa-attempt-3.md). | PASS |

## Required checks

| Command / check | Result | Evidence |
|---|---|---|
| `UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_sync.py tests/integration/test_stars.py tests/integration/test_review.py tests/integration/test_board.py tests/integration/test_pins.py tests/integration/test_chores.py tests/integration/test_recurrence.py -k 'not real_no_browser_once_loop_sixty_restart' -q` | 109 passed, 1 deselected; exit 0; 65.45s | Targeted PostgreSQL suite; excluded only the unrelated real 60-second scheduler restart journey owned by earlier task evidence. |
| `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error`; `RUN_NATIVE_SYNC=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_sync_native.py -q -s` | 3 passed; exit 0; 218.71s | Four observer browser/zoom cases, four form/conflict/failure browser/zoom cases, idle boundary cases. The Firefox 200% form scenario reapplied/asserted native zoom after navigation. Driver stopped after run. Logs/screenshots/latencies remain ignored under `.local/verification/009/`; blank Chrome 200% offline image is excluded from visual evidence. |

## Findings

None. Developer evidence at the exact implementation hash is corroborative, not substituted for the independent targeted runs above. No broad account/mail or real-minute scheduler journey was replayed. Full integrated release verification remains task 010.

## Verdict rationale

PASS for all four acceptance criteria at `497a573349f791833bdcee3683b3b1c23ed11ad0`. Attempt 0091/3; batch 2 remains 8/10; prior retry counters including 0073/3 are unchanged. This QA record changes documentation only. Task remains In review for coordinator bookkeeping/integration. No Done, merge, push or deployment. User `_docs/resume.md` remains untouched and excluded.
