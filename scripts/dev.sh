#!/usr/bin/env bash
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
action="${1:-run}"
case "$action" in
    help|--help|-h)
        echo 'Usage: scripts/dev.sh [run|web|mail|scheduler|once|health|migrate|static|driver]'
        echo 'run starts app, Mailpit and scheduler together; Ctrl-C stops these processes.'
        echo 'Database controls: scripts/db.sh {start|status|stop}'
        exit 0 ;;
    run|web|mail|scheduler|once|health|migrate|static|driver) [[ $# -le 1 ]] || fail 'Expected one action.' ;;
    *) fail "Unknown action: $action. See scripts/dev.sh --help." ;;
esac
if [[ "$action" == health ]]; then
    require curl
    exec curl --fail --silent --show-error http://127.0.0.1:8000/health/
fi
if [[ "$action" == driver ]]; then
    require geckodriver
    exec geckodriver --host 127.0.0.1 --port 4445 --allow-system-access --log error
fi
require_env
require uv
case "$action" in
    web) exec uv run --locked python manage.py runserver 127.0.0.1:8000 --noreload ;;
    mail)
        require mailpit
        exec mailpit --listen 127.0.0.1:8025 --smtp 127.0.0.1:1025 --database .local/mailpit.db --disable-version-check --smtp-disable-rdns --block-remote-css-and-fonts ;;
    scheduler) exec uv run --locked python manage.py reconcile_recurrence --loop --interval 60 ;;
    once) exec uv run --locked python manage.py reconcile_recurrence --once ;;
    migrate) exec uv run --locked python manage.py migrate ;;
    static) exec uv run --locked python manage.py collectstatic --noinput ;;
esac
require mailpit
require curl
# Manage only the repository cluster; an external database must already be running.
if [[ -f .local/pgdata/PG_VERSION ]] && uses_project_database; then "$PROJECT_ROOT/scripts/db.sh" start; fi
for port in 8000 8025 1025; do port_available "$port"; done
children=()
cleanup() {
    trap - EXIT INT TERM
    for pid in ${children[@]+"${children[@]}"}; do kill -TERM "$pid" 2>/dev/null || true; done
    for pid in ${children[@]+"${children[@]}"}; do wait "$pid" 2>/dev/null || true; done
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
for service in mail web scheduler; do
    "$PROJECT_ROOT/scripts/dev.sh" "$service" &
    children+=("$!")
done
printf 'App: http://127.0.0.1:8000/\nEmail: http://127.0.0.1:8025/\nCtrl-C stops app, email and scheduler; the database stays running.\n'
for attempt in {1..100}; do
    for pid in ${children[@]+"${children[@]}"}; do kill -0 "$pid" 2>/dev/null || fail 'A service exited; see its output above.'; done
    if curl --fail --silent http://127.0.0.1:8000/health/ >/dev/null; then break; fi
    [[ "$attempt" -lt 100 ]] || fail 'Application did not become healthy within 20 seconds.'
    sleep 0.2
done
echo 'Application is ready.'
while :; do
    for pid in ${children[@]+"${children[@]}"}; do kill -0 "$pid" 2>/dev/null || fail 'A service exited; stopping the remaining services.'; done
    sleep 1
done
