# Project commands

Status: Environment setup executed by developer on 2026-10-28; independent QA pending. Application skeleton and feature commands remain UNVERIFIED. Environment metadata/configuration exists; application source and tests do not yet exist.

The developer executes [environment-setup](tasks/environment-setup.md) before [application-skeleton](tasks/application-skeleton.md). Each task replaces intended entries with exact observed versions, working directory, environment, expected/observed results and evidence. Feature commands remain unverified until their owning tasks implement and validate them. QA checks independently under [testing-guidelines.md](testing-guidelines.md).

## Prerequisites and configuration

Working directory for all commands: repository root `/Users/alexy/Studies/sdd-apps/done-together`, unless stated otherwise. Current intended host is macOS/zsh. Native tools are the baseline; containers are optional and require their own documented commands if adopted. Reuse compatible existing tools and services without overwriting unrelated databases/configuration. Project-owned setup installation is recorded below.

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
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Dedicated local database/role; loopback port55432 (preserves unrelated PostgreSQL13 on5432); no real data |
| `TEST_DB_NAME` | Separate disposable `test_done_together` database; never point tests at normal application data |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` | Loopback Mailpit, port 1025, local TLS off |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Empty for local Mailpit; future provider credentials remain unselected |
| `DEFAULT_FROM_EMAIL`, `APP_BASE_URL` | Synthetic sender under `.test`; `http://127.0.0.1:8000` |

The local database role may create its isolated test database; it must not be a database superuser. Production roles/privileges are a separate operational decision. PostgreSQL clients use a protected local password file or interactive prompt, never passwords in shell arguments. Keep Mailpit UI/SMTP and PostgreSQL bound to loopback. Ignore `.env`, `.venv/`, local database/mail data, browser traces and generated private artifacts; never ignore `.env.example` or the dependency lockfile. Synthetic automated email tests use Django's in-memory backend; only local capture checks use Mailpit.

## Environment setup commands — developer validated, independent QA pending

Validated on 2026-10-28 on macOS x86_64 using Apple clang 21.0.0/GNU Make 3.81. Existing PostgreSQL 13.23 (Postgres.app, PID 858 at inventory) on 5432 is unrelated and remains untouched. Homebrew 7.0.11 has no Intel bottles for the selected PostgreSQL/Mailpit; its Mailpit source build would add Node. The supported project-local source/static-binary methods below avoid global installation and new build dependencies. All `.local/` contents are ignored.

Observed tools: uv 0.12.19 (`/Library/Frameworks/Python.framework/Versions/3.14/bin/uv`), managed Python 3.13.15 (`~/.local/share/uv/python/cpython-3.13.15-macos-x86_64-none/bin/python3.13`), Git 2.56.0 (`/opt/local/bin/git`), GitHub CLI 2.103.3 (`~/.local/bin/gh`), Chrome 156.0.8078.48 and stable Firefox 158.0 in `/Applications`. Playwright 1.64.1 separately installs Chromium 156.0.8078.4/build1248 and Firefox157/build1555. Runtime lock: Django5.2.18, django-allauth65.21.0, psycopg3.3.6, argon2-cffi25.1.0, python-dotenv1.2.4; pytest9.2.0, pytest-django4.14.0, pytest-playwright0.10.0, Ruff0.17.3. Full transitive versions are in `uv.lock`.

Run from repository root. These exports do not modify shell startup files:

```sh
export UV_CACHE_DIR="$PWD/.local/uv-cache"
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.local/playwright"
export PATH="$PWD/.local/postgresql/bin:$PWD/.local/bin:$PATH"
export PGPASSFILE="$PWD/.local/pgpass"
```

Metadata was initialized using `uv init --bare --python 3.13`, runtime packages added with `uv add 'Django>=5.2,<5.3' django-allauth 'psycopg[binary]' argon2-cffi python-dotenv`, and development packages with `uv add --dev pytest pytest-django pytest-playwright ruff`. `.python-version` pins3.13 and `requires-python` bounds3.13. Do not repeat initialization on an existing checkout. Reproduction and probes:

```sh
uv sync --locked
uv run python --version
uv run python -c 'import django, allauth, psycopg, argon2, dotenv; print(django.get_version())'
uv run pytest --version
uv run ruff --version
uv run playwright install chromium firefox
```

All above returned0; imports succeeded, no application tests were run. Browser executable paths exist under `.local/playwright/`. Existing system Python/shims are unchanged; the pre-existing pyenv shim does not provide3.13, so invoke Python through `uv run python` in this checkout. Sandbox execution may require access for network/processes; a default uv cache probe failed before redirecting `UV_CACHE_DIR`, and sandbox GitHub reads failed before authorized escalated execution.

### Project-local PostgreSQL17 installation

Prerequisites: existing C compiler, make, tar, curl, SDK and compression headers. Official source and supported [Autoconf installation](https://www.postgresql.org/docs/17/install-make.html), no bootstrap scripts:

```sh
mkdir -p .local/downloads
curl --fail --location --output .local/downloads/postgresql-17.11.tar.bz2 https://ftp.postgresql.org/pub/source/v17.11/postgresql-17.11.tar.bz2
shasum -a 256 .local/downloads/postgresql-17.11.tar.bz2
# Expected dd27f2b3c59e73ed14aa3324901242bf69a032a6347805f274e6260322d42979; stop on mismatch.
tar -xjf .local/downloads/postgresql-17.11.tar.bz2 -C .local
cd .local/postgresql-17.11
./configure --prefix=/Users/alexy/Studies/sdd-apps/done-together/.local/postgresql --without-icu --without-readline
make -j4
make install
cd ../..
```

The developer verified the SHA256 before extraction/build. `--without-icu`/`--without-readline` omit optional collation/interactive editing dependencies; libc UTF-8 and standard server features remain. This does not alter required transaction/scheduling semantics. Build/configure/install logs are ignored `.local/postgresql-*.log`. No Homebrew service is started, no global PostgreSQL configuration is edited.

A project-owned cluster `.local/pgdata` uses127.0.0.1:55432, separate ignored socket directory, SCRAM password authentication for TCP/local access and an isolated bootstrap administrator. `.local/pgpass` is0600 and contains generated credentials; never display it. `.env` is0600 and contains independently generated Django/PIN secrets and application DB password. Generate replacements by copying `.env.example` then replacing each secret separately with `secrets.token_urlsafe` inside a local Python process; never pass secrets as shell command arguments. For a new checkout only, create credentials without displaying them (stop if `.env` or cluster already exists):

```sh
uv run python - <<'PYSETUP'
from pathlib import Path
import secrets
p = Path('.env')
assert not p.exists()
text = Path('.env.example').read_text()
for _ in range(3):
    text = text.replace('replace-with-generated-local-secret', secrets.token_urlsafe(64), 1)
p.write_text(text)
p.chmod(0o600)
p = Path('.local/pgadmin-password')
assert not p.exists()
p.write_text(secrets.token_urlsafe(40) + '\n')
p.chmod(0o600)
PYSETUP
```

Initial cluster creation was:

```sh
mkdir -p .local/pgsocket
initdb -D .local/pgdata --username=done_together_admin --pwfile=.local/pgadmin-password --auth-local=scram-sha-256 --auth-host=scram-sha-256 --encoding=UTF8 --locale=C
# .local/pgadmin-password is a generated0600 file, never committed.
```

The cluster's `postgresql.conf` sets `listen_addresses='127.0.0.1'`, `port=55432` and `unix_socket_directories` to the absolute `.local/pgsocket` path. Role `done_together` has LOGIN/CREATEDB/NOSUPERUSER/NOCREATEROLE/NOREPLICATION and owns only dedicated `done_together`; `test_done_together` is the separately named disposable test DB. Skeleton settings must reject equal normal/test database names.

After `initdb`, append the three documented configuration settings and start the cluster. Provision the role/database once using this secret-safe procedure; no SQL/password is echoed:

```sh
uv run python - <<'PYSETUP'
from pathlib import Path
from dotenv import dotenv_values
import psycopg
from psycopg import sql
v = dotenv_values('.env')
admin = Path('.local/pgadmin-password').read_text().strip()
with psycopg.connect(host='127.0.0.1', port=55432, user='done_together_admin', password=admin, dbname='postgres', autocommit=True) as c:
    c.execute(sql.SQL('CREATE ROLE {} LOGIN CREATEDB NOSUPERUSER NOCREATEROLE NOREPLICATION PASSWORD {}').format(sql.Identifier(v['DB_USER']), sql.Literal(v['DB_PASSWORD'])))
    c.execute(sql.SQL('CREATE DATABASE {} OWNER {}').format(sql.Identifier(v['DB_NAME']), sql.Identifier(v['DB_USER'])))
p = Path('.local/pgpass')
p.write_text(f"127.0.0.1:55432:*:done_together_admin:{admin}\n127.0.0.1:55432:*:{v['DB_USER']}:{v['DB_PASSWORD']}\n")
p.chmod(0o600)
PYSETUP
```

Developer results: configure/build/install all exit0, `postgres`/`psql`17.11, server readiness exit0 and application-role `SELECT1` returned1. Privilege query returned `done_together,false,true,false`. Creating and removing only disposable `test_done_together` succeeded with application-role rights. The app database remains. Project cluster stop/start both exit0; it is left running on127.0.0.1:55432 for QA. Existing PostgreSQL13 PID858/listeners on5432 remained unchanged. Initial provisioning used psycopg secrets from ignored files and never displayed SQL/passwords.

Start/readiness/query/privilege/stop procedures:

```sh
pg_ctl -D .local/pgdata -l .local/postgresql-server.log start
pg_isready -h 127.0.0.1 -p 55432
psql -h 127.0.0.1 -p 55432 -U done_together -d done_together -c 'SELECT 1;'
psql -h 127.0.0.1 -p 55432 -U done_together -d done_together -c 'SELECT current_user, rolsuper, rolcreatedb, rolcreaterole FROM pg_roles WHERE rolname=current_user;'
# Only stop this project-owned cluster:
pg_ctl -D .local/pgdata stop -m fast
```

### Project-local Mailpit and repeatable synthetic capture

Downloaded official [static binary](https://mailpit.axllent.org/docs/install/) with matching GitHub release SHA256 asset digest. No SMTP relay/forwarding options or external credentials are configured.

```sh
mkdir -p .local/downloads .local/bin
curl --fail --location --output .local/downloads/mailpit-darwin-amd64.tar.gz https://github.com/axllent/mailpit/releases/download/v1.32.0/mailpit-darwin-amd64.tar.gz
shasum -a 256 .local/downloads/mailpit-darwin-amd64.tar.gz
# Expected d7f3d0964cd2ea4c2a7d10660a12e02876718e67d88ced390d9cd90350a453da; stop on mismatch.
tar -xzf .local/downloads/mailpit-darwin-amd64.tar.gz -C .local/bin
mailpit version --no-release-check
mailpit --listen 127.0.0.1:8025 --smtp 127.0.0.1:1025 --database .local/mailpit.db --disable-version-check --smtp-disable-rdns --block-remote-css-and-fonts
```

Version output isv1.32.0 compiled with go1.27.3, darwin/amd64. `mailpit --version` is unsupported (exit1); use `mailpit version --no-release-check` (exit0 without network; suppresses the online release lookup). Leave capture foreground in separate terminal; readiness logs show both loopback listeners. In another terminal with exports above:

```sh
uv run python - <<'PY'
from email.message import EmailMessage
import smtplib
message = EmailMessage()
message['From'] = 'setup@example.test'
message['To'] = 'capture@example.test'
message['Subject'] = 'Done Together setup synthetic capture'
message.set_content('Synthetic setup verification only; no personal data.')
with smtplib.SMTP('127.0.0.1', 1025) as smtp:
    smtp.send_message(message)
PY
curl --fail http://127.0.0.1:8025/api/v1/messages
```

Open `http://127.0.0.1:8025/`; verify the synthetic subject/sender/recipient and body. Developer SMTP send/API assertion returned0 and Chromium UI displayed the message at1280×720; inspected screenshot is ignored `.local/mailpit-capture.png`. `lsof -nP -iTCP:1025 -iTCP:8025 -sTCP:LISTEN` confirmed127.0.0.1 only. Ctrl-C produced graceful shutdown exit0; subsequent curl failed with HTTP000, proving service stopped. QA repeats these observations; SMTP capture is unrelated to application browser tests.

`.env`, `.local/`, `.venv/`, generated caches/data/screenshots are ignored. `.env.example`, `.python-version`, `pyproject.toml`, `uv.lock` remain tracked. Git ignore probes and local example inspection passed without printing secrets. No Django source, settings, templates, migrations, startup, health endpoint or application tests exist yet.


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
| Stop project-owned database | `pg_ctl -D .local/pgdata stop -m fast` | Stops only this repository’s dedicated cluster on55432; preserves unrelated PostgreSQL13 on5432; environment-setup validated. Requires documented project bin PATH |
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

## Acceptance and verification procedures — setup executed; application UNVERIFIED

- Environment setup: record exact tools, import success, application-role PostgreSQL query and synthetic SMTP capture; inspect ignored files and staged examples for secrets. No Django startup result is expected yet.
- Skeleton: start from documented prerequisites, migrate, start web server, verify health and landing page, load local HTMX, run checks/lint/tests/static collection, stop cleanly. Exercise health failure on an isolated test database/connection, not by disrupting an unrelated server.
- Feature verification: map all criteria to evidence. Use synthetic accounts/children and isolated PostgreSQL data. Exercise five-failure/five-minute identity limits across sessions, one-hour account links, seven-day single-use invitations, parent timeout and unauthorized direct requests.
- Recurrence/integrity: competing approvals award one star; overlapping schedulers and approval generate one eligible occurrence; test deleted/edited definitions, late approvals, timezone/DST changes in calendar interpretation and Monday week boundaries. Stop browser sessions to prove scheduler independence.
- Synchronization/offline: two independent browser contexts/computers observe accepted changes within five seconds under normal connectivity. Disconnect one, preserve displayed data, disable mutations, reconnect and refresh before enabling them; test lost mutation responses and stale revisions. Polling must not extend parent authority or discard form input/focus.
- Accessibility/browser release gate: current stable Chrome and Firefox, 1280×720 minimum, keyboard navigation, visible focus, labeled inputs, status text and 200% zoom. Record versions and manual observations; automated bundled Firefox does not certify stable Firefox.

Record procedures, actual results and exact revision in `_docs/verification/` using the verification template. A missing command/service/test or unavailable browser yields BLOCKED for its affected criterion, never PASS. No application checks have run; setup is recorded above and awaits independent QA.

## Upstream references

Intended syntax/prerequisites were checked against [uv projects](https://docs.astral.sh/uv/guides/projects/), [Homebrew PostgreSQL 17](https://formulae.brew.sh/formula/postgresql@17), [Mailpit installation](https://mailpit.axllent.org/docs/install/), and [Playwright browsers](https://playwright.dev/python/docs/browsers). These sources do not validate the local environment or future project commands.
