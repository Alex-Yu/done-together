# environment-setup: Set up the Django development environment

Status: Draft
Labels: `environment-setup`
GitHub issue: Not yet published; pending authorized backlog synchronization before delivery.
Requirement links: [plan](../plan.md), REQ-001/007/021/025–027 (enabling infrastructure, not feature completion); [architecture](../architecture.md); ADR-001–003.
Dependencies: User selected Django + PostgreSQL + HTMX on 2026-10-28; PM readiness review and backlog synchronization still required.

## Goal

The developer installs and configures a reproducible local Python/Django toolchain, dedicated PostgreSQL database, browser test tools and local mail capture before creating application source. The user need not perform routine installation/configuration manually.

## Acceptance criteria

- [ ] AC-001: Inspect the macOS environment and existing services, record actual versions/paths, and install only missing compatible prerequisites: uv, Python 3.13, PostgreSQL 17 clients/server, Mailpit, Git/GitHub CLI and stable Chrome/Firefox. Required access failures are recorded; unrelated services/data remain intact.
- [ ] AC-002: Create metadata/dependency files only (`pyproject.toml`, `.python-version`, `uv.lock`), resolve the runtime/dev package set in commands.md, and reproduce it with `uv sync --locked`. Python/Django versions and required package imports succeed. No Django project, app source, settings, manage.py or templates are created in this task.
- [ ] AC-003: Configure a dedicated loopback PostgreSQL database and non-superuser application role with isolated test-database creation rights. An authenticated application-role `SELECT 1` succeeds. Test database naming cannot target application data; no SQLite substitute is used.
- [ ] AC-004: Run loopback-only Mailpit, send a synthetic SMTP message to port 1025 using a repeatable documented procedure and observe it in the UI on port 8025. Confirm no external mail delivery is configured. Record startup/shutdown and any process left running.
- [ ] AC-005: Create ignored local `.env` values and a placeholder-only `.env.example` for the variable names in commands.md, including generated independent Django/PIN secrets. Ignore local credentials, mail data, environments and private artifacts while tracking examples and lockfiles. Evidence does not expose secrets. Application settings consumption is deferred to the skeleton.
- [ ] AC-006: Install Playwright Chromium/Firefox binaries and record executable availability, plus versions of the separate stable Chrome/Firefox installations. Ruff and pytest execute their version probes successfully. No application tests are claimed before source exists.
- [ ] AC-007: Replace the applicable environment command entries in commands.md with exact validated instructions, versions, working directory, prerequisites, expected/observed results and a reproducible synthetic SMTP capture procedure. Leave skeleton/feature commands explicitly UNVERIFIED. Independent QA maps evidence to AC-001–007.

## Out of scope

Django scaffolding, application settings implementation, server startup and HTTP smoke checks belong to [application-skeleton](application-skeleton.md). Product features, external email, production hosting, deployment, backups and paid provisioning are excluded. No application code is requested at architecture-recording time.

## Constraints

Follow [architecture](../architecture.md) and [commands](../commands.md). Native macOS/Homebrew installation is the intended path if available; prefer existing compatible tools and record an equivalent supported method if necessary. Inspect existing files before initializing metadata. Do not overwrite unrelated configuration or databases. Ask only for specific missing access/permissions when executing setup. Dependency patches are locked after compatibility checks; material stack changes require user agreement. Keep the environment-only/skeleton boundary intact.

## Verification plan

- AC-001: Compare recorded inventory/version probes and installation evidence against prerequisites; inspect local service bindings and preservation of existing resources.
- AC-002: QA independently runs `uv sync --locked`, version/import probes from commands.md; inspect metadata/lockfile and absence of application source. Expect successful imports with unchanged locked dependencies.
- AC-003: QA runs server readiness and authenticated `SELECT 1`, inspects role privileges/test database separation using safe queries, and records results without passwords.
- AC-004: QA repeats documented synthetic SMTP capture and observes matching synthetic message in Mailpit. Verify loopback binding and no relay; stop the task's mail process cleanly.
- AC-005: Inspect examples, ignore behavior and tracked files; confirm no local secrets/data enter source or evidence, without printing secret values.
- AC-006: Run pytest/Ruff version probes and verify browser binaries and stable browser version records.
- AC-007: Follow environment instructions from the recorded working directory; map each result to the criterion in a verification record. Missing installation, access or checks block completion.

## Questions and assumptions

- Architecture is selected; implementation has not begun. This refined task stays Draft until PM readiness review, authorized issue publication/reconciliation and delivery handover.
- Python 3.13/PostgreSQL 17 and native macOS tools are intended implementation defaults, not verified installations. Installation permissions are determined during execution.
- No production credentials or hosting choice is needed for isolated local setup. Production decisions remain open for later affected work.

## Handoff

- Implementation summary: Not started; architecture-stage task refinement only.
- Task branch / verified implementation commit: Pending
- Changed files / revision: Pending implementation
- Final branch tip / delivery commit / integration results: Pending
- Push status / authorized remote and branch targets: None authorized
- Checks and results: Commands intended and UNVERIFIED; no environment/application execution
- Verification record: Pending
- Orchestrator requirements re-check / evidence / outcome: Pending
- Remaining risks or blockers: PM readiness review and authorized backlog publication pending; delivery not handed over.
