# Local setup and commands

Scripts use Bash, resolve the repository root and configure `uv`, Playwright and project-local tool paths. They prefer `.local/postgresql/bin/` and `.local/bin/`, then Homebrew PostgreSQL 17 paths and your existing `PATH`. No shell profile changes are needed.

## First-time setup

1. Install `uv`, PostgreSQL **17** server/client tools and Mailpit. On macOS with Homebrew, the optional installer is:

   ```sh
   ./scripts/install-tools.sh
   ```

   On other systems, install these tools through your package manager. Existing tools under `.local/` are also supported; ignored binaries/data do not come with a clone.

2. Create the development environment:

   ```sh
   ./scripts/setup.sh
   ```

   Setup installs locked Python dependencies, creates `.env` with independent secrets if missing, initializes a dedicated PostgreSQL cluster if missing, starts it, provisions the database, applies migrations and runs Django checks. Existing `.env`, role passwords and application data are preserved. PostgreSQL binds to **127.0.0.1:55432**; unrelated services on 5432 are untouched.

   To install bundled test browsers too, use `./scripts/setup.sh --browsers`. For an already provisioned database, configure `.env` first and use `./scripts/setup.sh --external-db`; this skips cluster management and role/database provisioning. Its role needs `CREATEDB` for disposable test databases.

3. Start local services:

   ```sh
   ./scripts/dev.sh
   ```

   This starts the project database if present, then runs Django, Mailpit and the recurrence scheduler. App: <http://127.0.0.1:8000/>. Email UI: <http://127.0.0.1:8025/>. An external database must already be running. Ctrl-C stops the three foreground services and leaves PostgreSQL running. If a service exits, the other two stop too.

4. Register a synthetic parent account and verify its email in Mailpit. Create a household, set your parent PIN, unlock controls, then add children and assign chores. Invite a second parent through protected settings.

## Configuration

Defaults come from `.env.example`; `.env` and `.local/` remain private and ignored.

| Setting | Local value / purpose |
| --- | --- |
| `DJANGO_SETTINGS_MODULE` | `config.settings.local` |
| `DJANGO_SECRET_KEY`, `PIN_HASH_PEPPER` | Independent secrets; preserve them to retain sessions/PIN verification |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `done_together` database/role and generated password |
| `DB_HOST`, `DB_PORT` | `127.0.0.1`, `55432` for the managed cluster |
| `TEST_DB_NAME` | `test_done_together`; must start with `test_` and differ from the app database |
| `EMAIL_HOST`, `EMAIL_PORT` | Mailpit at `127.0.0.1:1025`; TLS off, empty SMTP credentials |
| `APP_BASE_URL` | `http://127.0.0.1:8000` |
| `DJANGO_DEBUG` | Local debugging only; local settings allow loopback hosts |

Setup never replaces an existing `.env`. Correct placeholders or mismatched credentials manually; it does not reset existing role passwords. Do not commit credentials or real household data.

## Daily commands

| Action | Command |
| --- | --- |
| Start all services | `./scripts/dev.sh` |
| Run app only | `./scripts/dev.sh web` |
| Run email capture only | `./scripts/dev.sh mail` |
| Run scheduler only | `./scripts/dev.sh scheduler` |
| Reconcile recurrence once | `./scripts/dev.sh once` |
| HTTP/database readiness | `./scripts/dev.sh health` |
| Apply migrations | `./scripts/dev.sh migrate` |
| Collect static assets | `./scripts/dev.sh static` |
| Project database controls | `./scripts/db.sh start`, `status` or `stop` |
| Refresh dependencies and migrate | `./scripts/setup.sh` |
| Available options | Add `--help` to any executable script |

For separate terminals, start `mail`, `web` and `scheduler` individually. The scheduler must stay running to generate recurring work while browsers are closed. `health` expects HTTP 200 and `{"status":"ok"}`; database failure returns 503. Local Django serves source static assets without a frontend build.

## Stop and troubleshoot

1. Press Ctrl-C in the `dev.sh` terminal, or in each terminal if services were started individually.
2. Optionally stop only this project's database:

   ```sh
   ./scripts/db.sh stop
   ```

| Symptom | Check / fix |
| --- | --- |
| Missing executable | Use the optional installer or install the named tool on `PATH` |
| Host Python cannot find 3.13 | Scripts use managed Python through `uv`; avoid host Python shims |
| Missing configuration | Run setup; correct existing `.env` placeholders without regenerating working secrets |
| Database connection refused | Check `./scripts/db.sh status`, then `start`; inspect `.local/postgresql-server.log` |
| Database authentication fails | Match `.env` to the provisioned role; do not reinitialize the cluster |
| Partial cluster initialization | Inspect `.local/pgdata` and the error; setup refuses to overwrite an existing cluster |
| Email send fails | Run `mail` or the full development stack; SMTP uses 1025, UI uses 8025 |
| No new recurring work | Run the scheduler; unfinished work prevents another occurrence |
| Port occupied | Stop/reuse only a process you own; the combined launcher refuses occupied service ports |

See [testing](testing-guidelines.md) for verification commands. These scripts target local development, not production deployment.
