# Architecture and implementation choices

Status: Core approach selected by the user on 2026-10-28: Django + PostgreSQL + HTMX. The design below records the recommended implementation baseline; dependency patches and local installation details remain unverified until bootstrap tasks run. Delivery has not been handed over and no scaffolding is authorized by this record.

## Options considered

| Approach | Benefits | Costs / reason for selection or rejection |
| --- | --- | --- |
| Django + PostgreSQL + HTMX | One application owns permissions, transactions, scheduling, and HTML; suits forms and shared board workflows. | Selected. Requires an application server and independent scheduler; polling generates regular requests. |
| Next.js / TypeScript + Supabase | Interactive React UI; managed accounts, database, and realtime services. | Custom PIN authorization still needed; application logic and database policies require coordinated verification; more provider integration. |
| React + separate Django API + PostgreSQL | Explicit API for multiple clients and richer frontend behavior. | Additional API contracts, client state, and build tooling are not justified by the browser-only first release. |

No existing team language preference was supplied. The selection favors maintainability and verification of the approved first release rather than speculative clients. Provider costs and operating budget have not been estimated or approved.

## Selected approach

- Python 3.13, Django 5.2 LTS on a supported security patch, PostgreSQL 17 on a supported patch. These are intended compatible baselines, not observed installations. Setup records exact resolved versions and locks dependencies. Revisit upgrades before support expires; Django 5.2 extended support ends April 2028.
- Server-rendered Django templates, locally served pinned HTMX, plain CSS, and small JavaScript modules for local dates, inactivity, focus-safe updates, and connectivity. No separate frontend build system or Node.js toolchain is required.
- Django sessions/authentication, django-allauth for account verification/recovery, psycopg for PostgreSQL. Household invitations, PIN authorization, identity lockouts, and their exact expiry rules are application responsibilities.
- PostgreSQL is the authoritative store in development, tests, and eventual operation. Do not substitute SQLite for transaction/concurrency verification.
- A two-second board-version poll with conditional content refresh targets accepted changes appearing within five seconds under normal connectivity. This is a design target, not measured evidence.
- An independent scheduler process invokes an idempotent Django management command at least once per minute; approval also reconciles recurrence inside its transaction. No Redis, Celery, or WebSocket service is initially required.
- Local tools: uv, pytest/pytest-django, pytest-playwright, Ruff, Mailpit, Git, GitHub CLI, current stable Chrome and Firefox. Native macOS services are the intended local baseline; containers are optional, not required. See [commands.md](commands.md).
- Hosting, distribution, production email provider, production process manager, backups, recovery objectives, operational ownership, and budget remain open. No provider provisioning or deployment is authorized.

## Structure and boundaries

These are intended paths, to be created only during the appropriate implementation tasks:

| Path | Responsibility |
| --- | --- |
| `manage.py`, `config/` | Django entry point, URLs, environment-specific settings, server entry points |
| `accounts/` | Parent accounts, verification/recovery integration, sessions, PIN credentials and shared authentication limits |
| `households/` | Membership, invitations, children, immutable household timezone, authorization helpers |
| `chores/` | Definitions, occurrence snapshots, submissions/reviews, approval records, recurrence service and management command |
| `board/` | Household-scoped read model, board/settings views, version polling and HTML fragments |
| `templates/`, `static/` | Accessible templates, CSS, first-party JavaScript and pinned vendored HTMX |
| `tests/unit/`, `tests/integration/`, `tests/e2e/` | Domain boundaries, real PostgreSQL behavior, browser journeys |
| `pyproject.toml`, `uv.lock`, `.python-version` | Runtime/tool dependency constraints and reproducible resolution |

Views validate input and call shared domain services; scheduled work calls the same recurrence service. Transactions belong in domain services so direct requests and scheduler execution enforce the same invariants. Django admin is not a substitute for the specified parent settings and must not provide a bypass on shared boards.

## Contracts and data

- A parent has at most one household; a household has at most two parents. Joining an invitation locks the relevant membership/household records and consumes a recipient-bound, expiring, single-use token atomically.
- Definitions store schedules; occurrences capture title, child assignment, due calendar date, state, version, submission classification/timestamps, return note, and approval time. Edits to recurrence affect future snapshots only. Retain completion snapshots and approval records when definitions are deleted; avoid cascading away earned history.
- Enforce unique definition/due-date occurrence identity, a conditional uniqueness constraint for one unfinished recurring occurrence, and a unique approval record per occurrence. Every accepted approval creates one durable star record atomically. Totals are derived from approval records, using approval time and household Monday boundaries.
- Serialize approval, recurrence generation, edits, and deletion using a consistent lock order (definition before occurrence when applicable). Locking plus database constraints protects against concurrent requests and scheduler overlap. Return explicit conflict responses for incompatible stale versions, then refresh the board. Retried requests cannot create additional awards or occurrences.
- Store instants in UTC and schedules/due dates as calendar dates interpreted with IANA household timezone data. Use Python timezone facilities for scheduling and weekly boundaries. Browser-local dates control overdue labels. Preserve submission timeliness across computers according to P-04; the submitting browser supplies its timezone context, while the server uses the receipt instant to avoid trusting a submitted clock value. Validate the timezone context. Local timezone is user-controlled, as in the approved product rule.
- Recurrence implements P-07 on creation and recovery. On approval, create today's occurrence once if scheduled and distinct from the completed occurrence; never repeat today's already completed occurrence or create skipped dates as backlog. Scheduler catch-up creates only the latest eligible date when no unfinished occurrence exists. Test timezone/DST boundaries and gaps with no browsers open.
- Same-origin HTML endpoints and version polling use household-scoped reads; mutation endpoints use POST with CSRF protection. Every mutation validates membership, role/PIN authority, current state, input, and version on the server. Validation failures leave data unchanged; stale state is an explicit conflict; unauthorized or expired authority denies access. Never expose credential hashes or access tokens in board fragments.
- Maintain a household board revision, advanced atomically for every change affecting board content. Consistent snapshots include a revision. Refresh only changed regions, preserving focused controls, open forms and unsaved input. Recompute local overdue labels and household-week visibility across time boundaries even without a mutation. Polling must not count as parent activity.

## Authentication, privacy, and recovery

- A verified parent account opens a household board. This board session grants viewing only until a parent unlock or a valid child submission authorizes the corresponding action. An unlocked parent identity may differ from the parent who opened the board, but must be a member of that household.
- Store a short-lived parent unlock server-side per board session, with selected parent identity and last accepted parent activity. Enforce expiry on every protected request after 60 seconds. Only explicit parent activity while unlocked extends it; polling, board viewing, and child actions do not. Client-side locking improves feedback but is not the authority. Own-password PIN resets must verify the selected parent's password.
- Use maintained password hashing, including salted PIN hashes that preserve four-digit strings and leading zeroes; keep additional PIN hashing secret material outside the database/source. Child PINs authorize only that child's submission request and do not establish a parent session. Never persist plaintext credentials or log PIN input.
- Keep atomic per-identity authentication failure counters in PostgreSQL across processes/computers: five consecutive failures impose five minutes of restriction; successful authentication clears failures when permitted. Require household board access before PIN attempts, use generic account errors and supplementary source/request throttling, and prevent attempts during restriction from extending the deadline. This reduces targeted lockout abuse but cannot eliminate it while preserving P-05's identity-wide restriction.
- Enforce one-hour verification/recovery links and seven-day single-use invitations. Do not assume package defaults match P-05. Consume access links safely and redact their tokens from logs. Use secure HttpOnly session cookies, CSRF checks and HTTPS in any deployed environment; local HTTP is loopback-only.
- Keep email, child names, notes and activity out of routine logs; use synthetic fixtures. Local account emails go only to loopback Mailpit. External email delivery must surface recoverable failures; email success is not inferred merely from successful local rendering.
- On failed polls/requests, preserve the displayed board, show connection status, and disable changes. Browser network hints alone do not prove server readiness. Reconnect must fetch a fresh authorized snapshot before mutations resume. Never queue offline writes or display an unconfirmed mutation as committed. A lost response may follow a committed action; reconciliation must safely reveal the server result.
- Offline scope is preservation of the currently open board. No service worker or persistent browser cache of private household data is introduced. Clear the board on sign-out or a confirmed authorization failure. Offline reload/startup is not promised by this design.

## Verification and operations

Unit tests cover schedules, timeliness, transitions and weekly boundaries. PostgreSQL integration tests cover competing approvals, uniqueness, deletion races, membership limits, lockout sharing, access-link consumption, and direct unauthorized requests. Browser journeys cover two independent sessions, five-second synchronization, 60-second parent expiry, focus preservation, offline/reconnect behavior, and visible failure handling. Include current stable Chrome and Firefox at 1280×720, keyboard-only use and 200% zoom; Playwright's Firefox build does not replace checking stable Firefox manually.

The scheduler must operate without browsers and recover safely after downtime. Local setup proves database connectivity and mail capture without scaffolding; the skeleton then proves HTTP/database readiness. Production readiness requires explicit later decisions on HTTPS hosting, continuous scheduling, email delivery, restricted database roles, backups/restore tests, log redaction, monitoring and responsibility. These unresolved operations do not block isolated local bootstrap tasks, but block affected provisioning/deployment work.

## Decisions

- [ADR-001: Django monolith with PostgreSQL and HTMX](decisions/001-django-postgresql-htmx.md)
- [ADR-002: Transactional state, recurrence and approval integrity](decisions/002-transactional-workflows.md)
- [ADR-003: Shared-board authority, polling and offline recovery](decisions/003-shared-board-access-and-sync.md)

## References

- [Django support periods](https://www.djangoproject.com/download/) and [Python compatibility](https://docs.djangoproject.com/en/5.2/faq/install/).
- [Django transactions](https://docs.djangoproject.com/en/5.2/topics/db/transactions/) and [constraints](https://docs.djangoproject.com/en/5.2/ref/models/constraints/).
- [HTMX polling](https://htmx.org/docs/#polling) and [django-allauth configuration](https://docs.allauth.org/en/latest/account/configuration.html).

## Account implementation details — task001

Allauth65.21.0 uses email-only login/mandatory verification with DB confirmation records and supported adapter/view/token-generator hooks for exact one-hour expiry and safe link consumption. PostgreSQL identity failure rows enforce P05; separate HMAC-keyed source windows permit60 account POSTs per60seconds using REMOTE_ADDR, replacing process-local allauth cache limits. This supplementary limit is a routine security default and does not replace five failures/five minutes.

Private verification URLs exchange their key into a session-bound nonce flow before rendering a form. Original token responses use no-referrer; token-free forms/ordinary pages use same-origin, since blanket no-referrer makes native browser POSTs send Origin:null and fail CSRF. All account responses are no-store; request/CSRF log filters redact original keys, flow identifiers and all account query strings. DB/SMTP failures return generic recoverable responses. See task001 evidence; household/PIN integration remains subsequent work.

## Household implementation details — task002

Membership has a unique parent and a household slot constrained to1/2 with a household/slot uniqueness constraint, enforcing P01 even for competing transactions. Creation locks the parent; invitation acceptance locks parent→household→invitation. Both members use identical membership-scoped authority; there is no owner privilege. Until task003, verified membership protects the bootstrap settings/invitation UI; task003 supplies parent PIN authority while retaining verified create/join bootstrap.

Private invitations store only a SHA256 digest of a32-byte random token, expire after exactly seven days, and exchange into a session/nonce-bound join flow before CSRF-protected POST consumption. New/superseding invitation state rolls back if local SMTP delivery fails. Successful sends redirect to GET, preventing reload from resending. Household timezone is validated IANA, browser-suggested and immutable; no change controls exist. Account privacy/source-limit middleware also covers household bootstrap routes, including no-store and redacted private paths/queries.

## PIN and parent-authority implementation details —003

PINs remain exact ASCII four-digit strings. Identity/type-namespaced HMAC-SHA256 with the outside-database pepper feeds Django’s salted Argon2 hasher; no plaintext PIN can be read back. Selected-parent first/own reset verifies that member’s exact account password via the shared account limiter. Parent/child PIN identities reuse the atomic limiter independently.

BoardAuthority stores only a session-key HMAC plus household/selected parent/credential version/last activity. Each protected request checks active verified membership, version and60-second expiry; successful parent POSTs alone touch activity. Explicit events inside unlocked parent controls may send throttled CSRF activity, never timers/polls/global/child events. Reset/grant locks user→credential, with credential versions revoking old grants. Existing household management is now parent guarded; verified creation/join and password-authorized own PIN recovery remain bootstrap. Full board004 and child submission007 remain later integrations.

Task004 board presentation contract: `board.read_model` produces ordered real household-child columns with active and current-week-completed card collections. The production work provider remains empty until persisted definitions/occurrences005–006, review007 and approval-derived week visibility008 integrate. Synthetic mixed states are patched internally by tests only; HTTP never selects a fixture/provider. Verified household members enter their shared board from `/`; settings retains003 parent authority. No separate dashboard or fake production work/totals.

Task005 one-off contract: `chores.Definition` and `Occurrence` persist household-scoped dated assignments and captured details. Protected board forms validate nonblank titles (200-character storage bound), a household child and ISO calendar date; past dates are allowed. One-off edits update both definition and occurrence, including reassignment, only in to-do with the submitted occurrence version. Deletes remove only the eligible to-do definition/occurrence. Awaiting/completed states are protected; completed fixtures remain retained until actual reviews/approval projection007–008. Household lock→definition→occurrence plus an atomic `F` revision increment serialize accepted changes; stale versions return409 with current scoped board and an instruction to reopen. Browser-local calendar comparison supplies to-do overdue text, including midnight/DST; no due time or recurrence/approval workflow is introduced.

Task006 recurrence contract: definitions distinguish one-off/daily/selected-weekday schedules and store a household-local `eligible_from` calendar cursor plus an edit version. Occurrences retain independent captured details. PostgreSQL additionally permits at most one unfinished occurrence per definition; the existing definition/date uniqueness prevents re-creating completed dates. Shared services lock household→definition→occurrence. The scheduler reconciles only the latest eligible scheduled date when no unfinished work exists. Completion advances the cursor to the approval calendar date before reconciling, so skipped dates never appear after late approval and a completed date cannot recur. `complete_occurrence` is a transaction-owning domain boundary, with no HTTP route in006;007 must call it inside the same outer transaction as its protected approval and unique award, retaining definition-first lock order. Recurring edits change only the definition; deletion removes unfinished occurrences and hard-deletes the definition while completed occurrences survive via SET_NULL. Existing007/008 approval/star integration obligations remain unchanged.

`reconcile_recurrence --once` reports committed creations or a generic nonzero retryable database error. `--loop --interval 60` closes stale connections before each run, logs generic database failure without private details, retries on the next interval, and handles Ctrl-C cleanly. A partly successful run is safely idempotent on retry. It runs independently of HTTP/browser requests; production supervision remains undecided.

## Implemented review boundary —007

Child submission verifies the occurrence's captured child identity through003's shared PostgreSQL PIN limiter before entering the state transaction. Failure counters remain committed if a later stale/state/assignment check denies the transition. Submission never grants or touches parent authority. The transition serializes household→definition→occurrence and rechecks version/state/assignment. A server receipt instant interpreted in the validated submitting browser IANA timezone determines the stored P-04 late flag; browser clock input is ignored. Return clears the flag so browser-local overdue applies again; resubmission recomputes it.

Selected-parent protected review uses the same lock order. Approval calls006 completion/reconciliation and creates a protected one-to-one Approval in one atomic transaction. Each durable approval represents exactly one star, with UTC approval time and selected parent; no mutable star counter exists. Rollback removes completion, recurrence and award together. Recurring deletion retains the completed occurrence through SET_NULL and the approval through PROTECT.008 owns aggregate/week projection.

## Implemented progress projection —008

The household-scoped board read model derives weekly/all-time stars from unique durable Approval records, including retained completed snapshots after recurrence deletion. It includes every active occurrence and only approvals in the current household-local Monday00:00 to next Monday00:00 interval; calendar boundaries account for167/169-hour DST weeks. Due/submission dates and viewer timezone do not determine membership. Each board read recomputes the interval without requiring a mutation;009 owns periodic idle refresh. Each child column exposes plain-text weekly and all-time totals, with current completions directly in its ordinary chore list. No mutable counter, history screen, expiry or credential-bearing response is introduced.


## Implemented synchronization/recovery boundary —009

Household-scoped `/snapshot/` GET serializes revision, columns, recurring-schedule HTML, authority state and household-week marker under the same household row lock used by every board-affecting writer. Child mutations now share this lock and atomic revision increments; child-name forms retain the original revision and reject stale overwrites. Snapshot keys include week/authority state, so idle Monday/expiry refresh without mutations; unchanged keys return metadata without replacement. Browser-local overdue retains its idle timer and recalculates after region updates.

Two-second polling replaces only columns/schedule regions, preserving separate open forms, drafts and version fields. Disconnection/500/unreachable preserve the in-memory view, announce read-only state and disable writes; online hints require a fresh authorized snapshot. POSTs never optimistically update or queue/retry. Unknown outcomes keep the submitted form disabled and instruct a board result check. Confirmed snapshot authorization failure clears private content. Parent expiry preserves drafts/board and disables protected controls without passive activity renewal. Validation rendering disposes prior polling/timers/listeners. No service worker or persistent private browser cache is added. Same-host independent native profiles meet the user-approved evidence gate; measured36 events are below five seconds, without claiming two physical computers. See [009 developer](verification/009-synchronization-developer.md).
