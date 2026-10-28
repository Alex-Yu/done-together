# Project commands

Status: INTENDED / UNVERIFIED — documented on 2026-10-28 for the selected Django + PostgreSQL + HTMX approach. None of the commands below has been executed or validated for this project. Source files, manifests, configuration, tests and custom management commands named here do not yet exist. Do not interpret these examples as evidence of a working application.

The developer executes [environment-setup](tasks/environment-setup.md) before [application-skeleton](tasks/application-skeleton.md). Each task replaces intended entries with exact observed versions, working directory, environment, expected/observed results and evidence. Feature commands remain unverified until their owning tasks implement and validate them. QA checks independently under [testing-guidelines.md](testing-guidelines.md).

## Prerequisites and configuration

Working directory for all commands: repository root `/Users/alexy/Studies/sdd-apps/done-together`, unless stated otherwise. Current intended host is macOS/zsh. Native tools are the baseline; containers are optional and require their own documented commands if adopted. Reuse compatible existing tools and services without overwriting unrelated databases/configuration. No installation is performed by this documentation change.

- Git, GitHub CLI (for later authorized issue synchronization), an editor, and network/package access.
- Homebrew if available for native installs; otherwise the developer chooses a supported project-local installation method and records it before execution. Do not run a remote bootstrap script blindly or assume administrative access.
- uv; managed Python 3.13; PostgreSQL 17 server/client tools; Mailpit; current stable Chrome and Firefox. Exact patches, tool versions and paths are captured during setup.
- Runtime packages: Django `>=5.2,<5.3`, django-allauth, psycopg with binary distribution, argon2-cffi, and python-dotenv. Development packages: pytest, pytest-django, pytest-playwright, Ruff. Lock exact resolved versions in `uv.lock`; pin the Python minor version. HTMX is a pinned locally served asset added during the skeleton task, with source/version/license recorded.
- Do not add Node.js, Redis, Celery, a paid service or external mail provider for local bootstrap.

Create an ignored `.env` locally and a committed `.env.example` containing placeholders only during environment setup. The skeleton implements settings that load these variables; pytest uses explicit test settings. Never print `.env` or credentials in evidence. Intended names:

| Variable | Purpose / safe local convention |
| --- | --- |
| `DJANGO_SETTINGS_MODULE` | `config.settings.local`; tests use `config.settings.test` |
| `DJANGO_SECRET_KEY`, `PIN_HASH_PEPPER` | Independently generated local secrets, no committed values |
| `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` | Local debug only; loopback hosts (`127.0.0.1,localhost`) |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Dedicated local database/role; loopback, normally port 5432; no real data |
| `TEST_DB_NAME` | Separate disposable `test_done_together` database; never point tests at normal application data |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` | Loopback Mailpit, port 1025, local TLS off |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Empty for local Mailpit; future provider credentials remain unselected |
| `DEFAULT_FROM_EMAIL`, `APP_BASE_URL` | Synthetic sender under `.test`; `http://127.0.0.1:8000` |

The local database role may create its isolated test database; it must not be a database superuser. Production roles/privileges are a separate operational decision. PostgreSQL clients use a protected local password file or interactive prompt, never passwords in shell arguments. Keep Mailpit UI/SMTP and PostgreSQL bound to loopback. Ignore `.env`, `.venv/`, local database/mail data, browser traces and generated private artifacts; never ignore `.env.example` or the dependency lockfile. Synthetic automated email tests use Django's in-memory backend; only local capture checks use Mailpit.

## Environment setup commands — all UNVERIFIED

Execute in the numbered order; these are intended operations, not a shell script to run wholesale. Inspect existing installations/ports first, and stop rather than replace unrelated resources.

| Order / operation | Intended command | Expected result / owner |
| --- | --- | --- |
| 1. Inspect tools | `git --version`, `gh --version`, `brew --version`, `uv --version`, `psql --version`, `mailpit --version` (separate commands) | Record present/missing tools without treating missing probes as passing; environment-setup |
| 2. Install missing native tools | `brew install uv postgresql@17 mailpit` | Only missing packages, if Homebrew is available and installation access permits; environment-setup |
| 3. Select PostgreSQL clients | `export PATH="$(brew --prefix postgresql@17)/bin:$PATH"` | Intended for this shell; record persistent/project invocation instructions without modifying unrelated shell configuration |
| 4. Python | `uv python install 3.13` | Managed compatible Python available |
| 5. Dependency manifest | `uv init --bare --python 3.13` | Create metadata only after inspecting existing files; do not create Django application source |
| 6. Runtime dependencies | `uv add 'Django>=5.2,<5.3' django-allauth 'psycopg[binary]' argon2-cffi python-dotenv` | Compatible resolution and lockfile; record exact versions |
| 7. Development dependencies | `uv add --dev pytest pytest-django pytest-playwright ruff` | Locked test and analysis tools |
| 8. Reproduce dependencies | `uv sync --locked` | Lockfile resolves and isolated environment installs |
| 9. Browser automation | `uv run playwright install chromium firefox` | Automated browser binaries installed; stable Chrome/Firefox are separate local browser prerequisites |
| 10. Start database | `brew services start postgresql@17` | Reuse an existing compatible server if present; inspect port conflicts before starting |
| 11. Create dedicated role | `createuser --createdb --pwprompt done_together` | Local administrator connection required; role is not superuser; omit creation if already safely configured |
| 12. Create database | `createdb --owner=done_together done_together` | Dedicated application database created from local administrator connection; do not overwrite an existing database |
| 13. Check database | `pg_isready -h 127.0.0.1 -p 5432` then `psql -h 127.0.0.1 -U done_together -d done_together -c 'SELECT 1;'` | Server reachable AND application-role authentication/query succeeds; passwords only via prompt/protected password file |
| 14. Start mail capture | `mailpit --listen 127.0.0.1:8025 --smtp 127.0.0.1:1025` | Foreground process in separate terminal; no external delivery; Ctrl-C stops it |
| 15. Inspect mail capture | `curl --fail http://127.0.0.1:8025/` | UI reachable; developer additionally sends a synthetic SMTP message to port 1025 and verifies receipt in UI |
| 16. Runtime compatibility | `uv run python --version` and `uv run python -c 'import django, allauth, psycopg, argon2, dotenv; print(django.get_version())'` | Required imports succeed; versions recorded without application scaffolding |

Install current stable Chrome and Firefox only if absent, using their official distributions and needed permissions. Record actual versions. Homebrew/service/role operations may need specific access; the developer requests only missing access when encountered. If native installation is unsuitable, record an equivalent supported alternative before executing it. Do not report the table as validated merely because upstream documentation describes these tools.

## Application commands — all UNVERIFIED

These commands become available only after the owning tasks create their referenced files. The developer must document actual exit codes, URLs, readiness signals and shutdown observations.

| Operation | Intended command | Expected behavior / validation owner |
| --- | --- | --- |
| Install from committed lockfile | `uv sync --locked` | Reproduce environment without changing lock; environment-setup, then skeleton |
| Migrate local database | `uv run python manage.py migrate` | Migrations apply to dedicated local PostgreSQL; application-skeleton initially, affected feature tasks later |
| Start local web server | `uv run python manage.py runserver 127.0.0.1:8000` | Loopback HTTP server, no startup errors; keep foreground; application-skeleton |
| HTTP/database smoke | `curl --fail http://127.0.0.1:8000/health/` | HTTP 200 and minimal `{"status":"ok"}` only when a database query succeeds; database failure returns 503 without internals; application-skeleton |
| Browser smoke | Open `http://127.0.0.1:8000/` | Accessible provisional Done Together landing page, local HTMX asset loads, no household data or browser errors; application-skeleton |
| Stop web server | Ctrl-C in its terminal | Process exits cleanly, endpoint no longer responds; application-skeleton |
| Stop database started for this project | `brew services stop postgresql@17` | Only when not shared with other work; environment-setup |
| Static assets | `uv run python manage.py collectstatic --noinput` | Builds local collected static directory including pinned HTMX; application-skeleton. Output directory is ignored |
| Package / frontend build | Not applicable to initial local delivery | Run application source with locked dependencies; no distributable package, Node build or deployment artifact selected |
| Django checks | `uv run python manage.py check` | No system-check errors; application-skeleton onward |
| Migration drift | `uv run python manage.py makemigrations --check --dry-run` | No model changes missing migrations; application-skeleton onward |
| Formatting | `uv run ruff format --check .` | No formatting changes required; application-skeleton onward |
| Static analysis | `uv run ruff check .` | No configured lint errors; application-skeleton onward |
| Targeted tests | `uv run pytest tests/integration/test_health.py -q` | Positive readiness and database-failure behavior; application-skeleton creates this test |
| Select feature tests | `uv run pytest tests/integration/ -k approval -q` | Example future selector; task 007 must supply real approval tests, not an empty passing selection |
| Full server tests | `uv run pytest tests/unit tests/integration -q` | Isolated PostgreSQL test database; in-memory mail; concurrency tests use independent transactions; skeleton initializes suite, features extend it |
| Browser tests | `uv run pytest tests/e2e --browser chromium --browser firefox -q` | Live test server with synthetic fixtures and isolated database; skeleton configures fixture and smoke journey, features extend it |
| Recurrence once | `uv run python manage.py reconcile_recurrence --once` | Idempotent catch-up; implemented/validated by task 006, not bootstrap |
| Local independent scheduler | `uv run python manage.py reconcile_recurrence --loop --interval 60` | Separate foreground process; no browser needed; Ctrl-C stops it; task 006 defines safe loop/retry behavior |

Custom command names and flags are intended contracts to implement in task 006, not existing Django commands. Production scheduling must use a supervised process or equivalent platform scheduler chosen in an explicit operational task.

## Acceptance and verification procedures — all UNVERIFIED

- Environment setup: record exact tools, import success, application-role PostgreSQL query and synthetic SMTP capture; inspect ignored files and staged examples for secrets. No Django startup result is expected yet.
- Skeleton: start from documented prerequisites, migrate, start web server, verify health and landing page, load local HTMX, run checks/lint/tests/static collection, stop cleanly. Exercise health failure on an isolated test database/connection, not by disrupting an unrelated server.
- Feature verification: map all criteria to evidence. Use synthetic accounts/children and isolated PostgreSQL data. Exercise five-failure/five-minute identity limits across sessions, one-hour account links, seven-day single-use invitations, parent timeout and unauthorized direct requests.
- Recurrence/integrity: competing approvals award one star; overlapping schedulers and approval generate one eligible occurrence; test deleted/edited definitions, late approvals, timezone/DST changes in calendar interpretation and Monday week boundaries. Stop browser sessions to prove scheduler independence.
- Synchronization/offline: two independent browser contexts/computers observe accepted changes within five seconds under normal connectivity. Disconnect one, preserve displayed data, disable mutations, reconnect and refresh before enabling them; test lost mutation responses and stale revisions. Polling must not extend parent authority or discard form input/focus.
- Accessibility/browser release gate: current stable Chrome and Firefox, 1280×720 minimum, keyboard navigation, visible focus, labeled inputs, status text and 200% zoom. Record versions and manual observations; automated bundled Firefox does not certify stable Firefox.

Record procedures, actual results and exact revision in `_docs/verification/` using the verification template. A missing command/service/test or unavailable browser yields BLOCKED for its affected criterion, never PASS. No application checks have run at this architecture stage.

## Upstream references

Intended syntax/prerequisites were checked against [uv projects](https://docs.astral.sh/uv/guides/projects/), [Homebrew PostgreSQL 17](https://formulae.brew.sh/formula/postgresql@17), [Mailpit installation](https://mailpit.axllent.org/docs/install/), and [Playwright browsers](https://playwright.dev/python/docs/browsers). These sources do not validate the local environment or future project commands.
