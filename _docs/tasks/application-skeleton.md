# application-skeleton: Create a runnable Django application skeleton

Status: Draft
Labels: None
GitHub issue: https://github.com/Alex-Yu/done-together/issues/12
Local task: `_docs/tasks/application-skeleton.md`
Requirement links: [plan](../plan.md), REQ-021/025–027 (enabling structure, not feature completion); [architecture](../architecture.md); ADR-001–003.
Dependencies: [environment-setup](environment-setup.md) Done and integrated; current PM readiness review.

## Goal

The developer creates a minimal Django application using the validated environment, proves HTTP/PostgreSQL readiness and local HTMX delivery, and establishes verification commands before account/household features begin.

## Acceptance criteria

- [ ] AC-001: Create `manage.py`, `config/` settings/URLs/server entry points, templates/static directories and test directories following architecture.md. Use the setup task's locked dependencies. Load ignored local configuration via documented settings; tests use separate PostgreSQL and in-memory email. Configure custom parent user model before initial migrations so task 001 can implement accounts without changing an already-migrated user model. No account workflow is required here.
- [ ] AC-002: Configure PostgreSQL and apply initial migrations to the dedicated local database. Start loopback development server at `127.0.0.1:8000`; `GET /health/` returns HTTP 200 with only `{"status":"ok"}` when a database query succeeds. Database unavailability returns HTTP 503 with a generic body and no credentials or internal details. Health exposes no household information and does not mutate data.
- [ ] AC-003: `GET /` renders a provisional Done Together landing page with a heading, keyboard-accessible labeled smoke interaction and visible focus. Pinned HTMX is served locally with version/source/license recorded, loads without browser errors and successfully updates a smoke fragment. No product household/account screens or data are introduced.
- [ ] AC-004: Django system checks, migration-drift check, Ruff lint/format checks, targeted health tests, full initial server suite and Playwright Chromium/Firefox smoke tests pass using the intended commands in commands.md. Include readiness success/failure behavior and the browser interaction; no empty test selection is treated as a pass. Static collection includes HTMX. Test fixtures start/stop the live server and use isolated PostgreSQL data.
- [ ] AC-005: Start and stop web server cleanly with documented readiness/shutdown signals. commands.md records exact validated migrations, start/stop, health/landing-page smoke, asset collection, lint and test commands and observed results. Recurrence/feature commands remain UNVERIFIED. Stable Chrome/Firefox smoke plus keyboard/200% zoom observations are recorded; full feature accessibility remains task 010.

## Out of scope

Accounts/verification/invitations, shared parent/child PIN behavior, household board, chores, recurrence command/scheduler and stars belong to feature tasks 001–009. No hosting, deployment, production mail, external provider provisioning or distribution artifact is included.

## Constraints

Use the integrated environment-setup result and agreed architecture. Delivery is handed over; scaffolding begins only when setup is Done/integrated and the PM marks this task Ready. Keep the smoke interface minimal and removable as features arrive. Bind development services to loopback. Never use live household data or SQLite for database verification. No frontend build system is required.

## Verification plan

- AC-001: Inspect layout/settings/custom user migration and safe configuration loading. Confirm test database and mail backend isolation without disclosing secrets.
- AC-002: QA applies migrations and independently checks HTTP/database health, including controlled database failure using isolated test settings/fixtures. Expect 200 on success and 503 without internals on failure.
- AC-003: Inspect HTMX provenance/local asset and repeat labeled fragment interaction in browsers; check keyboard focus and browser errors.
- AC-004: QA executes documented checks/server tests/browser smoke and static collection; inspect meaningful positive/negative health coverage and nonempty suites.
- AC-005: Repeat startup/shutdown from commands.md, observe endpoint/process state, and record stable Chrome/Firefox versions, viewport/zoom and keyboard observations. Map every criterion to revision-bound evidence.

## Questions and assumptions

- PM reviewed the five criteria against selected architecture on 2026-10-28. Remains Draft until environment-setup is Done/integrated and current readiness review confirms validated prerequisites. No requirement has been marked complete by this design document.
- A minimal custom user model extends Django's supported user mechanism; account workflows and exact verification/recovery rules remain task 001.
- Hosting and production operations remain unselected and do not block this loopback skeleton.

## Handoff

- PM scope review: 2026-10-28; five criteria complete and architecture aligned; Draft pending setup integration. Full grooming commit recorded in backlog checkpoint.

- Implementation summary: Not started; architecture-stage task refinement only.
- Task branch / verified implementation commit: Pending
- Changed files / revision: Pending implementation
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: None authorized
- Checks and results: Commands intended and UNVERIFIED; no environment/application execution
- Verification record: Pending
- Orchestrator requirements re-check / evidence / outcome: Pending
- Remaining risks or blockers: Environment-setup must be Done/integrated; current PM readiness review pending.
