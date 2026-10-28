# Reusable prompts

These prompts work in ordinary chat or coding assistants. Replace placeholders with real paths or task IDs. Explicitly provide files when your assistant cannot access the repository.

## Discover the product

> Help me turn <idea> into a precise product specification using `_docs/plan.md`. Ask one focused question at a time. Explore users, journeys, outcomes, scope, failure cases, data, and constraints. Keep technology choices separate. Record confirmed answers and unresolved questions. Do not write application code.

## Choose an approach

> Read `AGENTS.md` and the product plan. Compare plausible implementation options against the requirements and constraints. Explain tradeoffs and recommend an approach. Ask for the decision before scaffolding. Record the chosen approach in `_docs/architecture.md` and significant decisions using the decision template.

## Prepare the backlog

> Read `AGENTS.md` and the agreed specifications. Create small, dependency-ordered tasks using `_docs/task-template.md` and link them from the authoritative backlog. Link requirements to tasks and define verifiable acceptance criteria. Refine the Draft task labeled `environment-setup` and the application skeleton task for the selected architecture. Assign installation and configuration to the developer in the task labeled `environment-setup`, followed by the runnable skeleton and meaningful smoke check in the dependent application skeleton task. Do not require the user to perform setup manually. Do not implement yet or mark unreviewed tasks Ready.

## Groom a task

> Act as the PM in `_docs/team/pm.md` for <task>. Resolve ambiguity, define observable acceptance criteria and verification steps, and preserve deferred work with links. Ask about blocking decisions. Do not write application code.

## Implement a task

> Read `AGENTS.md`. Act as the engineer in `_docs/team/software-engineer.md` for <ready task>. Implement its agreed scope, run applicable checks, and record a reviewable handoff. Report blockers and actual results. Leave completion to verification.

## Verify a task

> Read `AGENTS.md`. Act as QA in `_docs/team/qa-engineer.md` for <task and revision>. Verify every criterion and required check. Record evidence using the verification template and give PASS, FAIL, or BLOCKED. Do not fix code during this pass.

## Work through a bounded set

> Follow `_docs/process.md` and the orchestrator guide for <task IDs>. Use <sequential role passes or supported separate agents>. Budget: <time, cost, or attempt limit>. Stop when all selected tasks meet the completion gate, the budget is reached, or progress requires a missing decision or prerequisite. Do not expand scope. Report completed and remaining tasks with evidence.

## Change a requirement

> Assess <proposed change> against the product specification, architecture, active tasks, and existing verification. Describe its impact and unresolved decisions. Once the change is agreed, update the source documents, affected tasks, and verification needs. Preserve decision history.
