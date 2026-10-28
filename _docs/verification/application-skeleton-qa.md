# Verification: application-skeleton — attempt 1

Overall verdict: PASS
Task / specification: [application-skeleton](../tasks/application-skeleton.md), [commands](../commands.md)
Revision or exact working-tree state: implementation `f663bfe2149500d13516c1d82d924c3fb0a87185` on `task/application-skeleton`, reviewed at `da17dd05d5f1187b591203c69f1ab02b3aa1a95b`. Exact diff between them changes only recorded hashes in task/checkpoint/developer evidence; no implementation changes.
Reviewer / independence: Separate QA subagent; no implementation fixes.
Environment: macOS x86_64; uv0.12.19/Python3.13.15/Django5.2.18/PostgreSQL17.11; locked dependencies; bundled Chromium/Firefox and installed stable Chrome156.0.8078.48/Firefox159.0.
Date: 2026-10-28

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | Inspect config/settings, entrypoints, initial accounts migration, URLs and tests; run configuration/server suite and migration/drift checks | Agreed structure, custom parent identity before initial migration, safe separate PostgreSQL tests/in-memory email, no account workflow | accounts.User extends AbstractUser, unique email and initial migration; AUTH_USER_MODEL configured. Environment secrets required, local dotenv loaded; test settings reject equal/non-test_/missing test names before DB operations. All configuration tests pass. Only landing/health/smoke URLs; account workflows absent | PASS |
| AC-002 | Replay migration; real loopback server and HTTP health; run all4 health tests and inspect SELECT1/failure behavior | Minimal200 only with successful DB query; generic503 on DB failure; no mutation/private data | Migrations exit0/idempotent. Live GET /health/ returns200, only status=ok, no-store. Query-count test executes exactly1 SELECT. Deterministic DB exception and real isolated closed-port PostgreSQL connection return503/status unavailable without internals; no database service disrupted | PASS |
| AC-003 | Inspect templates/CSS/local asset/license; bundled browser Tab/Enter tests; independent installed stable helper and four screenshot inspections | Heading, labeled keyboard interaction, visible focus, local pinned HTMX updates fragment without application errors | Local HTMX2.0.11 hash matches official docs; collected bytes identical; Zero-Clause BSD source/license recorded. Both engines render heading and focus outlined Check connection; Enter updates live status. No product data/screens. Browser suites pass, four fresh stable screenshots visually readable and no horizontal clipping | PASS |
| AC-004 | Independently execute locked sync, migrations/check/drift, Ruff format/lint, targeted/full/browser tests and collectstatic | All applicable nonempty required checks pass with isolated real PostgreSQL/live server | All exit0: health4, server11, bundled browsers2. System checks0 issues, no migration drift;60 files already formatted; lint clean. collectstatic5 unchanged files including local HTMX. Fixture starts/stops loopback live server with transactional test DB, safely scopes Playwright lifetime without async bypass | PASS |
| AC-005 | Run documented foreground server; HTTP/readiness; installed stable native100/200% keyboard/HTMX helper; SIGINT then endpoint probes; inspect commands | Repeatable startup/shutdown and browser observations; future commands UNVERIFIED | Server starts Django5.2.18/config.settings.local on127.0.0.1:8000. Stable Chrome156/Firefox159 pass native100/200; detailed metrics below. Server and driver stop exit0; endpoint probes fail connection as expected. Commands match successful replay; feature/scheduler entries explicitly UNVERIFIED | PASS |

## Required checks

Working directory: `/Users/alexy/Studies/sdd-apps/done-together`. Used documented `UV_CACHE_DIR="$PWD/.local/uv-cache"`, `PLAYWRIGHT_BROWSERS_PATH="$PWD/.local/playwright"`; local dotenv supplied credentials without printing them. PostgreSQL/process/browser operations used authorized sandbox escalation where required.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `uv sync --locked` | Exit0 | Resolved28/checked25 packages; dependency lock unchanged from integrated setup |
| `uv run python manage.py migrate` | Exit0 | accounts/auth/contenttypes/sessions migrations already applied; replay idempotent |
| `uv run python manage.py check` | Exit0 |0 issues |
| `uv run python manage.py makemigrations --check --dry-run` | Exit0 | No changes detected |
| `uv run ruff format --check .` | Exit0 |60 files already formatted |
| `uv run ruff check .` | Exit0 | All checks passed |
| `uv run pytest tests/integration/test_health.py -q` | Exit0 |4 passed in0.60s; success/exception/real connection failure/CSRF+method checks |
| `uv run pytest tests/unit tests/integration -q` | Exit0 |11 passed in1.36s; includes isolated PostgreSQL/in-memory email, unsafe test DB name rejection and missing secrets even in DEBUG |
| `uv run pytest tests/e2e --browser chromium --browser firefox -q` | Exit0 |2 passed in7.46s; local asset, heading, keyboard, focus, HTMX status, no console/script errors |
| `uv run python manage.py collectstatic --noinput` | Exit0 |0 copied/5 unchanged; collected HTMX identical to source |
| HTMX SHA384 calculation | PASS | `2OatzQy1H+Zd/IIrjr1TcuDGqLXeHhbooAyJY1KdQMKnr4LZ22k31GBLdYKHmVjg` matches [official installation docs](https://htmx.org/docs/#installing); bundled [license](https://raw.githubusercontent.com/bigskysoftware/htmx/v2.0.11/LICENSE) matches source |
| `PYTHONUNBUFFERED=1 uv run python manage.py runserver 127.0.0.1:8000 --noreload` | Started successfully | Readiness no system errors, Django5.2.18/local settings; loopback listener only |
| `curl --fail -i http://127.0.0.1:8000/health/` | Exit0 | HTTP200, body only `{"status": "ok"}`, no-store/private headers |
| `.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error` then `uv run python tools/verify_skeleton_browsers.py` | Helper exit0 | Installed Chrome156.0.8078.48/Firefox159.0; keyboard/focus/HTMX pass at both native zoom levels |
| Native zoom metrics | PASS | Both browsers100%:1280×720 CSS viewport,DPR1;200%:640×360,DPR2; overflow=false. Helper uses actual Chrome Page zoom and Firefox fullZoom, separate temporary profiles |
| Fresh screenshots visually inspected | PASS | `.local/skeleton-{chrome,firefox}-{100,200}.png` ignored. At100% heading/instructions/button/status readable; at200% text wraps, Tab scrolls focused button into view, outlined button/status usable with normal vertical scrolling; no horizontal clipping/overlap |
| SIGINT to QA-owned webserverPID67801/driverPID67806 | Both exit0 | Both process sessions completed; subsequent curl8000/health and4445/status each exit7/connection refused |
| `git diff --check` | Exit0 | No whitespace errors |

## Findings

None affecting criteria. Installed Firefox driver stderr reports browser-internal compositor/remote-experiment warnings during startup/shutdown; bundled Firefox application console/script checks pass and installed-browser behavior/visual checks pass. These messages originate in browser internal resource paths, not application scripts.

No account/household behavior or full-release accessibility is claimed by this provisional skeleton. Those remain linked feature/release tasks.

## Verdict rationale

PASS for all five criteria at the exact implementation commit. Task remains In review pending orchestrator requirement re-check and integration. Skeleton attempt1/3; setup attempts2/3 retained; batch completions1/10. QA changed evidence/status only. PG17 remains running on55432; QA webserver/geckodriver stopped. No external email, deployment, merge or push.
