# Verification planning

Use this directory for scenario plans when a feature needs preparation beyond its task's verification plan. Plans define expected behavior; they are not executed evidence or PASS verdicts.

1. Read the current task criteria, [product specification](../../plan.md), [architecture](../../architecture.md) and authoritative issue. Resolve scope conflicts before execution.
2. Map every criterion to observable success, failure and boundary checks. Include synthetic households, unauthorized clients, calendar/DST boundaries and independent PostgreSQL transactions where relevant.
3. At QA handoff, use the exact implementation revision and real selectors/commands from [testing](../../testing-guidelines.md). Run suites sharing a test database sequentially; never substitute SQLite for concurrency.
4. Record actual expected/observed results with the [verification template](../../templates/verification.md), browser/environment versions and honest single-host/multi-host provenance. Missing required checks are BLOCKED; failures are FAIL. QA does not modify code or criteria.

Keep credentials, private links and generated browser/mail artifacts out of committed evidence. Store verbose sanitized artifacts under ignored `.local/verification/`.
