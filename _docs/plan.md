# Product specification — Done Together

Status: Scope confirmed by the user on 2026-10-28, including proposed defaults P-01–P-07. Technology choices remain undecided.

## Problem and intended outcome

Help families with children remember which chores need doing and when, through a shared household board in computer web browsers synchronized across computers. Parents assign and review work; children consult the board and submit their own chores using PINs.

Success is demonstrated by verified household setup, assignment, submission, review, recurrence, and weekly-progress journeys. Approvals must award exactly one star, recurrence must avoid duplicate unfinished work, and connected boards must update automatically within a few seconds. No adoption or commercial success targets are specified for release one.

## Users and context

- Parents have separate email/password accounts and equal household management rights.
- Children have profiles and four-digit PINs, without email accounts.
- A parent signs in to open each shared computer board. The board remains visible for children when parent controls lock.
- The primary environment is a connected computer browser. While offline, the last board remains visible with changes disabled.
- Household data is private to its members. A child PIN authorizes only that child's submissions.

## First release scope

Included: household setup, second-parent invitations, verified accounts and password recovery, children and PIN management, a shared board and protected parent settings, one-off and daily/selected-weekday recurring chores, fixed assignments, submissions, approval and returns with notes, retained completion history, weekly/all-time stars, automatic synchronization, and read-only offline viewing.

Excluded:

- Automatic assignment rotation or open claiming.
- Sounds, reminder notifications, variable star values, and reward redemption.
- Holiday/illness pauses and missed-occurrence backlogs.
- A phone-specific management experience or separate parent dashboard.
- Offline editing and child/account/household deletion controls.
- A separate history-browsing screen; older completed history is retained but hidden from the main board.

Invitation, verification, and password-recovery emails are included account functions. They are separate from excluded reminder notifications. Hosting, distribution, implementation technology, and public launch are not selected or authorized here.

## Terms and state rules

A chore definition specifies the child assignment and date or recurring schedule. An occurrence is the dated work submitted and reviewed. Occurrence states are **to do**, **awaiting approval**, and **completed**. A parent return restores **to do** with an explanation. Overdue is a date-based indicator.

A recurring definition has at most one unfinished occurrence, including awaiting-approval work. Missed scheduled dates do not accumulate. Scheduling uses the household timezone; overdue labels interpret each assigned calendar date as ending at midnight in the viewing computer's local timezone. Computers may therefore show different overdue labels for the same shared occurrence.

Weekly totals and visible completions use Monday 00:00 until the next Monday 00:00 in the household timezone, based on approval time.

## User journeys

### J-01: Set up the household

A parent registers, verifies their email, creates a household with a scheduling timezone, adds children and their PINs, and sets their own parent PIN. They invite the second parent by email; the intended recipient registers or signs in and joins through the invitation. A parent signs in on additional computers to open the same board. Invalid credentials or invitations deny access with recoverable errors. An expired invitation can be replaced. An empty board guides the parent to add children and chores.

### J-02: Assign and maintain work

A parent selects their identity and enters their PIN to unlock board controls. They create a titled chore assigned to one child, with a one-off date or daily/selected-weekday schedule. Invalid input leaves data unchanged. Recurring edits affect future occurrences only; deleting recurrence removes unfinished work and stops future occurrences while retaining completions and stars. One-off edit/deletion follows P-03 below.

### J-03: Submit and review

A child enters their PIN and submits an assigned chore. It becomes awaiting approval. A parent unlocks controls and approves it, awarding one star, or returns it with a required explanation. A returned chore can be submitted again. Invalid PINs cannot change state. Repeated or concurrent approvals cannot award additional stars. An on-time submission does not become overdue while awaiting review; returning it after its deadline makes it overdue again.

### J-04: Follow recurring work and progress

Each child's column shows active work and this week's completions together, plus weekly and all-time stars. An unfinished recurring chore remains one item over multiple scheduled days. On approval, skipped dates do not become a backlog. If today is scheduled, today's work appears separately; otherwise the next occurrence waits for the next scheduled day. Late completion never shifts the fixed schedule. Weekly rollover hides older completions without deleting history or all-time stars.

### J-05: Recover access or connectivity

Protected settings let a parent reset a child's PIN. A parent resets their own parent PIN using their own account password, or recovers their password through email. Parent controls lock after one minute of inactivity while the board stays visible. Disconnection preserves the last board with offline status and disables mutations. Reconnection refreshes shared data automatically before changes resume. Failed requests must not appear successful.

## Requirements

Every requirement is in scope for release one. Numerical limits and edge rules are defined in the confirmed defaults below.

| ID | Required behavior or quality | Source / rationale | Observable acceptance condition |
| --- | --- | --- | --- |
| REQ-001 | Separate parent email/password accounts, verified email, email-based password recovery. | Source; D-05 | Verified parents can sign in; unverified accounts cannot access household data; password recovery invalidates the old password; invalid/expired links deny access. |
| REQ-002 | Household creation and second-parent email invitation with expiry and single use. | Source; D-05 | Intended verified recipient joins once; wrong-address, reused, and expired invitations fail; an expired invitation can be replaced. |
| REQ-003 | Equal parent rights and household data isolation. | D-04; private household context | Either member parent can manage the household; outsiders cannot read or change it through UI or direct requests. |
| REQ-004 | Manage child names, four-digit child PINs, and own parent PIN. | Source | Protected settings add children/reset child PINs; own password authorizes own parent PIN reset; replaced PINs fail. Four-digit PINs preserve leading zeroes. |
| REQ-005 | Either parent can select their identity and unlock board/settings controls with their own PIN. | Source; D-04 | Either valid parent PIN unlocks management; child/incorrect PINs and locked requests cannot perform parent actions. |
| REQ-006 | Lock parent controls after 60 seconds of parent inactivity while keeping the board visible. | Source | After 60 seconds, management requires a PIN again. Board viewing and child activity do not extend parent access. |
| REQ-007 | Temporarily throttle repeated incorrect passwords and PINs. | D-05 | Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits. |
| REQ-008 | One board column per child; distinguish due, overdue, awaiting approval, and completed states visually. | Source | Mixed-state assignments appear under the correct child; states are understandable without color alone; empty states guide setup. |
| REQ-009 | Show all active work and this week's completions without a collapsed completed section. | Source; D-02 | Older overdue work remains visible; current-week completions are directly accessible; older completions leave the column but remain stored. |
| REQ-010 | Assign one-off dated and daily/selected-weekday recurring chores to specific children. | Source | Parent can create each type; missing/invalid title, child, or date/schedule cannot create partial work. Children cannot claim or reassign work. |
| REQ-011 | Use household timezone for scheduling and each computer's local timezone for overdue labels; no individual due times. | Source; D-01 | Different-timezone computers agree on occurrence identity and dates but may show different overdue labels at the same instant. |
| REQ-012 | At most one unfinished occurrence per recurring definition; skip missed dates. | Source; D-03 | Leaving daily work unfinished over several days, including awaiting approval, produces one outstanding item and no backlog after approval. |
| REQ-013 | Late approval preserves fixed recurrence and creates today's work separately when scheduled. | Source; D-03 | Approving overdue Monday work on scheduled Wednesday completes Monday and creates Wednesday once; an unscheduled approval day waits for the next scheduled day. |
| REQ-014 | Recurring edits apply only to future occurrences. | Source | Editing title, assignment, or schedule leaves current occurrence details and completed history unchanged; subsequent occurrences use the edit. |
| REQ-015 | Recurring deletion removes unfinished work and prevents future occurrences without erasing completions/stars. | Source | Deleting a definition removes to-do/awaiting-approval work and stops recurrence; prior approvals/history/star totals persist. |
| REQ-016 | A child PIN permits submission of that child's assigned work only. | Source | Correct PIN moves eligible work to awaiting approval; incorrect/another child's PIN or duplicate requests cannot create unauthorized transitions. |
| REQ-017 | Parent can approve or return with a required note; returned work can be resubmitted. | Source | Approval completes work; empty return note is rejected; valid return shows the note and restores to-do; child can retry. |
| REQ-018 | On-time submissions remain non-overdue while awaiting review; late returns become overdue. | Source | Submission before deadline remains non-overdue after it while awaiting approval; return after deadline restores overdue. Apply P-04 timeliness classification. |
| REQ-019 | Award exactly one star per approved occurrence regardless of effort. | Source | Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none. |
| REQ-020 | Show weekly and all-time totals using approval time and the household week. | Source; D-02 | Monday approval counts in the new week even for Sunday work; weekly rollover preserves history and all-time totals. |
| REQ-021 | Automatically synchronize accepted changes across connected boards within a few seconds. | Source | Two-computer checks cover children, chores, submissions, reviews, and totals without manual refresh; confirmed target is five seconds (P-06). |
| REQ-022 | Show last synchronized board offline, indicate disconnection, disable changes until resynchronized. | D-06 | Disconnect preserves visible board and disables actions; reconnect refreshes data automatically before actions resume. |
| REQ-023 | Handle failed/concurrent actions without false success, lost incompatible edits, or duplicate work. | Shared-board failure handling | Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed. |
| REQ-024 | Shared board and protected parent settings are the main screens; visual reminders only. | Source | Chores/reviews are managed on the board; accounts/children/PINs in settings; no separate dashboard, sounds, or reminder notifications are required. |
| REQ-025 | Persist household data, completed history, and stars across computers, reloads, sign-outs, and restarts. | Source; D-07 | Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded. |
| REQ-026 | Accessible core interactions and usable computer browser layouts. | Proposed quality baseline | Core journeys work with keyboard and visible focus, labeled inputs, and text status equivalents; agreed browser/viewport/zoom checks pass. |
| REQ-027 | Keep credentials and household information private. | Account safeguards | Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions. |

## Data and integrations

- Parent accounts: email, verification state, protected password and parent PIN credentials, household membership.
- Household: membership and scheduling timezone. Child profiles: display names and protected PINs; no child email or birth date is required.
- Chore definitions: title, child assignment, date or schedule. Occurrences: captured details, due date, state, submission/review times, return note, approval/star record. Definition edits preserve current-occurrence details and completed history.
- Access records: invitations, verification/recovery links, and signed-in sessions; their implementation belongs in architecture.
- Emails, credentials, PINs, child names, household activity, and notes are private household data. Use synthetic fixtures and examples; keep real personal information and secrets out of source and logs.
- Completion history/stars have no first-release age limit. Broader data removal, retention, and operational responsibilities must be revisited before public launch; product deletion controls cover chores only.
- Account email delivery is needed for verification, invitation, and recovery. Failed requests/delivery must offer a recoverable error. Provider, credentials, storage, and synchronization technology are undecided.

## Constraints and confirmed defaults

The user confirmed P-01–P-07 with the complete first-release scope on 2026-10-28. These defaults are binding product decisions.

| ID | Confirmed default | Impact |
| --- | --- | --- |
| P-01 | One household per parent account, at most two parents per household; no parent removal/ownership transfer in release one. | Account and membership boundaries; REQ-002/003. |
| P-02 | Set household timezone at creation, suggested from the creating computer; no timezone-changing controls in release one. | Stable schedules/week boundaries; REQ-011/020. |
| P-03 | One-off chores can be edited/deleted while to do; awaiting-approval work must first be returned before editing/deletion. Completed work cannot be edited/deleted. Recurring deletion retains its explicit source behavior. | One-off lifecycle missing from source; REQ-010/017/025. |
| P-04 | A late submission remains visibly overdue while awaiting approval. Classify submission timeliness using the submitting computer's local date and preserve that classification across computers until return/resubmission. | Cross-timezone on-time status; REQ-018. |
| P-05 | Invitations expire after seven days; verification/recovery links after one hour. Five consecutive incorrect attempts impose a five-minute restriction on the targeted account/PIN identity across computers; successful authentication clears failures. | Concrete safeguard limits; REQ-001/002/007. Architecture must address malicious lockout attempts. |
| P-06 | Synchronization target: five seconds under normal connectivity. Test current stable Chrome and Firefox at minimum 1280×720, keyboard navigation, and 200% browser zoom. | Measurable quality gates; REQ-021/026. |
| P-07 | A new recurring chore first becomes due on its first scheduled date on/after creation. After a gap with no unfinished occurrence, create only the latest scheduled occurrence due by today, never a backlog. Scheduling must not require a browser to remain open. | Initialization/recovery semantics; REQ-010–013. |

Budget, hosting environment, backup/recovery arrangements, operational security, distribution, and tooling remain for architecture discussion before affected setup tasks become Ready. No stack has been selected.

## Recorded user answers

Answered on 2026-10-28 during this discovery conversation:

| ID | Question | User answer | Requirements |
| --- | --- | --- | --- |
| D-01 | Scheduling across different timezones? | Use a household timezone for scheduling; keep overdue labels local. | REQ-011 |
| D-02 | Weekly stars and visible completions? | Monday through Sunday in the household timezone, counted when approved. | REQ-009/020 |
| D-03 | Missed dates after late approval? | Skip missed dates; create today's occurrence if scheduled, otherwise wait for the next scheduled day. | REQ-012/013 |
| D-04 | Whose PIN unlocks the shared board? | Either parent selects their identity and enters their own PIN; both have equal control. | REQ-003/005 |
| D-05 | Account safeguards? | Include verified email, email password recovery, expiring single-use invitations, and temporary throttling after repeated incorrect password/PIN attempts. | REQ-001/002/007 |
| D-06 | Disconnection behavior? | Keep last board visible, show offline status, disable changes until reconnected. | REQ-022 |
| D-07 | Deletion controls? | Delete chores only; child profiles, accounts, and household data removal remain outside release one. | REQ-015/025 |

## Open questions and assumptions

| ID | Question or assumption | Impact | Owner / resolution |
| --- | --- | --- | --- |
| Q-001 | Confirm or amend P-01–P-07. | Account boundaries, one-off lifecycle, scheduling, and security limits. | Resolved: user confirmed all defaults on 2026-10-28. |
| Q-002 | Confirm the complete first-release scope in this specification. | Gates origin inspection and task/issue synchronization. | Resolved: user said “Confirm the scope” on 2026-10-28. |
| A-001 | Done Together is a provisional product name. | Reversible display wording. | Documented assumption. |
| A-002 | Retain older completed history without adding a separate history screen. | Avoid unrequested screen. | Interpretation included in scope review. |

## Concrete delivery tasks

After scope confirmation, inspect only the remote named `origin` to select local or GitHub backlog mode under [process.md](process.md). For a GitHub origin, create/update one issue per concrete task, use [task-template.md](task-template.md), link requirement IDs, and synchronize issue bodies, local task files, and [tasks.md](tasks.md). Do not publish questions/placeholders. The linked local tasks remain Draft pending architecture selection and grooming; they are not Ready or authorization to implement.

| Candidate | Requirement links | Product dependency |
| --- | --- | --- |
| [Account registration, verification, sign-in, recovery, and safeguards](tasks/001-accounts.md) | REQ-001/007/027 | Environment setup and runnable skeleton after architecture selection |
| [Household creation, timezone setup, and second-parent invitation](tasks/002-households.md) | REQ-002/003/011/027 | Accounts |
| [Child profiles, parent/child PIN management, and protected shared access](tasks/003-pins.md) | REQ-004–007/027 | Household/accounts |
| [Shared board, empty states, and settings navigation](tasks/004-board.md) | REQ-008/009/024/026 | Household, children, protected controls |
| [One-off chore assignment and maintenance](tasks/005-one-off-chores.md) | REQ-010/011/025 | Board and children |
| [Recurrence, occurrence generation, future edits, and deletion](tasks/006-recurrence.md) | REQ-010–015/025 | Assignment and household timezone |
| [Child submission, parent review, returns, and overdue rules](tasks/007-review.md) | REQ-016–019/023 | Chores and protected access |
| [Weekly/all-time stars and completion visibility](tasks/008-stars.md) | REQ-009/019/020/025 | Review lifecycle |
| [Synchronization, concurrent-action handling, and offline recovery](tasks/009-synchronization.md) | REQ-021–023 | Shared household workflows |
| [Integrated release verification and browser/accessibility checks](tasks/010-release-verification.md) | REQ-001–027 | All release features |

Cross-cutting isolation, persistence, accessibility, concurrency, and credential protection belong in each affected feature's acceptance criteria, not solely final verification. Refine the existing environment-setup and dependent application-skeleton tasks after architecture selection; do not create placeholder issues for their unresolved template content.

## Review

- Discovery date: 2026-10-28.
- User decisions D-01–D-07 and defaults P-01–P-07 confirmed by the user on 2026-10-28.
- Blocking product questions: None. Architecture decisions remain separate.
- Architecture undecided; no application code written.
- Origin checked after confirmation: `git@github.com:Alex-Yu/done-together.git`; GitHub backlog mode selected. Tasks 001–010 are synchronized with GitHub issues #1–#10; see [tasks.md](tasks.md).
