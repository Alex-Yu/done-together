# Product specification

Done Together helps families manage chores on a shared board in computer browsers. Parents have separate verified email/password accounts and equal management rights. Children have names and four-digit PINs, without email accounts.

## Core journeys

1. Register and verify a parent, create a household and timezone, set a parent PIN, add children, and invite a second parent.
2. Unlock parent controls to assign dated, daily or selected-weekday chores to a child.
3. A child submits assigned work with their PIN. A parent approves for one star or returns it with an explanation; returned work can be resubmitted.
4. View all active work, this week's completions, weekly stars and all-time stars in each child's column.
5. Recover passwords by email or reset PINs in protected settings. After disconnection, retain the open board read-only until a fresh authorized refresh succeeds.

## State and calendar rules

Occurrences move from **to do** to **awaiting approval** to **completed**. Returning work restores **to do**. Overdue is a date-based indicator, not a separate state.

Scheduling uses the household timezone; overdue labels use the viewing computer's local date. Weekly totals and visible completions use approval time from Monday 00:00 to the next Monday 00:00 in the household timezone. Completed history remains stored after leaving the visible week.

A recurring definition has at most one unfinished occurrence, including work awaiting approval. Missed dates never accumulate as a backlog. Editing recurrence changes future occurrences only. Deletion removes unfinished work but preserves completions and stars.

## Requirements

| ID | Required behavior or quality | Observable acceptance condition |
| --- | --- | --- |
| REQ-001 | Separate parent email/password accounts, verified email, email-based password recovery. | Verified parents can sign in; unverified accounts cannot access household data; password recovery invalidates the old password; invalid/expired links deny access. |
| REQ-002 | Household creation and second-parent email invitation with expiry and single use. | Intended verified recipient joins once; wrong-address, reused, and expired invitations fail; an expired invitation can be replaced. |
| REQ-003 | Equal parent rights and household data isolation. | Either member parent can manage the household; outsiders cannot read or change it through UI or direct requests. |
| REQ-004 | Manage child names, four-digit child PINs, and own parent PIN. | Protected settings add children/reset child PINs; own password authorizes own parent PIN reset; replaced PINs fail. Four-digit PINs preserve leading zeroes. |
| REQ-005 | Either parent can select their identity and unlock board/settings controls with their own PIN. | Either valid parent PIN unlocks management; child/incorrect PINs and locked requests cannot perform parent actions. |
| REQ-006 | Lock parent controls after 60 seconds of parent inactivity while keeping the board visible. | After 60 seconds, management requires a PIN again. Board viewing and child activity do not extend parent access. |
| REQ-007 | Temporarily throttle repeated incorrect passwords and PINs. | Repeated failures trigger a temporary restriction, including direct requests; retry is possible after the restriction. Apply P-05 limits. |
| REQ-008 | One board column per child; distinguish due, overdue, awaiting approval, and completed states visually. | Mixed-state assignments appear under the correct child; states are understandable without color alone; empty states guide setup. |
| REQ-009 | Show all active work and this week's completions without a collapsed completed section. | Older overdue work remains visible; current-week completions are directly accessible; older completions leave the column but remain stored. |
| REQ-010 | Assign one-off dated and daily/selected-weekday recurring chores to specific children. | Parent can create each type; missing/invalid title, child, or date/schedule cannot create partial work. Children cannot claim or reassign work. |
| REQ-011 | Use household timezone for scheduling and each computer's local timezone for overdue labels; no individual due times. | Different-timezone computers agree on occurrence identity and dates but may show different overdue labels at the same instant. |
| REQ-012 | At most one unfinished occurrence per recurring definition; skip missed dates. | Leaving daily work unfinished over several days, including awaiting approval, produces one outstanding item and no backlog after approval. |
| REQ-013 | Late approval preserves fixed recurrence and creates today's work separately when scheduled. | Approving overdue Monday work on scheduled Wednesday completes Monday and creates Wednesday once; an unscheduled approval day waits for the next scheduled day. |
| REQ-014 | Recurring edits apply only to future occurrences. | Editing title, assignment, or schedule leaves current occurrence details and completed history unchanged; subsequent occurrences use the edit. |
| REQ-015 | Recurring deletion removes unfinished work and prevents future occurrences without erasing completions/stars. | Deleting a definition removes to-do/awaiting-approval work and stops recurrence; prior approvals/history/star totals persist. |
| REQ-016 | A child PIN permits submission of that child's assigned work only. | Correct PIN moves eligible work to awaiting approval; incorrect/another child's PIN or duplicate requests cannot create unauthorized transitions. |
| REQ-017 | Parent can approve or return with a required note; returned work can be resubmitted. | Approval completes work; empty return note is rejected; valid return shows the note and restores to-do; child can retry. |
| REQ-018 | On-time submissions remain non-overdue while awaiting review; late returns become overdue. | Submission before deadline remains non-overdue after it while awaiting approval; return after deadline restores overdue. Apply P-04 timeliness classification. |
| REQ-019 | Award exactly one star per approved occurrence regardless of effort. | Repeated, retried, or simultaneous approvals across computers yield one completion and one star. Submission/return earns none. |
| REQ-020 | Show weekly and all-time totals using approval time and the household week. | Monday approval counts in the new week even for Sunday work; weekly rollover preserves history and all-time totals. |
| REQ-021 | Automatically synchronize accepted changes across connected boards within a few seconds. | Two-computer checks cover children, chores, submissions, reviews, and totals without manual refresh; confirmed target is five seconds (P-06). |
| REQ-022 | Show last synchronized board offline, indicate disconnection, disable changes until resynchronized. | Disconnect preserves visible board and disables actions; reconnect refreshes data automatically before actions resume. |
| REQ-023 | Handle failed/concurrent actions without false success, lost incompatible edits, or duplicate work. | Stale reviews, deletion races, and edits produce a valid outcome or explicit conflict with refreshed data; failed actions do not appear committed. |
| REQ-024 | Shared board and protected parent settings are the main screens; visual reminders only. | Chores/reviews are managed on the board; accounts/children/PINs in settings; no separate dashboard, sounds, or reminder notifications are required. |
| REQ-025 | Persist household data, completed history, and stars across computers, reloads, sign-outs, and restarts. | Returning to the household restores data; chore deletion preserves earned history. Child/account/household deletion controls are excluded. |
| REQ-026 | Accessible core interactions and usable computer browser layouts. | Core journeys work with keyboard and visible focus, labeled inputs, and text status equivalents; agreed browser/viewport/zoom checks pass. |
| REQ-027 | Keep credentials and household information private. | Passwords/PINs cannot be read back or exposed in ordinary responses/logs; access links are private; unauthorized direct requests fail. Mechanisms are architecture decisions. |

## Confirmed defaults

| ID | Confirmed default | Impact |
| --- | --- | --- |
| P-01 | One household per parent account, at most two parents per household; no parent removal/ownership transfer in release one. | Account and membership boundaries; REQ-002/003. |
| P-02 | Set household timezone at creation, suggested from the creating computer; no timezone-changing controls in release one. | Stable schedules/week boundaries; REQ-011/020. |
| P-03 | One-off chores can be edited/deleted while to do; awaiting-approval work must first be returned before editing/deletion. Completed work cannot be edited/deleted. Recurring deletion follows REQ-015. | One-off lifecycle; REQ-010/017/025. |
| P-04 | A late submission remains visibly overdue while awaiting approval. Classify submission timeliness using the submitting computer's local date and preserve that classification across computers until return/resubmission. | Cross-timezone on-time status; REQ-018. |
| P-05 | Invitations expire after seven days; verification/recovery links after one hour. Five consecutive incorrect attempts impose a five-minute restriction on the targeted account/PIN identity across computers; successful authentication clears failures. | Concrete safeguard limits; REQ-001/002/007. Architecture must address malicious lockout attempts. |
| P-06 | Synchronization target: five seconds under normal connectivity. Test current stable Chrome and Firefox at minimum 1280×720, keyboard navigation, and 200% browser zoom. | Measurable quality gates; REQ-021/026. |
| P-07 | A new recurring chore first becomes due on its first scheduled date on/after creation. After a gap with no unfinished occurrence, create only the latest scheduled occurrence due by today, never a backlog. Scheduling must not require a browser to remain open. | Initialization/recovery semantics; REQ-010–013. |

## Scope limits

No assignment rotation, open claiming, reminder notifications, sounds, variable star values, rewards, holiday pauses, missed-work backlogs, offline editing, separate parent dashboard, separate history screen, or child/account/household deletion controls. No phone-specific management layout is promised.

Offline support retains the currently open board in memory; offline reload/startup is not supported. Two independent browser sessions on one host are accepted for synchronization verification; this does not establish behavior across two physical computers.

Private data includes accounts, credentials, invitations, child names, notes and household activity. Use synthetic development/test data. Hosting, external email delivery, backup/recovery, retention/removal operations and public launch require separate decisions.
