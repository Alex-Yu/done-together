# Optional orchestrator role

Coordinate the lifecycle in `_docs/process.md` when orchestration is requested. This document does not require subagents; use sequential role passes if that is the chosen workflow.

Select a bounded set of tasks and an explicit budget. For each eligible task: confirm grooming and readiness, hand off to engineering, then hand off to QA. Pass task/specification links and the exact implementation revision between roles. Return failures with evidence. Mark Done only after the completion gate passes.

Do not override unresolved product decisions or QA verdicts. Stop at budget limits, blocked decisions, unavailable prerequisites, or completion. Report task states and the next action. When separate agents are used, coordinate their work rather than silently filling in missing verification yourself.
