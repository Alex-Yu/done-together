# Verification: environment-setup — attempt 1

Overall verdict: FAIL
Task / specification: [environment-setup](../tasks/environment-setup.md), [commands](../commands.md)
Revision or exact working-tree state: implementation `f31e725ed4356ee142370cf8323e36f9ea43d8d5`, reviewed on `task/environment-setup` at `789b4d2c2abdea184b33b9ab42480eaa75b97013`. The intervening commit changes only handoff/checkpoint/developer-record hashes; implementation and locked dependencies are unchanged.
Reviewer / independence: Separate QA subagent; no implementation changes made.
Environment: macOS x86_64; repository root `/Users/alexy/Studies/sdd-apps/done-together`; Python 3.13.15, uv 0.12.19, Django 5.2.18, PostgreSQL 17.11, Mailpit 1.32.0, pytest 9.2.0, Ruff 0.17.3; installed stable Chrome 156.0.8078.48 and Firefox 158.0.
Date: 2026-10-28

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | Replay `git --version`, `gh --version`, `uv --version`, project `postgres --version`, `psql --version`, `mailpit version`; inspect browser bundle versions and TCP listeners; compare official archive checksums | Compatible toolchain and unrelated service preserved | Git 2.56.0, gh 2.103.3, uv 0.12.19, PG 17.11, Mailpit 1.32.0; stable browser versions above. Existing PG13 PID858 remains on loopback5432 before/after QA. Project PG17 binds only127.0.0.1:55432. Archive SHA256s match commands.md exactly | PASS |
| AC-002 | `uv sync --locked`; `uv run python --version`; required Django/allauth/psycopg/argon2/dotenv imports; inspect tracked files and source absence | Reproducible dependencies and metadata only | All exit0; sync resolved28/checked25 packages. Python3.13.15/Django5.2.18; no lock diff. No manage.py/config/apps/templates/tests present; Python minor pinned/bounded | PASS |
| AC-003 | `pg_isready`, authenticated app-role `SELECT 1`, privilege/binding queries; app-role create/query/drop of unused `TEST_DB_NAME`; dedicated cluster stop/start | Non-superuser app role, isolated disposable DB and loopback server | SELECT1 returned1; rolsuper=false, rolcreatedb=true, rolcreaterole=false, rolreplication=false; port55432/listen127.0.0.1. Test DB distinct from app DB, absent before test, created/queried/dropped successfully; application DB preserved. Project stop/start/readiness/auth query all exit0 | PASS |
| AC-004 | Documented Mailpit foreground command; synthetic SMTP send; API match; Chromium UI screenshot inspection; listeners; SIGINT and failed HTTP probe | Local capture visible and clean stop without external mail relay | Synthetic QA message sender/setup@example.test, recipient/capture@example.test, subject/body visible in UI at1280×720. API matched. SMTP1025/HTTP8025 bind127.0.0.1 only. No relay options or external email credentials. SIGINT printed graceful shutdown, process exit0; subsequent curl exit7 | PASS |
| AC-005 | Secret-safe dotenv assertions; mode checks; `git check-ignore -q`; tracked-file checks | Independent local credentials excluded from source, examples/lock tracked | Key parity; three distinct generated secrets >=40 characters; .env and pgpass0600; normal/test DB differ; local mail fields safe; credential/service/cache/browser artifacts ignored; example/lock/metadata tracked. No secret values printed | PASS |
| AC-006 | Bundled browser executable existence/execute permissions via Playwright; stable browser plist versions; `uv run pytest --version`, `uv run ruff --version` | Both automation binaries and separate stable browsers installed; tools executable | Chromium build1248 and Firefox build1555 executable paths exist and are executable; stable versions above. pytest9.2.0/Ruff0.17.3 exit0. No application tests claimed | PASS |
| AC-007 | Read and independently replay applicable environment instructions; compare database stop entries and actual service manager | Exact consistent validated setup/start/stop instructions; app commands remain UNVERIFIED | Setup procedures work, but application command table still directs stopping project DB with `brew services stop postgresql@17`, contradicting delivered project-local pg_ctl cluster. See F-001. Application/scheduler commands remain explicitly UNVERIFIED | FAIL |

## Required checks

Commands run from repository root with documented `UV_CACHE_DIR="$PWD/.local/uv-cache"`, `PLAYWRIGHT_BROWSERS_PATH="$PWD/.local/playwright"`, project PostgreSQL/Mailpit bin directories in PATH and `PGPASSFILE="$PWD/.local/pgpass"`. Local sockets/process/browser execution required sandbox escalation; blocked default probes were replayed successfully with appropriate access.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `uv sync --locked` and `git diff --exit-code -- uv.lock` | Exit0 | Locked reproduction does not modify dependencies |
| `uv run python --version`; `uv run python -c 'import django, allauth, psycopg, argon2, dotenv; print(django.get_version())'` | Exit0 | Python3.13.15, Django5.2.18, all imports succeed |
| `uv run pytest --version`; `uv run ruff --version` | Exit0 | Versions9.2.0/0.17.3; no empty test suite claimed |
| `pg_isready -h 127.0.0.1 -p 55432` | Exit0 | Accepting connections |
| `psql -h 127.0.0.1 -p 55432 -U done_together -d done_together -c 'SELECT 1; SELECT current_user, rolsuper, rolcreatedb, rolcreaterole, rolreplication FROM pg_roles WHERE rolname=current_user; SHOW listen_addresses; SHOW port;'` | Exit0 | Authenticated role/binding evidence as above; password read only from protected local file |
| psycopg isolated database check | Exit0 | Read DB names from dotenv; assert distinct/test_ prefix and no preexisting test DB; CREATE DATABASE using Identifier; connect/SELECT1; finally DROP only created test DB; confirm current app DB unchanged |
| `pg_ctl -D .local/pgdata stop -m fast`; `pg_ctl -D .local/pgdata -l .local/postgresql-server.log start` | Both exit0 | Followed by successful readiness and app-role SELECT1; unrelated PG13PID858 unchanged |
| `mailpit --listen 127.0.0.1:8025 --smtp 127.0.0.1:1025 --database .local/mailpit.db --disable-version-check --smtp-disable-rdns --block-remote-css-and-fonts` | Started successfully | Readiness log confirms both loopback listeners |
| Synthetic SMTP/API/UI check | Exit0 | Repeat documented smtplib procedure with subject `Done Together QA setup synthetic capture`, body `Synthetic independent QA verification only; no personal data.`; urllib API subject match, Playwright Chromium UI opened and captured. Screenshot visually inspected: `.local/mailpit-qa-capture.png` (ignored) |
| `lsof -nP -iTCP:1025 -iTCP:8025 -sTCP:LISTEN` | Exit0 | QA Mailpit PID64763, loopback only |
| `kill -INT 64763` and `curl --fail --connect-timeout 2 http://127.0.0.1:8025/` | Stop exit0; curl exit7 | Graceful interrupt shutdown; endpoint no longer responds |
| `mailpit version` | Exit0 with network access | Default sandbox probe printed version then exit1 because online release check DNS was denied; `mailpit version --no-release-check` also independently exit0 without network |
| `shasum -a 256` for both downloaded archives | Exit0, exact matches | PostgreSQL `dd27f2b3c59e73ed14aa3324901242bf69a032a6347805f274e6260322d42979`; Mailpit `d7f3d0964cd2ea4c2a7d10660a12e02876718e67d88ced390d9cd90350a453da` |
| `.env`/ignore/browser/source-absence assertions | Exit0 | Boolean assertions described in AC002/005/006; no credential output |
| `git diff --check` | Exit0 | No whitespace errors before evidence edits |

## Findings

F-001 — AC-007 fails: `_docs/commands.md` application-command table, row `Stop database started for this project` (line189 in verified revision), still specifies `brew services stop postgresql@17`. Starting state: delivered PG17 is a source-built project-local cluster, not a Homebrew service; the document records this supported choice and the working pg_ctl stop procedure earlier. Read the two stop entries and compare the installation/service manager. Expected: the table points to the same verified project-only pg_ctl command. Actual: the table identifies an unrelated service manager and cannot stop the delivered cluster. QA did not execute the inappropriate Homebrew command or disturb unrelated services. Developer should replace it with the verified project-owned cluster stop command and keep application-only commands marked UNVERIFIED. Fresh QA is required after a committed correction.

Robustness note for the same documentation fix: make the version probe `mailpit version --no-release-check` to avoid requiring network access merely to inspect an installed version. The documented unflagged command succeeds with network access, so this note is not a separate failed criterion.

## Services and artifacts

Project PG17 is left running after successful QA stop/start; loopback55432 only. Existing PG13PID858 remains unchanged on5432. QA-started Mailpit is stopped; no external mail sent. Screenshot and service/capture artifacts remain ignored under `.local/`. No application code or implementation documentation was changed by QA.

## Verdict rationale

FAIL because AC-007's setup instructions are internally inconsistent. AC001–006 runtime/environment checks pass. This is attempt1/3, batch completions0/10. Return to developer on the same task branch for the documentation correction, then verify the new implementation commit independently. Task cannot be marked Done or integrated yet.
