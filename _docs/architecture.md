# Architecture

## Stack and structure

A Django 5.2 monolith on Python 3.13 uses PostgreSQL 17, server-rendered templates, vendored HTMX and small JavaScript modules. `uv.lock` fixes Python dependencies. There is no Node build, Redis, Celery or WebSocket service.

| Path | Responsibility |
| --- | --- |
| `config/`, `manage.py` | Settings, URLs and server entry points |
| `accounts/` | Parent accounts, allauth integration, PIN credentials, authority and authentication limits |
| `households/` | Membership, invitations, children and household timezone |
| `chores/` | Definitions, occurrence snapshots, submissions, review, approvals and recurrence scheduler |
| `board/` | Household-scoped read model, board views and snapshots |
| `templates/`, `static/` | HTML, CSS, JavaScript and pinned HTMX |
| `scripts/` | Bash setup, development service supervision and sequential test commands |
| `tests/`, `tools/` | Automated tests and local browser/mail verification helpers |

## State and integrity

Views validate requests and call shared transactional services. Writers lock household → definition → occurrence where applicable. PostgreSQL constraints enforce one household per parent, at most two household members, unique definition/date occurrences, one unfinished occurrence per recurring definition and one approval per occurrence.

Definitions hold schedules; occurrences capture title, assignment, due date, state, version and submission/review details. Recurring edits change future snapshots. Deleting recurrence removes unfinished work; completed occurrences survive through nullable definition references. Protected approval records represent exactly one star each; totals are derived rather than stored as mutable counters.

Approval completes an occurrence, creates its unique award and reconciles recurrence in one transaction. Stale versions return an explicit conflict and current scoped data. Independent PostgreSQL transactions are required to test races; SQLite cannot verify these contracts.

Instants are stored in UTC. Calendar schedules and Monday week boundaries use the IANA household timezone, including DST. Overdue uses browser-local dates. Submission timeliness uses the server receipt instant in the validated browser timezone and remains fixed while awaiting review; browser clock values are not trusted.

`reconcile_recurrence` runs independently of browsers every 60 seconds. It creates only the latest eligible date when no unfinished work exists. Late approval skips missed dates and creates today's work only if scheduled and not already completed. Reconciliation is idempotent across overlapping runs, restarts and connection failures.

## Accounts and authority

Verified membership grants board viewing. Parent mutations additionally require a server-side per-session unlock identifying a household parent. Authority expires after 60 seconds without accepted parent activity; polling, passive viewing and child activity do not renew it. Credential versions revoke prior unlocks after PIN changes. Own PIN recovery checks the selected parent's account password.

Child PINs authorize only that child's submissions. PINs preserve four ASCII digits, including leading zeroes. A namespaced HMAC using `PIN_HASH_PEPPER` feeds salted Argon2 hashing; plaintext PINs are never stored. PostgreSQL identity counters enforce five failures/five-minute restriction across processes; supplementary source throttles limit abuse. Attempts during restriction do not extend the deadline.

Allauth provides email-only login and mandatory verification. Verification/recovery links expire after one hour; recipient-bound, single-use invitations expire after seven days. Private links exchange tokens for session-bound flows before form submission. Token-bearing URLs are redacted from ordinary logs, private responses are no-store, and mutations require CSRF and server-side scope checks.

## Synchronization and offline recovery

Board writers atomically increment a household revision. `/snapshot/` reads a consistent scoped snapshot under the household lock. Two-second polling updates changed regions while preserving open forms, drafts, focus and version fields. Week and authority markers refresh time-dependent state without mutations; local-date timers update overdue labels.

Failures preserve the open board, show disconnection and disable writes. Reconnection requires a fresh authorized snapshot before mutations resume. POSTs are never optimistically committed, queued or automatically retried; lost responses require reconciliation with server state. Confirmed authorization loss clears private content. No service worker or persistent private browser cache is used.

## Operations

Local development runs PostgreSQL, Django, Mailpit and the recurrence command as separate processes. Settings load ignored `.env`; tests use isolated PostgreSQL and in-memory email. HTMX is served locally; provenance is in its [vendor README](../static/vendor/htmx/README.md).

Production needs an HTTPS host, email provider, scheduler supervision, restricted database roles, backups/restore checks, monitoring and operational ownership. These are not configured by the local release.
