# Testing

Tests use synthetic data, `config.settings.test`, in-memory email and the disposable `TEST_DB_NAME` from `.env`. Its name must start with `test_` and differ from `DB_NAME`; the role needs `CREATEDB`. Scripted suites take a shared lock to prevent simultaneous database tests. Do not run separate raw pytest processes concurrently.

## Server checks

1. Complete [local setup](commands.md#first-time-setup). PostgreSQL must be running; a separate app, Mailpit or scheduler is unnecessary for pytest.
2. Run the routine checks and server suite:

   ```sh
   ./scripts/test.sh
   ```

   This runs Django checks, migration drift, Ruff lint/format and all unit/integration tests. The full suite includes real PostgreSQL races, a 60-second no-browser scheduler loop, shutdown/restart and connection-failure checks; allow several minutes.
3. For narrower verification, select a suite or test file:

   ```sh
   ./scripts/test.sh checks
   ./scripts/test.sh unit
   ./scripts/test.sh server -k review
   ./scripts/test.sh pytest tests/integration/test_review.py -q
   ```

## Bundled browsers

1. Install Playwright Chromium and Firefox once:

   ```sh
   ./scripts/setup.sh --browsers
   ```

2. Run both bundled browsers:

   ```sh
   ./scripts/test.sh browser
   ```

   Tests start their own live server with isolated data. Installed-native modules are disabled in this suite; bundled Firefox does not establish stable Firefox coverage.

## Installed Chrome and Firefox

Native helpers currently require macOS, installed Chrome and `/Applications/Firefox.app/Contents/MacOS/firefox`.

1. Install Chrome and Firefox in `/Applications`. Install geckodriver, if missing:

   ```sh
   ./scripts/install-tools.sh --native
   ```

2. Run the complete native suite:

   ```sh
   ./scripts/test.sh native
   ```

   The script starts geckodriver on 4445 with the required `--allow-system-access` flag, waits for readiness and stops its driver afterward. The port must be free. Driver output goes to `.local/geckodriver.log`. No separate app or Mailpit is required.
3. Inspect meaningful screenshots under `.local/` and record browser versions. Coverage includes 1280×720, 100%/200% native zoom, complete keyboard journeys, focus/labels, draft preservation, offline recovery and synchronization. Independent sessions on one host meet the agreed setup; state that provenance explicitly.

Use `./scripts/test.sh all` to run checks, server tests, bundled browsers and native browsers sequentially after their prerequisites are installed. Allow several minutes.

## Actual email, inactivity and restart

These helpers create synthetic records in the **local application database**, unlike pytest's disposable data.

1. Install the native browser prerequisites above, then start the development stack in another terminal:

   ```sh
   ./scripts/dev.sh
   ```

2. Exercise real Mailpit delivery, invitations and 61-second parent inactivity:

   ```sh
   ./scripts/test.sh mail
   ```

3. Stop the development stack with Ctrl-C and restart it using `./scripts/dev.sh`. Confirm readiness:

   ```sh
   ./scripts/dev.sh health
   ```

4. Verify stored account/household/PIN data after restart:

   ```sh
   ./scripts/test.sh mail-revisit
   ```

5. Stop the stack with Ctrl-C. Both mail commands manage their own geckodriver; keep generated `.local/` fixtures private. PostgreSQL stays running unless explicitly stopped.

## Verification standards

Verify behavior against [requirements](plan.md), including unauthorized requests, invalid/stale input and failures. Scheduling changes need midnight, DST and household-week boundaries; state changes need retry/concurrency and retained history checks. Check every acceptance criterion, not just test counts.

Record the revision or working-tree state, commands, actual results and failures/skips. Use ignored `.local/` logs/screenshots without printing credentials, cookies or private links. Missing services or skipped required checks remain unverified. Reuse earlier evidence only when relevant code and environment are unchanged.

The [release summary](verification/release.md) records historical verification. If a test process is forcibly killed, confirm it and its children stopped before manually removing a stale `.local/test-suite.lock` directory.
