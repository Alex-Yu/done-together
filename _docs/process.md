# Development process

## Sources of truth

The product plan defines intended behavior; architecture and decision records define agreed constraints. Tasks describe scoped changes and link to these sources. `_docs/tasks.md` identifies the single authoritative backlog. If these sources conflict, resolve the conflict before dependent implementation. An implementation is not evidence that a requirement changed.

## Lifecycle

`Draft → Ready → In progress → In review → Done`

Use `Blocked` when a task cannot proceed; record the reason, required input, and prior state. After resolution, return to the appropriate prior state. QA failure returns a task to `In progress`; changed requirements return it to `Draft` for review.

1. **Discover:** clarify users, outcomes, scope, constraints, and important failure cases in the plan. Ask focused questions rather than inventing product choices.
2. **Design:** compare stack and architecture options, record the selection, and identify environment setup work. Refine the task labeled `environment-setup` and the application skeleton task so the developer installs and configures the environment before creating the runnable skeleton. Record intended commands now and validate them during those tasks. Keep these decisions separate from product requirements.
3. **Prepare:** decompose work into small tasks with dependencies and requirement links. Groom each task before implementation.
4. **Ready gate:** goal, acceptance criteria, exclusions, constraints, and verification plan are complete; dependencies are done; blocking questions are resolved; scope is reviewed by the decision owner. Record that review in the task. A task may configure commands as its explicit deliverable.
5. **Implement:** take one ready task, implement within its scope, run appropriate checks, and complete its handoff. Move it to `In review`; do not declare it done based only on implementation tests.
6. **Verify:** check the result against every acceptance criterion and record reproducible evidence using the verification template. Prefer a fresh reviewer/session; record when the same assistant performs both roles. QA reports findings without modifying the implementation.
7. **Complete:** all criteria pass, required checks pass, documents match the agreed behavior, and unresolved material findings are addressed. The coordinator or project owner marks it `Done`. Commit according to the user's instructions.

## Changes and defects

When scope changes, update the specification first, assess affected tasks and prior verification, and record significant decisions. Preserve requirement identifiers. A defect within agreed scope returns to the engineer with reproduction steps. New behavior becomes a separate task. Keep evidence tied to the verified revision; relevant code changes invalidate the affected verdicts.

## Bounded work loops

A loop is optional and requires a defined task set, measurable completion condition, and a time, cost, or attempt budget agreed with the user. Do not assume a tool-specific goal command exists.

For each iteration, select the next unblocked ready task, implement it, verify it, and update its state. On QA failure, return the evidence to implementation and reverify after changes. Stop when the selected tasks are Done, the budget is reached, no eligible task remains, or a decision or required environment blocks progress. Report incomplete work honestly. Do not expand scope, retry indefinitely, or treat a blocked task as complete.

## Roles and orchestration

Role guides live in `_docs/team/`. A single assistant may follow them in separate passes. If the user chooses multiple agents, an orchestrator hands off task/specification links, constraints, revision information, and verification evidence. Dependent tasks remain sequential. Parallel work requires independent tasks and isolated changes. Role documents describe responsibilities; they do not activate an agent system.
