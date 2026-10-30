#!/usr/bin/env bash
# Shared environment; sourced by the executable scripts.
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
mkdir -p .local
export UV_CACHE_DIR="${UV_CACHE_DIR:-$PROJECT_ROOT/.local/uv-cache}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PROJECT_ROOT/.local/playwright}"
export PATH="$PROJECT_ROOT/.local/postgresql/bin:$PROJECT_ROOT/.local/bin:/opt/homebrew/opt/postgresql@17/bin:/usr/local/opt/postgresql@17/bin:$PATH"

fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Missing $1. See scripts/install-tools.sh and _docs/commands.md."; }
run_uv() { require uv; uv run --locked "$@"; }
require_env() { [[ -f .env ]] || fail 'Missing .env. Run scripts/setup.sh first.'; }
require_pg17() {
    require pg_ctl
    [[ "$(pg_ctl --version)" == *' 17.'* ]] || fail 'PostgreSQL 17 tools are required.'
}
port_available() {
    run_uv python - "$1" <<'PY'
import socket
import sys

with socket.socket() as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listener.bind(('127.0.0.1', int(sys.argv[1])))
    except OSError:
        sys.exit(f'Port {sys.argv[1]} is occupied; stop only a service you own.')
PY
}
uses_project_database() {
    run_uv python - <<'PY'
import os
import sys

from dotenv import dotenv_values

values = {**dotenv_values('.env'), **os.environ}
sys.exit(0 if (values.get('DB_HOST', '127.0.0.1'), values.get('DB_PORT', '55432')) == ('127.0.0.1', '55432') else 1)
PY
}
