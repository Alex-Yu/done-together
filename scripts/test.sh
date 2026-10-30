#!/usr/bin/env bash
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
suite="${1:-server}"
if [[ $# -gt 0 ]]; then shift; fi
case "$suite" in
    help|--help|-h)
        echo 'Usage: scripts/test.sh [checks|unit|server|browser|native|all|mail|mail-revisit|pytest] [pytest arguments]'
        echo 'Default: checks plus all unit/integration tests. all adds bundled and macOS native browsers.'
        echo 'native/mail start and stop their own geckodriver; mail modes require the running app and Mailpit.'
        echo 'Examples: scripts/test.sh server -k review; scripts/test.sh pytest tests/integration/test_review.py -q'
        exit 0 ;;
    checks|unit|server|browser|native|all|mail|mail-revisit|pytest) ;;
    *) fail "Unknown suite: $suite. See scripts/test.sh --help." ;;
esac
case "$suite" in checks|all|mail|mail-revisit) [[ $# -eq 0 ]] || fail "$suite takes no extra arguments." ;; esac
require_env
require uv
# Guard script-driven suites sharing Django's disposable database.
lock="$PROJECT_ROOT/.local/test-suite.lock"
mkdir "$lock" 2>/dev/null || fail 'Another scripted test suite is running. If it was killed, verify it stopped before removing .local/test-suite.lock.'
printf '%s\n' "$$" > "$lock/pid"
driver_pid=''
test_pid=''
run_uv() {
    # Job control gives the child normal SIGINT handling instead of Bash's
    # ignored background-job SIGINT, which scheduler subprocesses inherit.
    set -m
    uv run --locked "$@" <&0 &
    test_pid=$!
    set +m
    local result=0
    wait "$test_pid" || result=$?
    test_pid=''
    return "$result"
}
cleanup() {
    trap - EXIT INT TERM
    if [[ -n "$test_pid" ]]; then
        # Each test command owns a job-control group. Interrupt the entire
        # group so pytest can tear down subprocesses and its test database.
        kill -INT -- "-$test_pid" 2>/dev/null || true
        wait "$test_pid" 2>/dev/null || true
    fi
    if [[ -n "$driver_pid" ]]; then
        kill -TERM "$driver_pid" 2>/dev/null || true
        wait "$driver_pid" 2>/dev/null || true
    fi
    rm -f "$lock/pid"
    rmdir "$lock"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
checks() {
    run_uv python manage.py check
    run_uv python manage.py makemigrations --check --dry-run
    run_uv ruff check .
    run_uv ruff format --check .
}
server() { run_uv pytest tests/unit tests/integration -q "$@"; }
browser() {
    RUN_NATIVE_BOARD=0 RUN_NATIVE_CHORES=0 RUN_NATIVE_RECURRENCE=0 RUN_NATIVE_REVIEW=0 \
    RUN_NATIVE_STARS=0 RUN_NATIVE_SYNC=0 RUN_NATIVE_RELEASE=0 \
    run_uv pytest tests/e2e --browser chromium --browser firefox -q "$@"
}
start_driver() {
    [[ "$(uname -s)" == Darwin ]] || fail 'The current native helpers require macOS.'
    [[ -d '/Applications/Google Chrome.app' && -x /Applications/Firefox.app/Contents/MacOS/firefox ]] || fail 'Install Chrome and Firefox in /Applications for native checks.'
    require geckodriver
    require curl
    port_available 4445
    "$PROJECT_ROOT/scripts/dev.sh" driver > .local/geckodriver.log 2>&1 &
    driver_pid=$!
    for attempt in {1..50}; do
        kill -0 "$driver_pid" 2>/dev/null || fail 'geckodriver exited; inspect .local/geckodriver.log.'
        if curl --fail --silent http://127.0.0.1:4445/status >/dev/null; then return; fi
        sleep 0.2
    done
    fail 'geckodriver did not become ready; inspect .local/geckodriver.log.'
}
native() {
    start_driver
    RUN_NATIVE_BOARD=1 RUN_NATIVE_CHORES=1 RUN_NATIVE_RECURRENCE=1 RUN_NATIVE_REVIEW=1 \
    RUN_NATIVE_STARS=1 RUN_NATIVE_SYNC=1 RUN_NATIVE_RELEASE=1 \
    run_uv pytest tests/e2e/test_board_native.py tests/e2e/test_chores_native.py \
        tests/e2e/test_recurrence_native.py tests/e2e/test_review_native.py \
        tests/e2e/test_stars_native.py tests/e2e/test_sync_native.py \
        tests/e2e/test_release_keyboard_native.py -q -s "$@"
}
case "$suite" in
    checks) checks ;;
    unit) run_uv pytest tests/unit -q "$@" ;;
    server) checks; server "$@" ;;
    browser) browser "$@" ;;
    native) native "$@" ;;
    all) checks; server; browser; native ;;
    pytest) run_uv pytest "$@" ;;
    mail|mail-revisit)
        require curl
        curl --fail --silent http://127.0.0.1:8000/health/ >/dev/null || fail 'Start scripts/dev.sh before mail checks.'
        curl --fail --silent http://127.0.0.1:8025/api/v1/messages >/dev/null || fail 'Mailpit is unavailable.'
        start_driver
        if [[ "$suite" == mail-revisit ]]; then
            run_uv python tools/verify_account_mail.py --revisit
            run_uv python tools/verify_pin_browsers.py --revisit
        else
            run_uv python tools/verify_account_mail.py
            run_uv python tools/verify_pin_browsers.py
        fi
        ;;
esac
