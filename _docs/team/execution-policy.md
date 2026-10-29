# Token-saving execution policy

Approved by the user on 2026-10-29. Applies when delivery resumes; it does not resume a paused goal or change product scope, acceptance criteria, retry limits or release gates.

## Agent lifecycle and context

- Create a fresh developer and independent QA for each new task. Do not reuse the previous task's agent threads. Keep the same agents for fixes within the current task; retire them after successful integration. Retiring means no further dispatch to those threads, not deleting branches, worktrees, evidence or live processes.
- Spawn with no inherited conversation (`fork_turns: "none"` where supported). Pass task/role/specification links, exact branch and revision, relevant decisions/findings, commands, counters and the expected deliverable. Do not paste the full conversation, backlog history or raw logs.
- Read the current checkpoint and relevant linked sources. Follow AGENTS.md's required reading, but do not repeatedly reload unchanged documents during the same task. Persist decisions in repository documents so fresh agents can find them.
- Reuse the existing PM scope review when the task/specification is unchanged and only dependency completion remains. The coordinator checks dependencies and records Ready, citing that grooming commit. Invoke a fresh PM only for missing grooming, consequential ambiguity, changed scope/contracts or defects requiring task refinement. Do not spawn a PM just to repeat an existing review.
- A fresh coordinator chat should start from [resume.md](../resume.md). The current chat cannot erase its own history; the user must open a fresh chat. Checkpoint before changing sessions, and prevent two coordinators from writing concurrently.

## Models and reasoning

Set both model and reasoning explicitly when the runtime supports them. Do not inherit a costly reasoning setting accidentally.

| Role | Model | Reasoning |
| --- | --- | --- |
| Coordinator | Current coordinator model | Low |
| PM / routine documentation | `gpt-6-luna` | Low |
| Developer | Current development model | Medium |
| Routine task QA | `gpt-6-luna` | Medium |
| Difficult security, concurrency or defect investigation | Current development/review model | High, limited to the difficult work |
| Final release QA and requirements review | Current development/review model | High |

If an exact setting is unavailable, report it; do not silently substitute another model. Changing the current coordinator's UI model/reasoning may require the user to select it. These are execution instructions, not a claim that account/global settings have been changed.

## Verification and output

- Developer, QA and integration checks target the changed behavior and affected regressions. Preserve every acceptance criterion, including relevant failure, authorization and concurrency cases. Existing task-specific mandatory checks still apply.
- Reuse prior executed evidence only after identifying its revision and confirming the relevant code/configuration/environment is unchanged. Explain the retained evidence briefly. Changes or failures require fresh affected checks.
- Do not replay account email, real inactivity waits or complete browser journeys for unrelated tasks. Run the full integrated regression, complete supported-browser journeys and requirements review at final release. There is no separate per-task orchestrator requirements re-check.
- Keep one concise verification record: revision, AC-to-evidence table, commands/counts and findings. Link earlier evidence instead of copying it.
- Store verbose, sanitized logs/screenshots under ignored `.local/verification/<task>/` or another documented ignored directory. Never commit raw logs, credentials or private fixtures. Return only verdict, exact commit, test counts, evidence path and blockers (normally under 150 words).
- Batch independent reads and checks when safe. Never overlap suites sharing a disposable database. Wait on confirmed live handles; do not restart work merely because observation times out. Use the longest permitted event-driven wait rather than frequent polling, and avoid waiting-only messages where client instructions allow.

## Bookkeeping and boundaries

- Batch related documentation/status edits and issue updates at meaningful handoffs: readiness/start, implementation review, QA result/fix routing, and integrated completion. Avoid separate writes for each sentence or redundant readback; verify each actual external update.
- Keep the implementation commit immutable for QA. Add evidence/completion records in the next necessary commit. Do not create a commit only to insert its own hash; record known implementation/grooming/QA hashes, and record the delivery hash in the next normal checkpoint.
- Keep the current checkpoint concise; link detailed historical handoffs instead of copying them into each prompt. Persist attempts before long QA runs and before stopping. Do not weaken traceability, GitHub reconciliation or push authorization rules to save tokens.
- Preserve the user's existing autonomous delivery scope and batch limits. No new per-task approval or one-task stop rule is introduced. A paused goal resumes only on explicit user instruction.
