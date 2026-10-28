# Release QA preparation

Status: PREPARATION ONLY — no implementation verdict or executed-check claim.
Prepared independently on `qa/release-verification-plans` from `develop` at `24b5ca3`; upcoming tasks remain Draft until PM readiness/dependency gates. These scenarios interpret the agreed [plan](../../plan.md), [architecture](../../architecture.md) and task criteria, without changing scope. Re-read current authoritative issues/task documents at the actual exact-commit handoff; reconcile later grooming before execution.

- [003–006: identity, board and assignment](003-006-identity-board-assignment.md)
- [007–010: review, totals, synchronization and release](007-010-review-sync-release.md)

## Execution and evidence contract

Use the [verification template](../../templates/verification.md) and [testing guidelines](../../testing-guidelines.md). Every criterion needs actual expected/observed evidence tied to the full implementation hash and environment. Record attempts only when implementation is submitted to QA. No PASS on moving code, source inspection alone where runtime behavior matters, empty selectors or missing services. FAIL takes precedence over BLOCKED; QA never changes implementation or criteria. Under the user's updated workflow, per-task QA PASS proceeds to completion/integration; orchestrator requirements review is reserved for final release.

Parallel preparation may edit this isolated worktree only. Runtime QA uses an exact recorded implementation. The root application worktree's single disposable PostgreSQL test database cannot be shared by simultaneous suites; sequence them or configure a separately named disposable DB, guarded against normal database names. Never substitute SQLite for concurrency. Do not alter unrelated services/databases, reveal credentials/connection representations, print private access URLs or put generated browser/mail/profile artifacts into source. Use short tracebacks and secret-safe assertions. No external mail, deployment, push or issue-state change is authorized by these preparation documents.

## Shared synthetic fixtures and deterministic clocks

| Fixture | Definition / expected use |
| --- | --- |
| Household A | Scheduling `Europe/Warsaw`; verified parents `parent-a@example.test`, `parent-b@example.test`; children `Aster` and `Birch` with distinct generated four-character PIN strings, including a leading-zero case. Parent A opens board; B may independently unlock it. Generate credentials locally; never print them |
| Household B | Separate verified parent and child `Cedar`; use its real IDs to probe every A read/mutation boundary. No real names or family data |
| Anonymous/unverified clients | Independent browser/session contexts; test direct endpoint access as well as hidden UI. Child PIN grants submission only, never parent identity/session |
| Shared board clients | Two independent contexts/sign-in sessions, preferably different browser engines; no shared cookies or unlocked parent state. One receives mutations from the other |
| Fixed schedule dates | Monday2026-10-26, Wednesday2026-10-28, Friday2026-10-30. Daily and Monday/Wednesday schedules; approved creation date bounds avoid pre-creation work |
| Cross-timezone instant | `2026-10-28T01:00:00Z`: `America/Los_Angeles` dateOct27, `Asia/Tokyo` dateOct28. A due dateOct27 is not overdue in LA and overdue in Tokyo. Both must retain identical occurrence ID/date |
| Week boundaries | Compute Monday00:00 and next Monday00:00 using household ZoneInfo, not seven times24h. Warsaw weeks2026-03-23→30 and2026-10-19→26 span DST changes. Check immediately before/exactly at boundary |
| Controlled clocks | Server receipt/schedule/review instant is controlled in tests; browser timezone/local time handled independently. Do not simulate timeliness by trusting a user-supplied clock timestamp |
| Race harness | PostgreSQL independent connections/transactions and Barrier; release competing requests together, bound waits, close connections in finally. Check persisted invariants after both outcomes, not response status alone |

## Browser and operational evidence

For affected core journeys, record actual installed stable Chrome/Firefox versions separately from Playwright bundled versions,1280×720 and real200% browser zoom, keyboard-only control traversal, visible focus, labels, text statuses and readable validation/errors. Inspect fresh screenshots; scaling CSS or merely setting device scale factor does not establish browser zoom. Use isolated temporary profiles and ignored artifacts. Record browser/app errors separately from browser-internal diagnostics.

Run appropriate documented Django checks, migration drift, Ruff format/lint, locked sync, PostgreSQL server suites, both bundled engines, static collection and owning scheduler checks. Do not invent command selectors before implementation exists; replace scenario IDs below with real selectors/manual procedures at handoff. Verify startup/shutdown and persistence through reload/sign-out/restart where required. Logs and evidence record boolean privacy checks, not compared private values.
