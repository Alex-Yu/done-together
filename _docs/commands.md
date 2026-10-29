# Project commands

Status: Bootstrap and001–010 locally implemented; independent release QA2 and final requirements review PASS at `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`. Final [local integration](verification/010-release-integration.md) PASS on develop374c2ad. Earlier dated/prospective sections are historical evidence; this status and the final release records supersede their old pending/unverified labels. No push or deployment authorized.

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

## Environment setup commands — independently verified/integrated

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

`.env`, `.local/`, `.venv/`, generated caches/data/screenshots are ignored. `.env.example`, `.python-version`, `pyproject.toml`, `uv.lock` remain tracked. Git ignore probes and local example inspection passed without printing secrets. The setup task ended without application source; the dependent skeleton now supplies the source/checks recorded below.


## Application commands — skeleton developer-validated; features UNVERIFIED

Skeleton commands below exist and were executed successfully; later task-specific sections record feature validation, including006 scheduler. Future approval commands remain UNVERIFIED. Detailed reproduction and observations follow the table.

| Operation | Intended command | Expected behavior / validation owner |
| --- | --- | --- |
| Install from committed lockfile | `uv sync --locked` | Reproduce environment without changing lock; environment-setup, then skeleton |
| Migrate local database | `uv run python manage.py migrate` | Migrations apply to dedicated local PostgreSQL; application-skeleton initially, affected feature tasks later |
| Start local web server | `uv run python manage.py runserver 127.0.0.1:8000 --noreload` | Loopback HTTP server, no startup errors; keep foreground; application-skeleton |
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
| Select feature tests | `uv run pytest tests/integration/ -k approval -q` | UNVERIFIED future selector; task007 must supply real approval tests, not an empty passing selection |
| Full server tests | `uv run pytest tests/unit tests/integration -q` | Isolated PostgreSQL test database; in-memory mail; concurrency tests use independent transactions; skeleton initializes suite, features extend it |
| Browser tests | `uv run pytest tests/e2e --browser chromium --browser firefox -q` | Live test server with synthetic fixtures and isolated database; skeleton configures fixture and smoke journey, features extend it |
| Recurrence once | `uv run python manage.py reconcile_recurrence --once` | Developer-validated006: idempotent latest eligible catch-up, no browser required |
| Local independent scheduler | `uv run python manage.py reconcile_recurrence --loop --interval 60` | Developer-validated006: actual60-second loop, generic DB retry, clean Ctrl-C and restart |

### Validated skeleton procedures — 2026-10-28

Run from repository root after the setup exports above and start the project-owned PostgreSQL17 cluster if not running. `.env` is loaded by settings; `config.settings.local` requires generated Django/PIN/database secrets even with DEBUG enabled. Tests explicitly select `config.settings.test`, PostgreSQL `test_done_together` and in-memory email. Before any test DB operation, settings reject missing/non-`test_` names or a test name equal to the application database. No SQLite fallback exists. `accounts.User` and its initial migration are installed before feature account workflows.

```sh
uv sync --locked
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run ruff format --check .
uv run ruff check .
uv run pytest tests/integration/test_health.py -q
uv run pytest tests/unit tests/integration -q
uv run pytest tests/e2e --browser chromium --browser firefox -q
uv run python manage.py collectstatic --noinput
```

Developer observed: every command exit0; targeted tests4 passed, full server/config tests11 passed, browser tests2 passed (one each bundled Chromium/Firefox); system checks0 issues, no migration drift, lint/format clean. Asset collection includes5 files (CSS, favicon and three HTMX vendor/provenance files), including local HTMX. Initial migration applied accounts/auth/contenttypes/sessions; replay is idempotent. Health tests execute a real SELECT1, a controlled real closed-port PostgreSQL connection failure and a deterministic DB exception, verifying minimal200/generic503 and no internal details; smoke checks POST/CSRF. The server suite includes equal normal/test DB name rejection even when both start `test_`, and missing-secret rejection in DEBUG.

Browser fixtures start Django's static live server on loopback with disposable PostgreSQL, start/stop Playwright inside the transactional DB fixture lifetime, then tear down the server/database. This prevents Playwright's sync event loop from surrounding Django DB setup/teardown. No async-safety bypass setting is used. Browser tests exercise Tab, visible focus, Enter, successful HTMX fragment response, local asset loading and no script/console errors. The small placeholder interaction is temporary skeleton UI, not a chore/account workflow.

Startup in a foreground terminal:

```sh
PYTHONUNBUFFERED=1 uv run python manage.py runserver 127.0.0.1:8000 --noreload
```

Readiness logs identify settings `config.settings.local`, Django5.2.18, no system errors and `Starting development server at http://127.0.0.1:8000/`. In another terminal, `curl --fail http://127.0.0.1:8000/health/` returned200 with only `{"status":"ok"}` (JSON spacing is insignificant). Open `/` for the Done Together heading and labeled Check connection button; Tab/Enter updates the status without navigating. Ctrl-C exited0; subsequent curl returned connection refusal/HTTP000. `--noreload` makes process ownership/shutdown explicit. This is local development only; no deployment/provisioning is performed.

HTMX2.0.11 provenance/license/SHA384 are in [vendor README](../static/vendor/htmx/README.md); the file is served from `/static/vendor/htmx/htmx.min.js` with no CDN runtime request. The developer verified its SHA384 against official documentation before use.

#### Installed stable Chrome/Firefox, keyboard and actual200% zoom

This supplements the bundled browser tests. Stable Chrome156.0.8078.48 was driven through its installed `chrome` channel in an isolated temporary project profile. Stable Firefox initially reported158.0 during setup; the existing installation applied a pending update on first launch, and the completed checks observed159.0 (confirmed by binary/version capability). Its initial WebDriver launch failed500 during that update; retry with the installed browser succeeded. Browser-internal Firefox experiment/compositor warnings were observed in driver stderr; no application stack was implicated. Bundled Firefox157 remains separate.

Official project-local geckodriver0.37.1 was downloaded from Mozilla's release (no Selenium dependency). Install only if missing, verify checksum before extraction:

```sh
curl --fail --location --output .local/downloads/geckodriver-v0.37.1-macos.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.37.1/geckodriver-v0.37.1-macos.tar.gz
shasum -a 256 .local/downloads/geckodriver-v0.37.1-macos.tar.gz
# Expected d02b3f7003f999caf90974a2ef5da0286c05d01cee19112c86846d759fdba4f5; stop on mismatch.
tar -xzf .local/downloads/geckodriver-v0.37.1-macos.tar.gz -C .local/bin
```

With the loopback app running, start the isolated driver foreground in another terminal:

```sh
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
```

Then run the tracked reproducible observation helper:

```sh
uv run python tools/verify_skeleton_browsers.py
```

The helper opens installed Chrome/Firefox in dedicated temporary profiles and uses real browser zoom: Chrome's native `chrome://settings/appearance` Page zoom selector and Firefox's privileged `browsingContext.fullZoom` via WebDriver. It applies Firefox zoom after navigation to avoid a navigation reset. At100%, both reported1280×720 CSS viewport and DPR1; at200%, both reported640×360 and DPR2. The helper asserts those dimensions, no horizontal overflow, Tab focus outline and Enter-triggered HTMX status. Chrome script/console errors are rejected; bundled-browser tests independently reject application script/console errors in both engines.

Developer helper exit0 and screenshots `.local/skeleton-{chrome,firefox}-{100,200}.png` were visually inspected: text remains readable, the button/status are accessible after normal focus scrolling, no overlapping/clipped horizontal content, visible focus outline. Screenshots are ignored private artifacts. Ctrl-C stops only the project geckodriver, exit0; its status endpoint then refuses connections. WebDriver sessions/profiles are closed by the helper. No user browser profile is reused.

Independent QA must replay checks and bind its verdict to the implementation commit. Feature and scheduler commands remain UNVERIFIED until their tasks implement them.


Custom command names and flags are intended contracts to implement in task 006, not existing Django commands. Production scheduling must use a supervised process or equivalent platform scheduler chosen in an explicit operational task.

### Validated account procedures — task001, 2026-10-28

Account-specific implementation now uses the locked django-allauth65.21.0. Verified email is mandatory, sign-in is email/password only, and the existing custom user is retained. No household/PIN/board workflows are implemented by this task. The reusable verified-account guard is exercised through a test-only protected endpoint; its later household/PIN integration remains tasks002–004/007.

```sh
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run ruff format --check .
uv run ruff check .
uv run pytest tests/integration/test_accounts.py -q
uv run pytest tests/unit tests/integration -q
uv run pytest tests/e2e --browser chromium --browser firefox -q
uv run python manage.py collectstatic --noinput
uv sync --locked
```

Developer final required regression:32 server/config tests passed (21 account cases plus11 bootstrap cases),4 bundled browser tests passed (account lifecycle and skeleton in each engine), checks/drift/lint/format/locked sync exit0. Account-targeted runs passed19 then20 cases while coverage was added; the full32-case run covers the final21 account cases. After two final narrow safeguards, only their affected checks were repeated: database-independent failure rendering1 pass/20 deselected, and SMTP registration/unsent-link retry1 pass/20 deselected. No empty selector is treated as success. Static collection copied7 files for account/static changes and includes local HTMX. All PostgreSQL test commands must run sequentially against the single disposable test database; independent simultaneous suites require separately named test databases.

Account links expire at one hour, including exact boundary tests3599/3600/3601 seconds. Allauth database confirmation links use1/24day plus explicit boundary/unsent-key checks. Verification GET exchanges the private key into a server-side, nonce-bound confirmation flow and redirects to a URL containing no original email key; GET never verifies. An older tab cannot consume a subsequently opened link. The CSRF-protected POST rechecks unexpired/unconsumed state under a PostgreSQL row lock. Recovery uses the supported custom token-generator hook to reject at3600 seconds (Django's default accepts the exact timeout); password changes invalidate old tokens and credentials. Reset POST locks/rechecks the current user before replacing the password.

Security headers: every account response/redirect is no-store. Original private verification/recovery token URLs use `Referrer-Policy:no-referrer`; ordinary account pages and token-free forms use `same-origin`, suppressing cross-origin referrers while permitting native browser CSRF Origin checks. A blanket no-referrer policy caused real browser POST Origin:null/403 and was corrected without relaxing CSRF. Request/CSRF-security log handlers redact private path segments and all account query strings, including encoded redirect parameters. Exception filtering also hides the PIN pepper. Password inputs never re-render their values.

The PostgreSQL identity limiter serializes five consecutive incorrect passwords into five minutes of restriction across sessions/processes. Restricted requests never extend the deadline; correct credentials are denied until expiry, then permitted success clears failures. Supplemental source throttling is a separate atomic60 account POSTs per60-second window, using REMOTE_ADDR (no untrusted forwarded headers). Allauth cache limits are replaced by these DB limits. Source/identity keys are HMAC-derived and contain no plaintext email/IP. The shared identity helper is prepared for task003 PIN integration, which is not yet claimed verified.

Known/unknown recovery and resend requests use equal generic responses and delivery attempts. SMTP errors return a recoverable503 without provider details or false success; a retained unverified registration can request another link without duplicating its account. Unsent confirmation records deny access safely. Account database failures render a generic503 independent of session/database-backed template context. Base settings use secure/HttpOnly sessions; local loopback HTTP/test settings alone disable Secure for local execution.

#### Installed browsers, real SMTP capture and persistence

Start the loopback webserver, Mailpit and geckodriver with the previously documented foreground commands. Then:

```sh
uv run python tools/verify_account_browsers.py
uv run python tools/verify_account_mail.py
# Stop/restart only the local webserver, then:
uv run python tools/verify_account_mail.py --revisit
# Retained skeleton installed-browser regression helper:
uv run python tools/verify_skeleton_browsers.py
```

The installed-browser account helper passed Chrome156.0.8078.48/Firefox159.0 at native100% (1280×720,DPR1) and200% (640×360,DPR2): keyboard navigation through labeled email/password/button, visible focus, generic failed-login message, empty password on re-render and no horizontal overflow. The `.local/account-{chrome,firefox}-{100,200}.png` screenshots were visually inspected. These are private ignored artifacts. Bundled-browser tests complete register→email capture→verify→sign in→reload→sign out→recover→old password denial/new password sign-in in isolated PostgreSQL/in-memory mail.

`verify_account_mail.py` passed using installed Chrome and actual loopback SMTP/Mailpit: synthetic registration, captured verification link, verification/sign-in/sign-out, captured recovery email and password replacement. Mailpit UI screenshot `.local/account-mailpit-capture.png` visually confirms both email types. The helper retains only generated synthetic credentials in ignored0600 `.local/account-mailpit-fixture.json`; it never prints credentials or links, including on failure. After webserver restart, `--revisit` passed sign-in/reload with the stored account, demonstrating persistence. The helper creates isolated synthetic local accounts; no real family data or external email is used.

Developer services started only for verification are stopped before handoff. PostgreSQL17 remains running on55432; unrelated PostgreSQL13 on5432 is preserved. A mistakenly overlapping pair of disposable test suites caused teardown failures; those results were discarded and suites rerun sequentially. A framework long traceback included local connection parameters during that failure; the project-only database credential was immediately rotated in ignored `.env`/pgpass, parity/authenticated SELECT1 rechecked, and pytest short tracebacks configured. No credential value is included in source/evidence. Do not print fixture files or raw verbose connection traces.

Independent QA must verify task001 at its exact implementation commit. Remaining feature/scheduler commands remain UNVERIFIED.


### Validated household procedures — task002, 2026-10-28

Household creation/settings are reached from the signed-in landing page’s Household settings link (`/households/`). Until task003 adds parent PIN authority, verified account membership authorizes the bootstrap create/join/invite/settings actions. No child/PIN/chore workflows are implemented or claimed here.

```sh
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run ruff check .
uv run ruff format --check .
uv run pytest tests/integration/test_households.py -q
uv run pytest tests/unit tests/integration -q
uv run pytest tests/e2e --browser chromium --browser firefox -q
uv run python manage.py collectstatic --noinput
uv sync --locked
```

Developer observed: targeted household17 passed; full server/config49 passed; full bundled-browser6 passed. Django checks/drift/lint/format/static/locked sync exit0. Static collection copied2 changed/new assets with6 unmodified. A final narrow recovery correction cleared a rejected invitation flow so the wrong recipient can return to their own household; its affected access test passed1/16 deselected. No unchanged suites were rerun after passing.

The two-browser household journey uses independent contexts/computers: creator timezone Europe/Warsaw is suggested, creation/invitation succeeds, intended recipient opens the invitation before registration, registers/verifies/signs in, joins, and sees the same immutable household timezone while their browser uses America/New_York. Reload preserves membership; reused invitation denies access. Successful invitation POST redirects to GET so reload cannot resend/supersede an invitation.

PostgreSQL constraints enforce one membership per parent and only household slots1/2, with unique household/slot. User→household→invitation locks serialize acceptance/create races. Tests cover simultaneous acceptance of one token, competing recipients for the last parent slot, competing household joins and creation versus joining; exactly one succeeds, with no double consumption/third parent/second household. Both members have the same scoped settings/management rights. Two actual households, outsiders, unverified users and forged IDs are tested for denied reads/mutations without foreign data exposure.

Invitation raw tokens are32 random bytes, emailed only through existing allauth local SMTP handling; only SHA256 digests are stored. Expiry is exactly seven days and tested just before/at/after the boundary. GET exchanges the private token into a session/nonce-bound flow, without joining; authenticated intended-recipient POST rechecks and consumes under lock. Anonymous users are directed to sign in while their pending flow survives registration. Wrong/expired/reused links cannot change membership; invalid state has a recoverable explanation. Rejected pending flows are cleared. Original private URLs use no-referrer; safe forms same-origin; all household responses no-store. Request/security logs redact invite/join path keys and all household queries. CSRF remains required. Invitation creation/replacement and SMTP delivery share a transaction; delivery failure rolls back the new/superseding state, displays503 and permits retry.

Timezone is a validated IANA selection, initially suggested with browser Intl; UTC remains the visible fallback if Intl cannot supply a supported zone. Invalid/missing selections create no partial household. No timezone-change controls exist; direct settings input cannot change it, and model saves reject a changed existing timezone. Chore/local-overdue semantics remain tasks005–007.

#### Installed stable browsers, real invitations and restart persistence

With documented loopback app/Mailpit/geckodriver running:

```sh
uv run python tools/verify_household_browsers.py
# Stop/restart only the loopback app, then:
uv run python tools/verify_household_browsers.py --revisit
```

The tracked helper seeds explicitly synthetic verified local parent fixtures, leaving registration verification to the real bundled-browser journey/task001. Generated credentials remain ignored0600 `.local/household-browser-fixtures.json`, never printed. It drives installed Chrome156.0.8078.48/Firefox159.0 at actual native100% (1280×720,DPR1) and200% (640×360,DPR2), covering creation, browser timezone suggestion, keyboard/labeled controls/focus, actual SMTP invitation capture, recipient sign-in/join and recoverable full-household/reused-link errors. All four cases passed with no horizontal overflow. Viewport screenshots `.local/household-{chrome,firefox}-{100,200}.png` and `-invalid.png` were visually inspected: readable text, ordinary vertical scrolling, no horizontal clipping. The helper closes its browser sessions/profiles; errors redact fixture passwords/private paths.

Mailpit API confirmed invitation email receipt and the UI visibly showed actual synthetic invitation emails; screenshot `.local/household-mailpit-capture.png` was inspected. No external SMTP provider or delivery is configured. After app restart, the helper’s `--revisit` passed all four stored households, confirming membership/timezone persistence across sign-out/reload/restart and computers. App/Mailpit/geckodriver were then stopped cleanly (exit0; endpoints refused/HTTP000). ProjectPG17 remains55432; unrelatedPG13:5432 is preserved.

Task002 F001 correction: generic DatabaseError recovery now covers household endpoints as well as accounts after source/authorization checks. With DEBUGTrue, committed regressions inject controlled failures at create-service, settings-render, invitation-send transaction and join-service boundaries; each returns generic503/no-store/same-origin, omits private detail/traceback from response and actual request-handler logs, leaves household/membership/invitation state unchanged and permits retry. Run `uv run pytest tests/integration/test_households.py -k domain_database_failures -q`:4 passed/17 deselected. Original independent QA probe `.local/qa_households_extra.py` also passed1. Fresh full server regression53 passed; Django check/drift/lint/format/diff pass. Normal UI/browser/SMTP/scheduling code is unchanged by this one-line recovery-prefix fix, so prior QA positive6-browser/native/SMTP/restart evidence is retained; no unchanged browser suites repeated.

Independent QA must verify the exact task002 implementation. Task003 must add parent PIN management protection while preserving verified-account creation/join bootstrap. Remaining feature/scheduler commands remain UNVERIFIED.


### Validated PIN/child/parent-authority procedures — task003, 2026-10-29

Verified-account household creation/join remain bootstrap. Existing household settings/invitations now require a selected-parent unlock; first/own parent PIN setup/reset stays reachable while locked and requires the selected member’s own account password. The board-opening account and selected parent may differ. The current read-only board surface lists children and remains visible when controls lock; full columns arrive004, actual child chore submission007. There are no child deletion controls/endpoints.

```sh
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run ruff check .
uv run ruff format --check .
uv run pytest tests/integration/test_pins.py -q
uv run pytest tests/unit tests/integration -q
uv run pytest tests/e2e --browser chromium --browser firefox -q
uv run python manage.py collectstatic --noinput
uv sync --locked
```

Developer observed: targeted PIN suite19 passed, full backend72 passed in33.78s and bundled browser8 passed in49.16s, with earlier household regression21 passed. A final exact-password-whitespace correction was verified by its one affected password/pepper case (1 passed/19 deselected); no unchanged broader suites repeated. Current PIN collection contains20 cases after that addition. System/migration-drift/lint/format/static/locked checks pass. Static collection copied3 changed/new files with6 unmodified. The earlier002 request/browser fixtures now explicitly set/unlock parent credentials before protected settings; no authority bypass fixture is used for those HTTP checks.

PIN validation accepts exactly four ASCII digits as strings, preserving `0007`/`0123`; no integer conversion. Stored PINs are salted maintained Argon2 hashes of identity/type-namespaced HMAC-SHA256 values using the independent ignored pepper. The raw PIN alone cannot verify the stored hash, and a different pepper denies verification. Password checks preserve exact whitespace and use the existing account password identity limiter. Parent/child PINs have their own shared identity keys with the approved five failures/five minutes across sessions; blocked attempts never extend the deadline and permitted success clears failures. Child credential checks require household board access and never grant/touch parent authority. The executable child-check endpoint exists only in a test URL fixture; no product submission workflow is claimed before007.

Board authority is a PostgreSQL row keyed by an HMAC of the signed-in board session key, binding household, selected parent, credential version and last accepted parent activity. Each protected request rechecks membership, verification, active selected account, version and exact60-second expiry. Only successful parent POSTs touch authority; views, child checks, invalid/unauthorized actions do not. Explicit parent-control interaction may send a throttled CSRF-protected activity request; the client listens only within unlocked parent controls, never automatic timers/background polls/global mouse/child activity. Its timer only locks/reloads the visible board. Server enforcement remains authoritative.

PIN resets increment credential version, invalidating all prior selected-parent grants. Unlock locks selected user→credential through verification/grant, matching reset order; deterministic paused-old-PIN/reset concurrency proves an old PIN cannot be tagged with a new version. Deactivating selected B revokes B’s grant in a board session opened by A. Leading-zero add/name/PIN updates, malformed/Unicode digits, old/new replacement, forged household/parent/child IDs, CSRF, no-store/password non-echo and generic DB failure checks pass. Failed authentication counters must be committed before raising a later product-transition denial;007 must preserve that shared-limiter rule when integrating submission.

#### Installed browsers and actual idle timing

With documented loopback app/Mailpit/geckodriver running:

```sh
PYTHONUNBUFFERED=1 uv run python tools/verify_pin_browsers.py
# Stop/restart only the app, then:
PYTHONUNBUFFERED=1 uv run python tools/verify_pin_browsers.py --revisit
```

The helper seeds private synthetic fixtures and exercises real invitation setup, then parent selection/password-authorized PIN setup, other-parent unlock, child addition/name editing/PIN reset, manual lock, own parent PIN replacement and recoverable old-PIN error. Installed Chrome156.0.8078.48/Firefox159.0 passed native100% (1280×720,DPR1) and200% (640×360,DPR2), keyboard/labeled focus and no horizontal overflow. Both100% browser cases then actually idled61seconds together, without parent input/heartbeat; each automatically locked while its read-only child board remained visible. This was real elapsed time, not a clock override. Deterministic backend tests separately cover59/60, accepted activity extending89/90, passive/child/failed-action nonextension and exact299/300 restriction retry.

Screenshots `.local/pins-{chrome,firefox}-{100,200}.png` and `-idle.png` were visually inspected for readable board/child text and locked controls. Firefox WebDriver initially appended to a prefilled name field; helper fill now clears first, and narrow native100/200 checks proved exact replacement without repeating idle. The post-app-restart `--revisit` passed stored parent PIN and child state in all four browser/zoom cases. Helpers close their profiles; generated passwords stay in ignored0600 fixture files and are not printed. No external SMTP or real family data is used.

App/Mailpit/geckodriver stopped cleanly after checks (exit0; endpoints refuse/HTTP000). ProjectPG17 remains55432; unrelatedPG13 is preserved. Independent QA must verify task003 at its exact implementation commit; full board/child submission remain later tasks.


## Acceptance and verification procedures — bootstrap executed; features UNVERIFIED

- Environment setup: record exact tools, import success, application-role PostgreSQL query and synthetic SMTP capture; inspect ignored files and staged examples for secrets. No Django startup result is expected yet.
- Skeleton: start from documented prerequisites, migrate, start web server, verify health and landing page, load local HTMX, run checks/lint/tests/static collection, stop cleanly. Exercise health failure on an isolated test database/connection, not by disrupting an unrelated server.
- Feature verification: map all criteria to evidence. Use synthetic accounts/children and isolated PostgreSQL data. Exercise five-failure/five-minute identity limits across sessions, one-hour account links, seven-day single-use invitations, parent timeout and unauthorized direct requests.
- Recurrence/integrity: competing approvals award one star; overlapping schedulers and approval generate one eligible occurrence; test deleted/edited definitions, late approvals, timezone/DST changes in calendar interpretation and Monday week boundaries. Stop browser sessions to prove scheduler independence.
- Synchronization/offline: two independent browser contexts/computers observe accepted changes within five seconds under normal connectivity. Disconnect one, preserve displayed data, disable mutations, reconnect and refresh before enabling them; test lost mutation responses and stale revisions. Polling must not extend parent authority or discard form input/focus.
- Accessibility/browser release gate: current stable Chrome and Firefox, 1280×720 minimum, keyboard navigation, visible focus, labeled inputs, status text and 200% zoom. Record versions and manual observations; automated bundled Firefox does not certify stable Firefox.

Record procedures, actual results and exact revision in `_docs/verification/` using the verification template. A missing command/service/test or unavailable browser yields BLOCKED for its affected criterion, never PASS. Setup has independent PASS; skeleton developer checks are recorded above and await independent QA. Feature checks have not run.

## Upstream references

Intended syntax/prerequisites were checked against [uv projects](https://docs.astral.sh/uv/guides/projects/), [Homebrew PostgreSQL 17](https://formulae.brew.sh/formula/postgresql@17), [Mailpit installation](https://mailpit.axllent.org/docs/install/), and [Playwright browsers](https://playwright.dev/python/docs/browsers). These sources do not validate the local environment or future project commands.

## Task004 affected board verification

Per user instruction, use targeted feature/security checks plus affected regressions during delivery; reserve full integrated suites and complete stable-browser journeys for010. Do not repeat unchanged account/mail/real61-second idle flows for board presentation changes.

```sh
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_board.py tests/integration/test_pins.py -q
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell; stop owned driver afterward with Ctrl-C:
RUN_NATIVE_BOARD=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_board_native.py -q -s
```

Observed:5 unique board cases and20 affected PIN cases passed across scoped runs; native1 test/four installed Chrome156/Firefox159 engine/100/200% cases passed. Native test uses disposable PostgreSQL/live server and an internal patched work provider, not production fixtures or an HTTP seed route. Chrome uses actual Page zoom setting; Firefox uses privileged browsingContext.fullZoom. Screenshots `.local/board-{chrome,firefox}-{100,200}.png` inspected. Production renders real children/empty work; persisted chore/review/approval week behavior remains005–008. Full evidence: [004 developer](verification/004-board-developer.md).

## Task005 affected one-off verification

```sh
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -q
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell; stop owned driver afterward:
RUN_NATIVE_CHORES=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_chores_native.py -q -s
```

Observed005 implementation:37 server cases PASS;1 native test/four Chrome156/Firefox159 native100/200% cases and two DST timezone contexts PASS. Native calendar/select values use test assignment after labeled keyboard-focus checks; keyboard submits/text/recovery tested. Real two-process PostgreSQL restart included. Full integrated browser journeys remain010. Evidence: [005 developer](verification/005-one-off-developer.md).

## Task006 affected recurrence verification —2026-10-29

Run only one disposable PostgreSQL suite at a time. `UV_CACHE_DIR=.local/uv-cache uv run python` uses the managed interpreter; the host `python` shim is unavailable. No browser or web server is needed for the scheduler:

```sh
UV_CACHE_DIR=.local/uv-cache uv run python manage.py reconcile_recurrence --once
UV_CACHE_DIR=.local/uv-cache uv run python manage.py reconcile_recurrence --loop --interval 60
# Ctrl-C stops the owned foreground scheduler cleanly.
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_recurrence.py -q
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -q
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell; stop owned driver after verification:
RUN_NATIVE_RECURRENCE=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_recurrence_native.py -q -s
```

Observed:29 recurrence cases passed across scoped runs (28 initial,1 added real connection-failure/restart case);37 affected regressions passed. Six race cases additionally passed after strengthening eligible-generation vs edit/delete fixtures. The real subprocess test runs once twice, observes actual60-second loop generation with no browser, sends SIGINT/observes exit0, and starts a fresh idempotent scheduler. A separate real refused connection produces a generic nonzero failure, then a fresh correctly connected process succeeds; deterministic loop failure/retry coverage checks interval60 without another elapsed-minute wait. Installed Chrome156.0.8078.48/Firefox159.0 passed four native100/200% cases: weekday checkbox keyboard selection, labels/focus, validation, future-only edits and deletion. Native select values are assigned after keyboard/label checks. All eight ignored screenshots were visually inspected; readable vertical scrolling/no horizontal overflow. Driver and all owned subprocesses stopped. Existing005 browser-local overdue evidence is retained for unchanged local-date JS/identity/date rendering;006 adds household DST/date scheduling checks. Actual submission/approval/stars remain007–008. Full evidence: [006 developer](verification/006-recurrence-developer.md).

## Task007 affected review verification —2026-10-29

Run PostgreSQL suites sequentially; keep projectPG17:55432 and unrelatedPG13:5432 separate.

```sh
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_review.py tests/integration/test_recurrence.py tests/integration/test_chores.py tests/integration/test_board.py tests/integration/test_pins.py -k 'not real_no_browser_once_loop_sixty_restart' -q
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell; stop the owned driver afterward:
RUN_NATIVE_REVIEW=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_review_native.py -q -s
```

The `--allow-system-access` flag on the driver command above is required for Firefox native browser zoom. Do not omit it: Firefox's privileged zoom API otherwise returns HTTP500/System access required. The verification helper now surfaces that setup failure directly instead of misreporting a heading/sign-in timeout, and restores content context after a zoom failure. Start this exact owned driver before the native run; stop it afterward. QA3 must use the full command above.

Actual review/approval/star workflows now replace prior synthetic-state evidence for007. Exact executed selectors/counts and retained unchanged006 scheduler evidence are in [007 developer](verification/007-review-developer.md).008 totals/week projection and009 synchronization/offline remain later.

## Task008 affected progress verification —2026-10-29

```sh
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_stars.py tests/integration/test_review.py tests/integration/test_board.py tests/integration/test_pins.py tests/integration/test_chores.py tests/integration/test_recurrence.py -k 'not real_no_browser_once_loop_sixty_restart' -q
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell; stop owned driver afterward:
RUN_NATIVE_STARS=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_stars_native.py -q -s
```

Observed:104 server cases PASS, then added foreign-history scoping case1 PASS/7 deselected (105 unique overall;8 new stars cases). One native test/four Chrome156/Firefox159100/200 cases PASS; four screenshots inspected. Exact selectors, calendar boundaries/DST, real approval/race/restart/retention and retained unchanged evidence: [008 developer](verification/008-stars-developer.md). Run DB suites sequentially.009 owns idle periodic rollover refresh;008 proves fresh reads across boundary without writes.


## Task009 affected synchronization verification —2026-10-29

```sh
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/integration/test_sync.py tests/integration/test_stars.py tests/integration/test_review.py tests/integration/test_board.py tests/integration/test_pins.py tests/integration/test_chores.py tests/integration/test_recurrence.py -k 'not real_no_browser_once_loop_sixty_restart' -q
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell; stop owned driver afterward:
RUN_NATIVE_SYNC=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_sync_native.py -q -s
# Narrow required Firefox200 form follow-up; no broad replay:
SYNC_NATIVE_CASE=firefox-2 RUN_NATIVE_SYNC=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_sync_native.py -k open_form -q -s
```

Observed:109 affected server cases PASS (4 new sync),3 native tests PASS, one narrow Firefox200 form test PASS.36 accepted mutation→other-session DOM measurements0.9051–2.0266s cover each required class in all four native observer engine/zoom cases. Both independent profiles are on this one Mac; no physical-second-computer claim. Native idle Monday and actual local-date timer, unchanged DOM, drafts/caret/conflicts, offline/500/unreachable, unknown committed response/no retry, exact expiry and confirmed private-view clear verified. Initial Firefox form navigation reset zoom; only the narrow follow-up counts as200% form conflict/unknown-response evidence. Blank Chrome200 offline capture is excluded as visual evidence. System/drift/Ruff149/diff PASS; static collection3 copied9 unmodified. [Exact evidence/selectors](verification/009-synchronization-developer.md); logs/screenshots ignored `.local/verification/009/`. Run DB suites sequentially; full integrated regression remains010.

## Task010 integrated release commands —2026-10-29

The setup/feature sections above are historical execution records. The application now includes001–009; use this section for the current final gate. Task010 is In review atdc456af after scoped QA1 verifier corrections; affected QA2 and final orchestrator review remain required. The correction section below identifies retained evidence and required all13 native/PIN2 rechecks. Run all disposable PostgreSQL suites **sequentially**; keep local projectPG17:55432 and unrelatedPG13:5432 distinct. Native Firefox requires the exact driver privilege flag below.

```sh
UV_CACHE_DIR=.local/uv-cache uv sync --locked
UV_CACHE_DIR=.local/uv-cache uv run python manage.py migrate
UV_CACHE_DIR=.local/uv-cache uv run python manage.py check
UV_CACHE_DIR=.local/uv-cache uv run python manage.py makemigrations --check --dry-run
UV_CACHE_DIR=.local/uv-cache uv run ruff check .
UV_CACHE_DIR=.local/uv-cache uv run ruff format --check .
UV_CACHE_DIR=.local/uv-cache uv run pytest tests/unit tests/integration -q
PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e --browser chromium --browser firefox -q
UV_CACHE_DIR=.local/uv-cache uv run python manage.py collectstatic --noinput
UV_CACHE_DIR=.local/uv-cache uv run python manage.py reconcile_recurrence --once
.local/bin/geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
# Separate shell, after bundled suite completes:
RUN_NATIVE_BOARD=1 RUN_NATIVE_CHORES=1 RUN_NATIVE_RECURRENCE=1 RUN_NATIVE_REVIEW=1 RUN_NATIVE_STARS=1 RUN_NATIVE_SYNC=1 RUN_NATIVE_RELEASE=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_board_native.py tests/e2e/test_chores_native.py tests/e2e/test_recurrence_native.py tests/e2e/test_review_native.py tests/e2e/test_stars_native.py tests/e2e/test_sync_native.py tests/e2e/test_release_keyboard_native.py -q -s
# Verify the Firefox200 form/conflict/lost-response zoom scope explicitly:
SYNC_NATIVE_CASE=firefox-2 RUN_NATIVE_SYNC=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_sync_native.py -k open_form -q -s
```

The complete server suite includes actual independent-transaction/HTTP races and the real no-browser scheduler once/60-second-loop/SIGINT/restart/refused-connection checks; no long-scheduler deselection is allowed at this gate. Native release cases are independently isolated per engine/zoom, preserve real per-source limits, and use actual keyboard navigation/select/date input rather than DOM field value/focus assignment. Existing earlier native scenarios retain their documented scope and supplement this integrated fresh-account keyboard journey.

For actual SMTP and process-persistence checks, start only the documented loopback Mailpit/application processes, verify `/health/`, then run:

```sh
PYTHONUNBUFFERED=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run python tools/verify_account_mail.py
PYTHONUNBUFFERED=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run python tools/verify_pin_browsers.py
# Stop/restart only the owned app; verify readiness, then:
PYTHONUNBUFFERED=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run python tools/verify_account_mail.py --revisit
PYTHONUNBUFFERED=1 PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run python tools/verify_pin_browsers.py --revisit
```

The PIN helper also captures actual invitations and performs real61-second stable-browser inactivity while retaining board content. Close owned app/Mailpit/driver cleanly and verify their listeners stop; preserve both PostgreSQL clusters. [010 developer matrix](verification/010-release-developer.md) records actual exact revision/counts/latencies/screenshots, setup limitations and discovered integrated defects. Logs, screenshots, synthetic private fixture files and per-event measurements stay ignored; no external SMTP or deployment is configured.

Developer010 executed the final gates:166 server PASS152.05s (final strengthened HTTP3 PASS5.26s), bundled8 PASS50.14s, nine unique native tests verified through7 retained PASS+2 corrected/rechecked PASS53.96s and explicitFirefox200 followup2 PASS20.45s, complete fresh keyboard4 PASS95.45s. Actual loopback SMTP/invitations4, real61sec idle2, fresh app restart/account and selected-identity household/PIN revisits4 PASS.36 same-Mac events0.9142–2.0968s. Ruff156/static/system/drift/locked/scheduler/diff PASS. [Developer record](verification/010-release-developer.md) qualifies code-revision reuse, historical failures and exact artifacts; this is not independent QA or final release completion. Owned app/Mailpit/driver stopped cleanly, DB17/13 retained.

## Task010 affected QA1 correction checks

At correction `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`, only bundled PIN verification, shared native focus helper and native review cleanup changed. Product/backend/config/dependencies remain unchanged from QA1's3769e5c. [Fix evidence](verification/010-release-qa1-fixes-developer.md) records bundledPIN2 PASS18.46s, native review4 cases PASS31.33s and12 actual positive/negative focus controls PASS; Ruff157/diff PASS. QA1 FAIL remains historical. Independent QA2 must run **all13 installed-native tests** (the full native command above with every flag, including RUN_NATIVE_RELEASE=1), plus:

```sh
PLAYWRIGHT_BROWSERS_PATH=.local/playwright UV_CACHE_DIR=.local/uv-cache uv run pytest tests/e2e/test_pins.py --browser chromium --browser firefox -q
```

Retain fresh independent QA1's unchanged166 server/domain/security/config/SMTP/real-idle/restart evidence only with the recorded exact product/configuration diff proof; no developer replay of those unchanged gates. Native focus evidence requires QA2 recertification because its shared helper changed. Owned services are stopped; PG17/13 remain available. No source push/deployment authorized.

## Verified local release —2026-10-29

Independent [QA2](verification/010-release-qa-attempt-2.md) and [final requirements review](verification/010-release-requirements.md) PASS all27 requirements atdc456af. Full166 PostgreSQL/server cases, eight unique bundled cases,13 installed-native tests including four complete keyboard journeys,12 focus controls, actual loopback SMTP/61second inactivity/restart/privacy and scheduler gates are supported by the revision-bound records. QA1 failures remain historical; affected QA2 passes supersede them. Final [integration](verification/010-release-integration.md) PASS at develop374c2ad with28 affected cases and unchanged reviewed code.

For local use, keep the dedicated PostgreSQL17 cluster on55432 running (documented start procedure above); preserve unrelated PostgreSQL13 on5432. In separate foreground terminals at repository root:

```sh
.local/bin/mailpit --listen 127.0.0.1:8025 --smtp 127.0.0.1:1025 --database .local/mailpit.db --disable-version-check --smtp-disable-rdns --block-remote-css-and-fonts
UV_CACHE_DIR=.local/uv-cache uv run python manage.py runserver 127.0.0.1:8000 --noreload
UV_CACHE_DIR=.local/uv-cache uv run python manage.py reconcile_recurrence --loop --interval 60
```

Open `http://127.0.0.1:8000/`; account/invitation emails are captured only at `http://127.0.0.1:8025/`. Scheduler operation is independent of browsers. Ctrl-C stops each owned foreground process. No app/Mailpit/driver is intentionally left running after verification; PostgreSQL instances are retained. Local HTTP, same-Mac independent-profile synchronization evidence and synthetic fixtures certify the agreed local scope; production hosting/email/operations remain outside this delivery.
