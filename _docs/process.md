# Development process

## Sources of truth

The product plan defines intended behavior; architecture and decision records define agreed constraints. Tasks describe scoped changes and link to these sources. `_docs/tasks.md` identifies the single authoritative backlog. If these sources conflict, resolve the conflict before dependent implementation. An implementation is not evidence that a requirement changed.

## Lifecycle

`Draft → Ready → In progress → In review → Done`

Use `Blocked` when a task cannot proceed; record the reason, required input, and prior state. After resolution, return to the appropriate prior state. QA failure or an unmet requirement found by the orchestrator returns a task to `In progress`; changed requirements return it to `Draft` for review.

1. **Discover:** clarify users, outcomes, scope, constraints, and important failure cases in the plan. Ask focused questions rather than inventing product choices.
2. **Design:** compare stack and architecture options, record the selection, and identify environment setup work. Refine the task labeled `environment-setup` and the application skeleton task so the developer installs and configures the environment before creating the runnable skeleton. Record intended commands now and validate them during those tasks. Keep these decisions separate from product requirements.
3. **Prepare:** decompose work into small tasks with dependencies and requirement links. Groom each task before implementation.
4. **Ready gate:** goal, acceptance criteria, exclusions, constraints, and verification plan are complete; dependencies are done; blocking questions are resolved; scope is reviewed by PM against the product scope agreed by the decision owner. From README step 4 onward, the orchestrator accepts this review without separate user approval for each task. Record that review in the task. A task may configure commands as its explicit deliverable.
5. **Implement:** take one ready task, implement within its scope, run appropriate checks, and complete its handoff. Move it to `In review`; do not declare it done based only on implementation tests.
6. **Verify:** check the result against every acceptance criterion and record reproducible evidence using the verification template. Prefer a fresh reviewer/session; record when the same assistant performs both roles. QA reports findings without modifying the implementation.
7. **Complete:** all criteria pass, required checks pass, documents match the agreed behavior, and unresolved material findings are addressed. After QA PASS, the orchestrator re-checks the implementation against the task’s linked requirements and acceptance criteria, using evidence for the exact implementation state and running additional checks where needed. Record the re-check and evidence in the task handoff. Only the orchestrator marks it `Done`, after this re-check passes. If any in-scope requirement is unmet, return the task to `In progress` with reproducible findings for the developer, then repeat QA and the orchestrator re-check. Unverifiable requirements block completion. Merge according to the Git policy below; automatically continue only after integration succeeds.

## Changes and defects

When scope changes, update the specification first, assess affected tasks and prior verification, and record significant decisions. Preserve requirement identifiers. A defect within agreed scope returns to the engineer with reproduction steps. New behavior becomes a separate task. Keep evidence tied to the verified revision; relevant code changes invalidate the affected verdicts.

## Orchestrated delivery from README step 4

Discovery and architecture selection remain user-guided (README steps 1–3). After the user hands over delivery in step 4, the orchestrator owns the following graph:

1. PM creates dependency-ordered tasks, refines the task labeled `environment-setup` and the application skeleton task, and grooms the next eligible task.
2. PM reviews readiness against agreed requirements and constraints. Escalate consequential uncertainty or scope changes; do not request routine per-task user approval.
3. Developer implements one Ready task, including installation and configuration where required, runs applicable checks, and records an exact revision or working-tree handoff.
4. QA verifies that implementation against every criterion and required check. PASS proceeds to the completion gate. FAIL returns findings to the developer, followed by fresh verification of the changed implementation. BLOCKED is routed to the developer for technical remediation, PM for product ambiguity, or the user for unavailable decisions/access.
5. After QA PASS, the orchestrator re-checks the implementation against the task’s linked requirements and acceptance criteria and records evidence in the handoff. Unmet requirements return the task to In progress and the developer, followed by fresh QA and another orchestrator re-check. Unverifiable requirements block completion. Only after the re-check and all completion conditions pass does the orchestrator mark Done and automatically select the next eligible task.
6. When release tasks are Done, QA checks the integrated application against complete product journeys and required regression checks. Failures become defect tasks and reenter the graph. Final delivery requires PASS against the delivered code state.

Use separate PM, developer, and QA subagents when supported. Otherwise use explicit sequential role passes and record reduced reviewer independence. The orchestrator coordinates rather than replacing a missing QA verdict with its own assertion. Dependent work remains sequential; parallel work requires independent tasks and isolated changes, followed by integration verification.

## Autonomy and limits

Handle routine reversible choices, grooming, handoffs, fixes, and task-state updates without prompting the user. Respect agreed architecture, requirements, and dependency constraints. Ask only about consequential uncertainty, changes outside agreed scope or architecture, missing access/credentials, required authorization, or exhausted limits. Continue other eligible work when a task is blocked. Do not repeat already answered questions or expand scope silently.

Default limits are three developer-to-QA attempts per task and ten task completions per delivery batch, unless the user specifies alternatives. Each implementation handoff submitted to QA consumes an attempt. Session changes and batch renewal do not reset task retry counts; obtain an explicit extension before exceeding them. Honor additional user time/cost limits and tool restrictions. Do not assume a tool-specific goal command or automatic continuation is available.

Stop at verified completion, an execution limit, or no eligible work. Record a delivery checkpoint in `_docs/tasks.md` after handoffs and before stopping: agreed task set, current role/task, exact implementation state, per-task attempt counts, batch completions, evidence links, blockers, and next routing action. Keep detailed findings in linked task handoffs and verification records. On resume, read these records and reverify evidence invalidated by intervening changes.

Role guides in `_docs/team/` describe responsibilities; they do not themselves launch an agent runtime. Local delivery commits and merges follow the Git policy below. Pushes, other external actions, and deployment remain subject to the user's authorization.

## Branching, commits, merges, and pushes

This default applies to application delivery after README step 4. Explicit user instructions take precedence. Template maintenance remains uncommitted unless requested.

- Use `develop` as the delivery branch and record it in `_docs/tasks.md`. If it does not exist, the orchestrator creates it from the existing project default branch before task work begins; ask only if that starting point is ambiguous. Record any user-authorized push remote and branch targets. Missing push authorization does not block local delivery.
- The developer creates one branch per task from the current `develop` branch, named `task/<task-id>-<short-title>` (for example, `task/003-short-title` or `task/environment-setup`). Reuse that branch for fixes. Use isolated worktrees when needed; preserve unrelated changes and never include them in task commits.
- The developer commits implementation and fixes on the task branch with concise messages identifying the task and change. Run applicable checks before handoff and record the branch and full commit hash. No per-commit user approval is needed within agreed delivery scope.
- QA verifies the recorded implementation commit. The orchestrator re-checks that same commit against requirements before marking Done. Implementation changes require a new commit and fresh affected verification. Evidence and status-only commits may follow; record both the verified implementation commit and final branch tip, and ensure these later commits contain no implementation changes.
- After the re-check passes, the orchestrator records Done, commits the completion records, and merges the task branch into `develop`. Prefer a fast-forward when possible; otherwise preserve history with a merge commit. Run applicable integration checks on the resulting delivery state before selecting dependent work. If integration changes implementation, conflicts require fixes, or checks fail, return the task to In progress and the developer, followed by fresh QA and orchestrator re-check. Record the final merge/delivery commit and evidence.
- Push automatically only when the user has authorized the remote and target branches, and only within that authorization. A delivery handover alone does not authorize pushes. Existing authorization persists until changed; do not ask again for each permitted push. Without it, retain local commits and report that they have not been pushed. A push failure does not invalidate local verification; record the pending push separately.
- Do not force push, rewrite published history, delete remote branches, or perform destructive Git operations without explicit authorization. Preserve task branches by default. Do not bypass repository protections or required checks.

A task is ready for dependent work only when its verified implementation has been integrated successfully. Record task branch, verified implementation commit, final branch tip, delivery commit, integration results, and push status in its handoff. Final release QA verifies the recorded integrated delivery commit.
