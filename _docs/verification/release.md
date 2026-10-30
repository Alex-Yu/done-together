# Local release verification

Historical result: **PASS**, 2026-10-29. This summarizes the recorded release checks; it is not a new test run.

- Verified implementation: `dc456af4aa16f03ee03e8dcc21fe3c5346cab3c3`.
- Integrated delivery on `develop`: `374c2ad42d1ac4b40bb111fc31bf3ed4cf1b66d2`; only documentation differed from the verified implementation.
- Independent final QA and requirements review covered REQ-001–027, defaults P-01–P-07 and all five core journeys.

| Coverage | Recorded result |
| --- | --- |
| Unit/PostgreSQL server tests | 166 passed, including concurrency and actual no-browser scheduler/restart checks |
| Bundled Chromium/Firefox | 8 unique cases passed |
| Installed Chrome/Firefox | 13 native tests passed, including 4 complete keyboard journeys at 100%/200% zoom |
| Focus verifier | 12 positive/negative controls passed |
| Synchronization | 36 events across 9 mutation classes; 0.9949–1.9487 seconds, under the 5-second target |
| Mail and persistence | Actual loopback SMTP, invitations, 61-second parent inactivity and app restart/revisit checks passed |
| Integration | 28 affected tests passed; migration, system, drift, lint, format and diff checks passed |

Environment: macOS x86_64, Python 3.13.15, Django 5.2.18, PostgreSQL 17.11, installed Chrome 156.0.8078.48 and Firefox 159.0. Independent browser profiles ran on one Mac; this was not a two-physical-computer test. Data was synthetic and mail was loopback-only.

The first final-QA attempt failed a stale bundled PIN assertion and a native Firefox focus assertion. Corrected verification code passed fresh affected QA: both bundled PIN cases, all native tests and focus controls. Unchanged server/SMTP/restart evidence was retained after revision/configuration comparison; the original failures were not counted as passes.

Detailed historical matrices, findings and logs are referenced in the documentation at final-record commit `9e36f21`. The final QA record was committed at `a1c0752baa0ccdb92554e67ffd8ce587844781f7`. For example:

```sh
git show 9e36f21:_docs/verification/010-release-integration.md
git show a1c0752:_docs/verification/010-release-qa-attempt-2.md
```

Use [testing instructions](../testing-guidelines.md) to verify later changes. This local result does not certify production hosting, external mail, backups or deployment.
