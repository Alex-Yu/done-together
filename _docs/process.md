# Development process

## Sources of truth

[plan.md](plan.md) defines product behavior; [architecture.md](architecture.md) defines implementation contracts. [tasks.md](tasks.md) records the backlog, current checkpoint, counters and authorized delivery scope. GitHub issues hold mapped task scope/status; local task documents mirror them. Resolve conflicts before dependent implementation.

## Feature delivery

Start this workflow when the user hands over an agreed feature or release for delivery. Routine maintenance remains scoped to the request. Use the [role guides](team/orchestrator.md) and [execution policy](team/execution-policy.md).

1. **Specify:** clarify the requested outcome, scope, failures and data handling. Update requirements and architecture for agreed changes, preserving existing requirement IDs. Record significant new decisions using the [decision template](templates/decision.md).
2. **Prepare:** PM creates or refines a small task using the [task template](task-template.md), linking requirements, dependencies, exclusions, acceptance criteria and verification. Use `Draft → Ready → In progress → In review → Done`; record a blocker with the required input and prior state.
3. **Ready:** resolve consequential questions, complete dependencies and obtain a PM scope review. Reuse a valid unchanged review when only dependency completion remains; record its grooming commit. Do not ask the user to approve routine tasks already within the agreed scope.
4. **Implement:** a fresh developer implements one Ready task on its task branch, runs affected checks and supplies an immutable implementation commit plus concise handoff. Keep the same developer for fixes.
5. **Verify:** independent QA reads every acceptance criterion before the implementation summary, executes applicable checks and records expected/observed evidence using the [verification template](templates/verification.md). QA changes neither code nor criteria. FAIL returns to the developer; changed implementation requires fresh affected QA. Missing evidence is BLOCKED.
6. **Complete:** after independent QA PASS, the orchestrator records Done, commits completion records, integrates into `develop` and runs affected integration checks. There is no separate orchestrator requirements review per task. Integration failures return to implementation and independent affected QA before completion stands.
7. **Release:** QA verifies integrated journeys and required regression/browser/operational gates at the delivered revision. The orchestrator reviews requirements at this final release stage only. Both must PASS; failures become defect tasks and reenter the workflow within existing limits.

Use fresh task-only developer/QA contexts for new tasks, retain them for same-task fixes and retire them after integration. Prefer independent agents where supported; otherwise use distinct sequential role passes and disclose reduced independence. Use the explicit model/reasoning settings in the execution policy. Keep dependent implementation and suites sharing a database sequential.

## Changes, evidence and checkpoints

1. Update specifications before implementing agreed scope changes. Material scope/architecture changes return to the user; routine reversible choices within the agreed architecture may be handled by the developer.
2. Run targeted checks and affected regressions during tasks; use [testing](testing-guidelines.md) for commands. Full integrated checks remain required for release. Reuse prior evidence only after confirming relevant code/configuration/environment is unchanged.
3. At meaningful handoffs, record task state, exact implementation/grooming/QA revisions, findings, attempts, batch count, authorization and next action in the current checkpoint. Keep detailed evidence linked and verbose sanitized artifacts ignored under `.local/verification/`.
4. Resume from [resume.md](resume.md) and inspect actual repository/backlog state. A new chat does not reset counters or resume a paused goal. Prevent concurrent coordinators from writing the same delivery.

## Limits and autonomy

Default limits remain three developer-to-QA attempts per task and ten completions per delivery batch, unless the user changes them. Each implementation submitted to QA consumes an attempt. Preserve historical counts and obtain an explicit extension before exceeding an existing limit; session changes do not reset them.

The coordinator handles routine handoffs, fixes and completion within authorized scope. Ask only for consequential unresolved decisions, scope changes, missing access or required authorization. Continue independent eligible work when possible. Stop at verified completion, an execution limit or no eligible work, recording unfinished states and the next action. A paused goal resumes only on explicit user instruction.

## Branching, commits, merges, and pushes

During delegated delivery:

1. Use `develop` as the integration branch. If absent, create it from the agreed project base; resolve ambiguity first.
2. PM commits new grooming on `develop`, or on the existing task branch for fixes, and records the full hash before handoff. Reuse valid prior grooming rather than repeating it.
3. Developer branches from `develop` as `task/<id>-<title>` and commits implementation/fixes there. Keep that branch for same-task fixes. Stage only related work and preserve unrelated changes.
4. QA verifies the immutable recorded implementation commit. Later evidence/status commits must not alter implementation; code changes invalidate affected verdicts.
5. After QA PASS, the orchestrator commits completion records, merges to `develop` (fast-forward preferred), runs integration checks and records the delivery revision. Fixes during integration require fresh affected QA.
6. Push only to explicitly authorized remotes/branches. Delivery handover does not authorize source pushes. Without authorization, finish locally. Never force push, rewrite published history or delete branches without authorization.

Outside delegated delivery, leave changes reviewable and uncommitted unless instructed otherwise. User instructions override defaults. Deployment, external messages and destructive actions require authorization.

## GitHub issue synchronization

1. Inspect only `origin` to choose GitHub or local backlog mode. A missing/non-GitHub/ambiguous origin uses local tasks and no GitHub writes. Record the choice in [tasks.md](tasks.md).
2. For authorized GitHub delivery, PM maps one issue per concrete task, with requirement links and the local task path. Reuse existing mapped issues; do not publish unresolved questions or placeholders. Confirm external-write authorization before updates.
3. Read authoritative issue changes before grooming/implementation and at handoffs. Reconcile scope conflicts rather than overwriting them. Synchronize scope, criteria, status and evidence at meaningful handoffs; verify actual updates.
4. Keep issues open until verified integration succeeds; then close. Reopen if implementation returns to In progress. On synchronization failure, record the pending update and next action; do not create replacement issues. Reconcile before dependent work.
