#!/usr/bin/env bash
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
external_db=false
browsers=false
for option in "$@"; do
    case "$option" in
        --external-db) external_db=true ;;
        --browsers) browsers=true ;;
        --help|-h)
            echo 'Usage: scripts/setup.sh [--external-db] [--browsers]'
            echo 'Install locked Python dependencies, preserve/create .env, initialize/start the project database, migrate and check.'
            echo '--external-db uses an already provisioned database from .env without managing a cluster.'
            echo '--browsers also installs bundled Playwright Chromium and Firefox.'
            exit 0 ;;
        *) fail "Unknown option: $option" ;;
    esac
done
require uv
if ! "$external_db"; then require_pg17; require initdb; require postgres; fi
uv sync --locked
run_uv python - "$external_db" <<'PY'
import os
import secrets
import sys
from pathlib import Path

from dotenv import dotenv_values

path = Path('.env')
if not path.exists():
    text = Path('.env.example').read_text()
    assert text.count('replace-with-generated-local-secret') == 3
    for _ in range(3):
        text = text.replace('replace-with-generated-local-secret', secrets.token_urlsafe(64), 1)
    with open(path, 'x', opener=lambda name, flags: os.open(name, flags, 0o600)) as file:
        file.write(text)
    print('Created private .env with independent secrets.')
else:
    print('Preserving existing .env.')
values = {**dotenv_values('.env'), **os.environ}
for key in ('DJANGO_SECRET_KEY', 'PIN_HASH_PEPPER', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'):
    if not values.get(key) or values[key] == 'replace-with-generated-local-secret':
        sys.exit(f'Set {key} in .env before continuing.')
if not values.get('TEST_DB_NAME', '').startswith('test_') or values['TEST_DB_NAME'] == values['DB_NAME']:
    sys.exit('TEST_DB_NAME must be a separate test_ database.')
if sys.argv[1] == 'false' and (values.get('DB_HOST', '127.0.0.1') != '127.0.0.1' or values.get('DB_PORT', '55432') != '55432'):
    sys.exit('Managed setup requires DB_HOST=127.0.0.1 and DB_PORT=55432; use --external-db for another server.')
PY
if ! "$external_db"; then
    if [[ ! -e .local/pgdata ]]; then
        run_uv python - <<'PY'
import os
import secrets
from pathlib import Path

path = Path('.local/pgadmin-password')
if not path.exists():
    with open(path, 'x', opener=lambda name, flags: os.open(name, flags, 0o600)) as file:
        file.write(secrets.token_urlsafe(40) + '\n')
PY
        mkdir -p .local/pgsocket
        initdb -D .local/pgdata --username=done_together_admin --pwfile=.local/pgadmin-password --auth-local=scram-sha-256 --auth-host=scram-sha-256 --encoding=UTF8 --locale=C
        run_uv python - <<'PY'
from pathlib import Path

socket = str(Path('.local/pgsocket').resolve()).replace("'", "''")
with Path('.local/pgdata/postgresql.conf').open('a') as file:
    file.write(f"\nlisten_addresses = '127.0.0.1'\nport = 55432\nunix_socket_directories = '{socket}'\n")
PY
    fi
    "$PROJECT_ROOT/scripts/db.sh" start
    run_uv python - <<'PY'
import os
import sys
from pathlib import Path

import psycopg
from dotenv import dotenv_values
from psycopg import sql

v = {**dotenv_values('.env'), **os.environ}
params = dict(host='127.0.0.1', port=55432)
# Existing working application credentials need no administrator access or changes.
try:
    with psycopg.connect(**params, user=v['DB_USER'], password=v['DB_PASSWORD'], dbname=v['DB_NAME'], connect_timeout=3):
        print('Existing application database is accessible; preserving role and data.')
        sys.exit(0)
except psycopg.OperationalError:
    pass
with psycopg.connect(**params, user='done_together_admin', password=Path('.local/pgadmin-password').read_text().strip(), dbname='postgres', autocommit=True) as connection:
    if not connection.execute('SELECT 1 FROM pg_roles WHERE rolname = %s', (v['DB_USER'],)).fetchone():
        connection.execute(sql.SQL('CREATE ROLE {} LOGIN CREATEDB NOSUPERUSER NOCREATEROLE NOREPLICATION PASSWORD {}').format(sql.Identifier(v['DB_USER']), sql.Literal(v['DB_PASSWORD'])))
    if not connection.execute('SELECT 1 FROM pg_database WHERE datname = %s', (v['DB_NAME'],)).fetchone():
        connection.execute(sql.SQL('CREATE DATABASE {} OWNER {}').format(sql.Identifier(v['DB_NAME']), sql.Identifier(v['DB_USER'])))
# Never reset an existing role password to repair a mismatch.
with psycopg.connect(**params, user=v['DB_USER'], password=v['DB_PASSWORD'], dbname=v['DB_NAME'], connect_timeout=3):
    print('Application database is accessible.')
PY
fi
run_uv python manage.py migrate
run_uv python manage.py check
if "$browsers"; then run_uv playwright install chromium firefox; fi
echo 'Setup complete. Run scripts/dev.sh to start the app, email capture and scheduler.'
