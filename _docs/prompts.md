# Feature development prompts

## Specify a feature

> Read AGENTS.md and the current product specification and architecture. Help me specify [feature]. Ask focused questions about consequential behavior, scope, failure cases and data handling. Update the relevant specifications, preserving existing requirement IDs. Do not implement until the consequential decisions are resolved.

## Hand over delivery

> Read AGENTS.md, _docs/process.md, _docs/team/orchestrator.md and _docs/team/execution-policy.md. Deliver the agreed [feature/release] through PM, developer and independent QA. Record the task set, current checkpoint, explicit model/reasoning settings and applicable limits. Preserve prior history and uncommitted work. Follow the graph without routine per-task prompts, reuse valid grooming/evidence, and complete integrated release QA and final requirements review. Do not push or deploy. Ask for consequential decisions, missing access or an explicit extension if an existing limit is exhausted.

## Resume delivery

> Read AGENTS.md, _docs/resume.md and the current task checkpoint. Resume the authorized [feature/release], preserving scope, retry/batch counts and unrelated work. Use fresh task-only agents and recorded model/reasoning settings. Continue until verified completion or a documented stop condition; do not reset limits because this session is new.
