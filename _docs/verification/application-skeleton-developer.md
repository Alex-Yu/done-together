# Developer evidence: application-skeleton

Overall verdict: PENDING — independent QA required.
Task / specification: [application-skeleton](../tasks/application-skeleton.md), [commands](../commands.md).
Revision: `f663bfe2149500d13516c1d82d924c3fb0a87185` on `task/application-skeleton`; subsequent record-only handoff commit changes no implementation.
Reviewer / independence: Developer self-check; not independent QA.
Environment: macOS x86_64, uv0.12.19, Python3.13.15/Django5.2.18/PostgreSQL17.11, locked dependencies; installed Chrome156.0.8078.48, Firefox159.0; bundled Chromium156.0.8078.4 and Firefox157.
Date:2026-10-28

## Acceptance evidence

| Criterion | Executed procedure | Observed | QA verdict |
| --- | --- | --- | --- |
| AC-001 | Inspect config/base/local/test, accounts.User initial migration; run migration, PostgreSQL/in-memory email safety tests | Custom parent model installed before initial migration; .env required secrets loaded, test DB guard rejects equal/non-test names before connection; no account workflows | PENDING |
| AC-002 | Migrate; run loopback server; curl /health; test actual SELECT1 and real closed-port connection failure plus deterministic exception | Migration exit0; HTTP200 minimal status; controlled failures generic503 with no internal details; readiness does not mutate data | PENDING |
| AC-003 | Local HTMX2.0.11 integrity/provenance/license check; bundled Chromium+Firefox Tab/Enter/local asset/error checks; inspect stable screenshots | Heading, labeled button, visible focus and live status; local HTMX POST+CSRF fragment update, no application browser errors; no product data/screens | PENDING |
| AC-004 | Django checks/migration drift; Ruff lint/format; targeted health, full server and dual-browser suites; collectstatic | All exit0; targeted4 passed, server11 passed, browsers2 passed; five static files including HTMX; isolated PostgreSQL live server and teardown | PENDING |
| AC-005 | Foreground runserver readiness; HTTP health; Ctrl-C; stopped endpoint; installed stable browser helper/nativezoom screenshots | Server startup successful and shutdown exit0/refused endpoint; both stable browsers native100/200% keyboard/focus/HTMX/no horizontal overflow; screenshots inspected | PENDING |

## Required checks

All commands are reproduced in commands.md. `uv sync --locked`, migrate, check, makemigrations --check --dry-run, ruff check and ruff format --check exit0. Targeted `tests/integration/test_health.py`:4 passed. Full `tests/unit tests/integration`:11 passed. `tests/e2e --browser chromium --browser firefox`:2 passed. collectstatic includes five files. Health200 only status; real isolated closed-port PostgreSQL failure returns503 without connection details. Configuration subprocesses reject equal test_/test_ DB names and missing secrets even with DEBUGTrue. No SQLite or async-safety bypass.

Tracked helper `tools/verify_skeleton_browsers.py` drives installed Chrome native Page zoom setting and installed Firefox native fullZoom using official project-local geckodriver0.37.1/standard WebDriver HTTP. At100% both1280×720,DPR1;200% both640×360,DPR2. Tab focuses outlined button, Enter updates live status, no horizontal overflow. Ignored viewport screenshots `.local/skeleton-{chrome,firefox}-{100,200}.png` visually inspected for readable text/focus and normal scrolling to the interaction. Browser sessions/profiles closed.

## Findings and resolved implementation checks

Initial configuration test compared Django's active test DB name after runner substitution; corrected to compare against configured application DB. Initial pytest-playwright session event loop surrounded Django DB setup and failed with SynchronousOnlyOperation; scoped page fixture now creates/stops Playwright within transactional_db lifetime, all browser tests pass without disabling Django protection. Stable Chrome native settings require a persistent isolated profile. Initial installed Firefox launch returned500 while its existing installation applied a pending update from158→159; retry succeeded, final checks use159. Browser-internal Firefox experiments/compositor warnings remain in driver stderr, distinct from application JS. Empty favicon produced browser parser noise; replaced by valid local SVG favicon and affected browser checks repeated.

## Services and artifacts

Project PostgreSQL17 remains running on127.0.0.1:55432; unrelated PostgreSQL13 on5432 preserved. Developer web server and geckodriver stopped cleanly; no account emails or external delivery. Screenshot/profiles/downloads/logs remain ignored .local. Feature/scheduler commands explicitly UNVERIFIED.

## Verdict rationale

Implementation evidence covers five criteria. Independent QA must replay checks at the recorded implementation commit; no Done/merge claimed.
