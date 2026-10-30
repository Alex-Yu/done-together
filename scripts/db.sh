#!/usr/bin/env bash
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
case "${1:-help}" in
    help|--help|-h) echo 'Usage: scripts/db.sh {start|status|stop}'; exit 0 ;;
    start|status|stop) [[ $# -eq 1 ]] || fail 'Expected one database action.' ;;
    *) fail 'Usage: scripts/db.sh {start|status|stop}' ;;
esac
require_pg17
[[ -f .local/pgdata/PG_VERSION ]] || fail 'No project cluster. Run scripts/setup.sh.'
[[ "$(cat .local/pgdata/PG_VERSION)" == 17 ]] || fail 'Project cluster is not PostgreSQL 17.'
if [[ "$1" == status ]]; then exec pg_ctl -D .local/pgdata status; fi
require postgres
[[ "$(postgres -D .local/pgdata -C port)" == 55432 ]] || fail 'Project cluster must use port 55432.'
[[ "$(postgres -D .local/pgdata -C listen_addresses)" == 127.0.0.1 ]] || fail 'Project cluster must bind only to 127.0.0.1.'
if [[ "$1" == start ]]; then
    if pg_ctl -D .local/pgdata status >/dev/null 2>&1; then
        echo 'Project PostgreSQL is already running.'
    else
        pg_ctl -D .local/pgdata -l .local/postgresql-server.log -w start
    fi
else
    if pg_ctl -D .local/pgdata status >/dev/null 2>&1; then
        pg_ctl -D .local/pgdata -w stop -m fast
    else
        echo 'Project PostgreSQL is already stopped.'
    fi
fi
